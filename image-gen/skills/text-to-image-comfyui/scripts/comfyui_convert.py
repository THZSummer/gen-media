#!/usr/bin/env python3
"""Convert a ComfyUI UI workflow JSON (including subgraph/"definitions" bundles)
into ComfyUI API-format prompt JSON, and apply friendly parameter overrides.

Why: ComfyUI's modern template format stores the actual graph inside
``definitions.subgraphs`` and references it from a stub "subgraph node". The
``POST /prompt`` API wants a *flat* ``{node_id: {class_type, inputs}}`` graph.
This converter expands subgraphs recursively (nested ones included) and rewires
the links that cross subgraph boundaries.

Usage:
  python3 comfyui_convert.py workflow-ui.json -o workflow-api.json \
      --prompt "a red fox" --width 1024 --height 1024 --seed 42 --steps 8

  # inspect what a UI workflow exposes without writing an API file
  python3 comfyui_convert.py workflow-ui.json --list

Importable:
  from comfyui_convert import convert, resolve_params, PARAM_SCHEMA
  api_prompt, output_id = convert(ui_json, {"prompt": "...", "width": 512})
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from typing import Any


# --------------------------------------------------------------------------
# Parameter schema: friendly name -> how it maps onto the graph.
#   index:    position in the subgraph stub's widgets_values
#   aliases:  alternative friendly names
#   fallback: class_type used when the workflow has no subgraph interface
# --------------------------------------------------------------------------
PARAM_SCHEMA: dict[str, dict[str, Any]] = {
    "prompt": {"index": 0, "aliases": ["text", "positive"], "fallback": "CLIPTextEncode"},
    "width": {"index": 1, "fallback": "EmptySD3LatentImage"},
    "height": {"index": 2, "fallback": "EmptySD3LatentImage"},
    "seed": {"index": 3, "fallback": "KSampler"},
    "steps": {"index": 4, "fallback": "KSampler"},
    "unet_name": {"index": 5, "aliases": ["model", "ckpt_name"], "fallback": "UNETLoader"},
    "clip_name": {"index": 6, "aliases": ["text_encoder"], "fallback": "CLIPLoader"},
    "vae_name": {"index": 7, "fallback": "VAELoader"},
    # not a subgraph input: a node-local widget, set by name on its class
    "filename_prefix": {"widget_on": "SaveImage", "field": "filename_prefix"},
    "batch_size": {"widget_on": "EmptySD3LatentImage", "field": "batch_size", "aliases": ["batch", "n"]},
}
# widget index used when falling back to a class_type match
FALLBACK_WIDGET_INDEX: dict[str, int] = {
    "prompt": 0,
    "width": 0,
    "height": 1,
    "seed": 0,
    "steps": 2,
    "unet_name": 0,
    "clip_name": 0,
    "vae_name": 0,
    "batch_size": 2,
}

# The two synthetic ids ComfyUI uses for a subgraph's interface nodes.
SUBGRAPH_INPUT_NODE = -10
SUBGRAPH_OUTPUT_NODE = -20

class StubOut:
    """A subgraph output slot: points at the leaf node that actually produces it."""

    __slots__ = ("origin",)

    def __init__(self, origin: Any) -> None:
        self.origin = origin


class LinkRef:
    """A link id that still has to be resolved to (origin_node, origin_slot)."""

    __slots__ = ("link_id",)

    def __init__(self, link_id: Any) -> None:
        self.link_id = link_id

    def __repr__(self) -> str:  # pragma: no cover - debug aid
        return f"LinkRef({self.link_id!r})"


# UI-only helper nodes that must never reach the API prompt.
NON_EXECUTABLE_TYPES = {"MarkdownNote", "Note", "Reroute", "PrimitiveNode", "Bookmark"}

# Classes that terminate a graph and own the produced media.  The first match in
# this priority order is reported as the graph's output node, so a video
# workflow (SaveVideo) works exactly like an image one (SaveImage).
OUTPUT_NODE_CLASSES: tuple[str, ...] = ("SaveImage", "SaveVideo", "SaveWEBM", "SaveAudio")


class UnappliedOverrideError(ValueError):
    """A requested parameter never reached the submitted graph.

    This is the most expensive failure mode the converter has: the run looks
    healthy, the archive records the value, and the only symptom is an image
    that quietly ignored an instruction -- which then gets blamed on the prompt.
    ``convert`` refuses to hand back a graph in this state; ``convert_ex``
    records the keys in ``report``/warnings and only raises when ``strict``.
    """

    def __init__(self, unapplied: dict[str, Any]) -> None:
        self.unapplied = dict(unapplied)
        detail = ", ".join(f"{k}={v!r}" for k, v in sorted(self.unapplied.items()))
        super().__init__(
            f"{len(self.unapplied)} requested parameter(s) never reached the graph: {detail}. "
            "Check the spelling against --list, or the workflow really has no such input."
        )


# Where each requested parameter's value was written: key -> [(node_id, input_name)].
# ``input_name`` is None for a positional widget write, where the name is only
# decided later; verification then looks for the value in that node's inputs.
AppliedMap = dict[str, list[tuple[Any, "str | None"]]]


def _landed(api: dict[str, Any], dests: list[tuple[Any, "str | None"]], value: Any) -> bool:
    """True when the value is really present in the graph this converter built.

    Checking the *final* api (rather than trusting that a write happened) is what
    catches a literal that an upstream link overrides afterwards -- e.g. a
    top-level ResolutionSelector driving a subgraph's width/height, which used to
    be reported as applied while the graph contained no such value.
    """
    for nid, name in dests:
        entry = api.get(str(nid))
        if not isinstance(entry, dict):
            continue  # the node was bypassed/muted away, so nothing landed
        inputs = entry.get("inputs") or {}
        if name is None:
            if value in inputs.values():
                return True
        elif inputs.get(name) == value:
            return True
    return False


# Optional offline node schema: {class_type: {input_name: {required, widget, order}}}
_SCHEMA: dict[str, Any] | None = None


def load_node_info(path: str) -> None:
    """Load a cached /object_info subset used to name widget inputs offline."""
    global _SCHEMA
    with open(path, encoding="utf-8") as fh:
        _SCHEMA = json.load(fh)


def _schema_widget_names(class_type: str) -> list[str]:
    """Ordered widget-capable input names for a class, from the cached schema."""
    if not _SCHEMA:
        return []
    info = _SCHEMA.get(class_type)
    if not isinstance(info, dict):
        return []
    order = info.get("input_order") or {}
    names: list[str] = []
    for req in order.get("required", []) or []:
        if req in info:
            names.append(req)
    for opt in order.get("optional", []) or []:
        if opt in info:
            names.append(opt)
    return names


def _as_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _is_input_node(node_id: Any) -> bool:
    return _as_int(node_id) == SUBGRAPH_INPUT_NODE


def _is_output_node(node_id: Any) -> bool:
    return _as_int(node_id) == SUBGRAPH_OUTPUT_NODE


def _norm_links(links: Any) -> list[dict[str, Any]]:
    """Normalise both link encodings into dicts.

    - newer: [{"id":..,"origin_id":..,"origin_slot":..,"target_id":..,"target_slot":..}]
    - legacy: [[id, origin_id, origin_slot, target_id, target_slot, type]]
    """
    out: list[dict[str, Any]] = []
    for link in links or []:
        if isinstance(link, dict):
            if "origin_id" in link:
                out.append(link)
        elif isinstance(link, (list, tuple)) and len(link) >= 5:
            out.append(
                {
                    "id": link[0],
                    "origin_id": link[1],
                    "origin_slot": link[2],
                    "target_id": link[3],
                    "target_slot": link[4],
                }
            )
    return out


def find_subgraph_node(ui: dict[str, Any]) -> dict[str, Any] | None:
    """Top-level node whose type is a subgraph definition id."""
    sub_ids = {sg.get("id") for sg in ui.get("definitions", {}).get("subgraphs", [])}
    for node in ui.get("nodes", []):
        if node.get("type") in sub_ids:
            return node
    return None


def find_subgraph(ui: dict[str, Any], node: dict[str, Any]) -> dict[str, Any] | None:
    for sg in ui.get("definitions", {}).get("subgraphs", []):
        if sg.get("id") == node.get("type"):
            return sg
    return None


def _set_input(node: dict[str, Any] | None, slot: int, value: Any, *, force: bool = False) -> bool:
    """Write ``value`` onto an input slot; True when the graph was really changed.

    The return value is what makes unapplied-override reporting possible: a
    silent no-op here is exactly how ``--width`` used to vanish without a word.
    """
    if node is None:
        return False
    inputs = node.get("inputs", [])
    if slot >= len(inputs):
        return False
    name = inputs[slot].get("name")
    overrides = node.setdefault("_param_overrides", {})
    if not force and name in overrides:
        # an explicit override is already pending; defaults must not clobber it
        return False
    inputs[slot]["widget_value"] = value
    overrides[name] = value
    return True


def _set_widget(node: dict[str, Any], index: int, value: Any) -> None:
    wv = node.get("widgets_values")
    if not isinstance(wv, list):
        wv = []
        node["widgets_values"] = wv
    while len(wv) <= index:
        wv.append(None)
    wv[index] = value


def _widget_default(node: dict[str, Any], slot: int) -> Any:
    """Positional widget value for an input, when widgets_values is available."""
    inputs = node.get("inputs", []) or []
    wv = node.get("widgets_values")
    if not isinstance(wv, list):
        return None
    rank = -1
    for i in range(min(slot, len(inputs) - 1) + 1):
        if "widget" in (inputs[i] or {}):
            rank += 1
    if 0 <= rank < len(wv):
        return wv[rank]
    return None


def _alias_to_key(profile: dict[str, Any] | None = None) -> dict[str, str]:
    out: dict[str, str] = {}
    for key, spec in PARAM_SCHEMA.items():
        out[key] = key
        for alias in spec.get("aliases", []):
            out[alias] = key
    # a workflow profile may declare extra parameters and aliases
    for key, spec in ((profile or {}).get("parameters", {}) or {}).items():
        out[key] = key
        for alias in spec.get("aliases", []):
            out[alias] = key
    return out


def _profile_interface(profile: dict[str, Any] | None, canonical: str) -> str | None:
    spec = ((profile or {}).get("parameters", {}) or {}).get(canonical) or {}
    return spec.get("interface")


def _apply_node_local_overrides(
    nodes: dict[Any, dict[str, Any]],
    overrides: dict[str, Any],
    applied: AppliedMap | None = None,
) -> None:
    """Apply parameters that live on a specific class rather than a subgraph input."""
    alias = _alias_to_key()
    for key, value in overrides.items():
        spec = PARAM_SCHEMA.get(alias.get(key, ""))
        if not spec or value is None or "widget_on" not in spec:
            continue
        field = spec.get("field", key)
        for nid, node in nodes.items():
            if node.get("type") == spec["widget_on"]:
                node.setdefault("_param_overrides", {})[field] = value
                if applied is not None:
                    applied.setdefault(key, []).append((nid, field))



def _iface_target(sg: dict[str, Any], iface: dict[str, Any]):
    """(node_id, slot) that this subgraph interface input feeds, if any."""
    ids = set(iface.get("linkIds") or [])
    for link in _norm_links(sg.get("links", [])):
        if _is_input_node(link.get("origin_id")) and link.get("id") in ids:
            return link.get("target_id"), link.get("target_slot")
    return None


def _iface_is_widget(sg: dict[str, Any], iface: dict[str, Any]) -> bool:
    """True when the interface input lands on a widget-style node input."""
    target = _iface_target(sg, iface)
    if not target:
        return False
    for node in sg.get("nodes", []):
        if node.get("id") == target[0]:
            ins = node.get("inputs", []) or []
            return target[1] < len(ins) and bool((ins[target[1]] or {}).get("widget"))
    return False


def _seed_stub_values(sg: dict[str, Any], stub: dict[str, Any]) -> None:
    """Map the stub's widgets_values onto the subgraph inputs that are widgets.

    Stub widget values are positional over *widget* inputs only; interfaces that
    are link inputs (e.g. an IMAGE control input) do not consume a widget slot.
    """
    values = list(stub.get("widgets_values") or [])
    cursor = 0
    for iface in sg.get("inputs", []):
        if not _iface_is_widget(sg, iface):
            continue
        if cursor < len(values) and values[cursor] is not None:
            iface["_stub_value"] = values[cursor]
        cursor += 1


def _apply_subgraph_params(
    sg: dict[str, Any],
    overrides: dict[str, Any],
    profile: dict[str, Any] | None = None,
    applied: AppliedMap | None = None,
) -> None:
    """Write override values onto the right inner nodes/widgets of a subgraph."""
    # linkId -> target (node_id, slot) for links originating from the input node
    targets: dict[int, tuple[Any, int]] = {}
    for link in _norm_links(sg.get("links", [])):
        if _is_input_node(link.get("origin_id")):
            targets[link["id"]] = (link["target_id"], link["target_slot"])

    # seed defaults from the stub node's widget values so omitted params keep
    # the values the workflow shipped with.
    nodes_by_id_all = {n.get("id"): n for n in sg.get("nodes", [])}
    for iface in sg.get("inputs", []):
        if iface.get("_stub_value") is None:
            continue
        for lid in iface.get("linkIds", []) or []:
            if lid in targets:
                nid, slot = targets[lid]
                _set_input(nodes_by_id_all.get(nid), slot, iface["_stub_value"])

    alias_to_key = _alias_to_key(profile)

    for key, value in overrides.items():
        canonical = alias_to_key.get(key)
        if canonical is None or value is None:
            continue
        spec = PARAM_SCHEMA.get(canonical, {})
        if "widget_on" in spec:
            # node-local widget, handled by _apply_node_local_overrides / profile
            continue
        profile_iface = _profile_interface(profile, canonical)
        if profile_iface is None and canonical in ((profile or {}).get("parameters", {}) or {}):
            # profile declares this parameter as node/field based only
            continue
        wanted = profile_iface or {"prompt": "text"}.get(canonical, canonical)
        match = None
        for iface in sg.get("inputs", []):
            if iface.get("name") in (wanted, canonical) or iface.get("label") in (wanted, canonical):
                match = iface
                break
        if match is not None:
            for lid in match.get("linkIds", []) or []:
                if lid in targets:
                    nid, slot = targets[lid]
                    node = nodes_by_id_all.get(nid)
                    if _set_input(node, slot, value, force=True) and applied is not None:
                        name = (node.get("inputs", []) or [])[slot].get("name")
                        applied.setdefault(key, []).append((nid, name))
            continue
        # no interface match -> fall back to a widget index on the class type
        cls = spec.get("fallback")
        idx = FALLBACK_WIDGET_INDEX.get(canonical)
        if cls is None or idx is None:
            continue
        for node in sg.get("nodes", []):
            if node.get("type") == cls:
                _set_widget(node, idx, value)
                if applied is not None:
                    applied.setdefault(key, []).append((node.get("id"), None))
                break


def _expand_nodes(
    ui: dict[str, Any],
    overrides: dict[str, Any],
    out_nodes: dict[Any, dict[str, Any]] | None = None,
    out_links: dict[tuple[Any, int], tuple[Any, int]] | None = None,
    profile: dict[str, Any] | None = None,
    applied: AppliedMap | None = None,
) -> tuple[dict[Any, dict[str, Any]], dict[tuple[Any, int], tuple[Any, int]], list[str]]:
    """Flatten every (possibly nested) subgraph into leaf nodes + a link map."""
    out_nodes = {} if out_nodes is None else out_nodes
    out_links = {} if out_links is None else out_links
    warnings: list[str] = []
    sub_ids = {sg.get("id") for sg in ui.get("definitions", {}).get("subgraphs", [])}

    stub = find_subgraph_node(ui)
    subgraph_overrides: dict[Any, dict[str, Any]] = {}
    if stub is not None:
        sg = find_subgraph(ui, stub)
        if sg is not None:
            _seed_stub_values(sg, stub)
            _apply_subgraph_params(sg, overrides, profile, applied)
            # node-local params may live on any node inside the subgraph too
            _apply_node_local_overrides({n.get("id"): n for n in sg.get("nodes", [])}, overrides, applied)
            subgraph_overrides[stub.get("id")] = dict(stub.get("_param_overrides", {}))

    def walk(node: dict[str, Any]) -> None:
        nid = node.get("id")
        if nid in out_nodes:
            return
        if node.get("type") in sub_ids:
            sg = find_subgraph(ui, node)
            if sg is None:
                return
            _seed_stub_values(sg, node)
            _apply_subgraph_params(sg, subgraph_overrides.get(nid, {}), profile, applied)
            subgraph_overrides.setdefault(nid, {})
            for inner in sg.get("nodes", []):
                walk(inner)
            for link in _norm_links(sg.get("links", [])):
                if _is_output_node(link.get("target_id")):
                    origin = (link["origin_id"], link["origin_slot"])
                    if _is_input_node(origin[0]):
                        # passthrough: the subgraph forwards one of its inputs
                        socket = next(
                            (
                                si
                                for si in (node.get("inputs") or [])
                                if si.get("name")
                                == (sg.get("inputs") or [{}])[origin[1]].get("name")
                            ),
                            None,
                        )
                        raw = (socket or {}).get("link")
                        if raw is not None:
                            out_links[(nid, link["target_slot"])] = LinkRef(raw)
                            continue
                    out_links[(nid, link["target_slot"])] = StubOut(origin)
                elif not _is_input_node(link.get("origin_id")):
                    out_links[(link["target_id"], link["target_slot"])] = (
                        link["origin_id"],
                        link["origin_slot"],
                    )
            # link-type interface inputs (e.g. a control IMAGE): wire the inner
            # consumers to whatever feeds this slot on the parent graph
            inner_by_iface: dict[int, list[tuple[Any, int]]] = {}
            for link in _norm_links(sg.get("links", [])):
                if _is_input_node(link.get("origin_id")):
                    inner_by_iface.setdefault(link["origin_slot"], []).append(
                        (link["target_id"], link["target_slot"])
                    )
            for i, iface in enumerate(sg.get("inputs", [])):
                consumers = inner_by_iface.get(i) or []
                if not consumers:
                    continue
                socket = next(
                    (si for si in (node.get("inputs") or []) if si.get("name") == iface.get("name")),
                    None,
                )
                raw = (socket or {}).get("link")
                if raw is None:
                    raw = next(iter((socket or {}).get("links") or []), None)
                if _iface_is_widget(sg, iface):
                    # A widget interface is normally a literal, but the parent
                    # graph may also link into it (e.g. a top-level
                    # ResolutionSelector driving a subgraph's width/height).  The
                    # upstream link wins, exactly as it does in the ComfyUI UI --
                    # otherwise the parent node would be a silent no-op.
                    if raw is not None:
                        for key in consumers:
                            out_links[key] = LinkRef(raw)
                    continue
                if raw is None:
                    # A profile may declare interfaces it deliberately leaves
                    # unconnected (e.g. a t2v workflow's optional first/last
                    # frame inputs), which keeps the run warning-free.
                    if iface.get("name") in set((profile or {}).get("expected_unconnected", []) or []):
                        continue
                    warnings.append(
                        f"subgraph input '{iface.get('name')}' is not connected upstream; "
                        f"consumers {consumers} will miss a required input"
                    )
                    continue
                for key in consumers:
                    out_links[key] = LinkRef(raw)
            # the stub node's own inputs (e.g. a SaveImage fed by it)
            for slot, inp in enumerate(node.get("inputs", []) or []):
                if "link" in (inp or {}) and inp["link"] is not None:
                    out_links.setdefault((nid, slot), LinkRef(inp["link"]))
                for lid in (inp or {}).get("links", []) or []:
                    out_links.setdefault((nid, slot), LinkRef(lid))
            return
        out_nodes[nid] = node
        for slot, inp in enumerate(node.get("inputs", []) or []):
            if "link" in (inp or {}) and inp["link"] is not None:
                # legacy encodings carry the incoming link id on the input itself
                out_links.setdefault((nid, slot), LinkRef(inp["link"]))

    for node in ui.get("nodes", []):
        walk(node)
    # node-local params (e.g. SaveImage.filename_prefix) live outside subgraphs
    _apply_node_local_overrides(out_nodes, overrides, applied)
    return out_nodes, out_links, warnings


def _resolve_origin(
    origin: Any,
    index: dict[Any, tuple[Any, int]],
    chain: dict[tuple[Any, int], Any] | None = None,
) -> tuple[Any, int] | None:
    """Follow link-id references and subgraph-output hops to a real (node, slot)."""
    seen: set[Any] = set()
    while True:
        if isinstance(origin, LinkRef):
            lid = origin.link_id
            if lid in seen:
                return None
            seen.add(lid)
            nxt = index.get(lid)
            if nxt is None:
                return None
            origin = nxt
            continue
        if isinstance(origin, StubOut):
            origin = origin.origin
            if isinstance(origin, tuple) and _is_input_node(origin[0]):
                # the producer resolves through the subgraph's own inputs; the
                # caller's parameter map already handled it
                return None
            continue
        if isinstance(origin, tuple) and len(origin) == 2:
            return origin
        return None


def _named_widget_map(node: dict[str, Any]) -> dict[str, Any]:
    """input name -> value, from widgets_values_named (order-independent)."""
    named = node.get("widgets_values_named")
    if isinstance(named, dict):
        return {k: v for k, v in named.items() if v is not None}
    return {}


def _build_link_index(ui: dict[str, Any]) -> dict[Any, tuple[Any, int]]:
    """link id -> (origin_id, origin_slot) across the top level and every subgraph."""
    index: dict[Any, tuple[Any, int]] = {}
    for link in _norm_links(ui.get("links", [])):
        index[link.get("id")] = (link["origin_id"], link["origin_slot"])
    for sg in ui.get("definitions", {}).get("subgraphs", []) or []:
        for link in _norm_links(sg.get("links", [])):
            index.setdefault(link.get("id"), (link["origin_id"], link["origin_slot"]))
    return index



def load_profile(path: str) -> dict[str, Any]:
    """Load a workflow profile: parameter -> {interface | node+field} mapping."""
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def apply_profile(
    nodes: dict[Any, dict[str, Any]],
    link_map: dict[tuple[Any, int], Any],
    profile: dict[str, Any] | None,
    values: dict[str, Any],
    applied: AppliedMap | None = None,
) -> list[str]:
    """Apply node/field parameters declared by a profile. Returns warnings."""
    warnings: list[str] = []
    params = ((profile or {}).get("parameters", {}) or {})
    for key, value in values.items():
        if value is None:
            continue
        spec = params.get(key)
        if spec is None or "interface" in spec:
            continue  # interface params are handled during subgraph expansion
        cls, field = spec.get("node"), spec.get("field")
        targets = [nid for nid, n in nodes.items() if n.get("type") == cls]
        if not targets:
            warnings.append(f"{key}: no node of class {cls} found")
            continue
        nid = targets[0]
        node = nodes[nid]
        node.setdefault("_param_overrides", {})[field] = value
        if spec.get("enable"):
            node["mode"] = 0
            node["_profile_enabled"] = True
        # is this field fed by a link?
        linked_slot = None
        for slot, inp in enumerate(node.get("inputs", []) or []):
            if inp.get("name") == field and (nid, slot) in link_map:
                linked_slot = slot
                break
        if linked_slot is not None and not spec.get("force"):
            # the link wins in the built graph, so the literal value never lands
            warnings.append(
                f"{key}: {cls}.{field} is driven by a link; value ignored "
                f"(set \"force\": true in the profile to override)"
            )
            continue
        if linked_slot is not None:
            # cut the link so the literal value is used instead
            link_map.pop((nid, linked_slot), None)
        if applied is not None:
            applied.setdefault(key, []).append((nid, field))
    return warnings


def _out_type(node: dict[str, Any], slot: int) -> Any:
    outs = node.get("outputs", []) or []
    return (outs[slot] or {}).get("type") if slot < len(outs) else None


def hoist_disabled_nodes(
    nodes: dict[Any, dict[str, Any]],
    link_map: dict[tuple[Any, int], Any],
    extra_modes: dict[str, int] | None = None,
) -> tuple[set[Any], list[str]]:
    """Handle ComfyUI mute (mode 2) / bypass (mode 4) nodes for the API graph.

    * bypass: drop the node and rewire its consumers to whatever fed it
    * mute:   drop the node and its consumer links (reported as warnings)
    """
    warnings: list[str] = []
    for cls, mode in (extra_modes or {}).items():
        for nid, node in nodes.items():
            if node.get("type") == cls:
                node["mode"] = mode
                node.pop("_profile_enabled", None)
    disabled: dict[Any, int] = {}
    for nid, node in nodes.items():
        mode = node.get("mode", 0)
        if mode in (2, 4):
            disabled[nid] = mode

    def origin_of(node: dict[str, Any], nid: Any, want_type: Any) -> Any:
        """First feed of this node that can stand in for the wanted type."""
        fallback = None
        for slot, inp in enumerate(node.get("inputs", []) or []):
            cand = link_map.get((nid, slot))
            if cand is None:
                continue
            if fallback is None:
                fallback = cand
            if want_type is not None and (inp or {}).get("type") == want_type:
                return cand
        return fallback

    # bypass rewiring (iterate: chains of bypassed nodes need several passes)
    for _ in range(8):
        changed = False
        for nid, mode in list(disabled.items()):
            if mode != 4:
                continue
            node = nodes[nid]
            for slot in range(len(node.get("outputs", []) or [])):
                want = _out_type(node, slot)
                feed = origin_of(node, nid, want)
                for key, origin in list(link_map.items()):
                    if isinstance(origin, tuple) and len(origin) == 2 and origin == (nid, slot):
                        if feed is not None:
                            link_map[key] = feed
                        else:
                            link_map.pop(key, None)
                        changed = True
        if not changed:
            break

    # mute: consumer links are dead
    for nid, mode in disabled.items():
        if mode != 2:
            continue
        for key, origin in list(link_map.items()):
            if isinstance(origin, tuple) and len(origin) == 2 and origin[0] == nid:
                link_map.pop(key, None)
                warnings.append(f"input {key} referenced muted node {nid} ({nodes[nid].get('type')}); link dropped")
    return set(disabled), warnings


def convert_ex(
    ui: dict[str, Any],
    overrides: dict[str, Any] | None = None,
    profile: dict[str, Any] | None = None,
    node_modes: dict[str, int] | None = None,
    *,
    strict: bool = False,
    report: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], str | None, list[str]]:
    """Return (api_prompt, output_node_id, warnings).

    ``output_node_id`` is the SaveImage/SaveVideo/SaveWEBM/SaveAudio node whose
    outputs hold the produced media (highest priority class wins).

    Every requested override is tracked.  Ones that no node, interface or
    profile entry accepted are listed in ``warnings`` (and in ``report``); with
    ``strict=True`` they raise :class:`UnappliedOverrideError` instead of
    producing a graph that silently ignored them.  ``report`` receives
    ``{"applied": [...], "unapplied": {...}}`` when a dict is passed.
    """
    overrides = {k: v for k, v in (overrides or {}).items() if v is not None}
    ui = copy.deepcopy(ui)  # callers may reuse the loaded workflow
    if find_subgraph_node(ui) is None:
        raise ValueError("no subgraph node found; this converter expects a definitions.subgraphs workflow")

    applied: AppliedMap = {}
    nodes, link_map, expand_warnings = _expand_nodes(ui, overrides, profile=profile, applied=applied)
    link_index = _build_link_index(ui)
    pending_origin: list[tuple[Any, int]] = []

    def absorb() -> None:
        """Collapse link ids and subgraph-output hops to real (node, slot) pairs."""
        while pending_origin:
            key = pending_origin.pop()
            resolved = _resolve_origin(link_map.get(key), link_index, link_map)
            if resolved is None:
                continue
            link_map[key] = resolved
            # A StubOut whose producer is itself a subgraph input is a
            # passthrough; keep following. Never follow a plain tuple: (node,
            # slot) is an *origin* reference and may collide with an input key.
            if (resolved[0], resolved[1]) in link_map:
                nxt = link_map[(resolved[0], resolved[1])]
                if isinstance(nxt, StubOut):
                    link_map[key] = nxt
                    pending_origin.append(key)

    # pre-pass: every (node, slot) whose origin is a legacy link id, so that
    # chains through subgraph outputs resolve before entries are built
    for nid, node in nodes.items():
        for slot, inp in enumerate(node.get("inputs", []) or []):
            key = (nid, slot)
            if isinstance(link_map.get(key), (LinkRef, StubOut)):
                pending_origin.append(key)
    absorb()

    warnings = list(expand_warnings) + apply_profile(nodes, link_map, profile, overrides, applied)
    # UI-only widget fields (e.g. LoadImage's "upload" combo) must not be sent
    drop_inputs: dict[str, list[str]] = (profile or {}).get("drop_inputs", {}) or {}
    disabled, mode_warnings = hoist_disabled_nodes(nodes, link_map, node_modes)
    warnings += mode_warnings

    api: dict[str, Any] = {}
    output_id: str | None = None
    output_rank: int | None = None
    for nid, node in nodes.items():
        cls = node.get("type")
        if _as_int(nid) is not None and _as_int(nid) < 0:
            continue
        if cls in NON_EXECUTABLE_TYPES:
            continue
        if nid in disabled:
            continue
        entry: dict[str, Any] = {"class_type": cls}
        inputs: dict[str, Any] = {}
        pending = node.get("_param_overrides", {})
        # explicit overrides win over every inferred source, including widgets
        # with no declared input (e.g. SaveImage.filename_prefix)
        for field, value in pending.items():
            if value is not None:
                inputs[field] = value
        named = _named_widget_map(node)
        node_inputs = node.get("inputs", []) or []
        assigned: list[int] = []
        for slot, inp in enumerate(node_inputs):
            key = (nid, slot)
            origin = _resolve_origin(link_map.get(key), link_index, link_map)
            if origin is None and isinstance(link_map.get(key), (LinkRef, StubOut)):
                pending_origin.append(key)
            name = inp.get("name")
            if not name:
                continue
            if origin is not None and origin[0] is not None and not _is_input_node(origin[0]):
                inputs[name] = [str(origin[0]), origin[1]]
                assigned.append(slot)
                continue
            if name in pending:
                assigned.append(slot)
                continue
            if name in named:
                inputs[name] = named[name]
                assigned.append(slot)
                continue
            if "widget_value" in inp and inp["widget_value"] is not None:
                inputs[name] = inp["widget_value"]
                assigned.append(slot)
                continue
            if inp.get("widget"):
                value = _widget_default(node, slot)
                if value is not None:
                    inputs[name] = value
                    assigned.append(slot)
        # widgets_values whose named input is not declared in the node JSON
        # (ComfyUI omits pure widgets like cfg / sampler_name / scheduler there)
        wv = node.get("widgets_values")
        if isinstance(wv, list):
            raw_keys = list(named.keys()) if named else [
                i.get("name") for i in node_inputs if i.get("widget")
            ]
            for i, value in enumerate(wv):
                if value is None or i >= len(raw_keys):
                    continue
                inputs.setdefault(raw_keys[i], value)
        # last resort: map by declared widget order using the cached schema
        schema_widgets = _schema_widget_names(cls)
        for slot, inp in enumerate(node_inputs):
            if slot in assigned or not inp.get("widget"):
                continue
            name = inp.get("name")
            if name in inputs:
                continue
            if slot < len(schema_widgets) and schema_widgets[slot] not in inputs:
                value = _widget_default(node, slot)
                if value is not None:
                    inputs[schema_widgets[slot]] = value
        # node-local overrides already applied before the slots were read
        for drop in drop_inputs.get(cls, ()):
            inputs.pop(drop, None)
        entry["inputs"] = inputs
        api[str(nid)] = entry
        if cls in OUTPUT_NODE_CLASSES:
            rank = OUTPUT_NODE_CLASSES.index(cls)
            if output_rank is None or rank < output_rank:
                output_rank, output_id = rank, str(nid)
    absorb()
    # Verify against the graph that will actually be sent: a value written into
    # an inner node can still be overridden by a link from the parent graph, and
    # a node can be bypassed away, so the write itself proves nothing.
    landed = {k for k, v in overrides.items() if _landed(api, applied.get(k) or [], v)}
    unapplied = {k: v for k, v in overrides.items() if k not in landed}
    if report is not None:
        report["applied"] = sorted(landed)
        report["unapplied"] = dict(unapplied)
    if unapplied:
        warnings.append(
            "unapplied override(s): "
            + ", ".join(f"{k}={v!r}" for k, v in sorted(unapplied.items()))
            + " -- these never reached the graph"
        )
        if strict:
            raise UnappliedOverrideError(unapplied)
    return api, output_id, warnings


def convert(
    ui: dict[str, Any],
    overrides: dict[str, Any] | None = None,
    profile: dict[str, Any] | None = None,
    node_modes: dict[str, int] | None = None,
    *,
    strict: bool = True,
    report: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], str | None]:
    """`(api_prompt, output_node_id)`; raises when an override was not applied.

    Strict by default: a parameter that cannot reach the graph is a mistake, and
    handing back a graph that quietly ignored it is how a whole round of
    experiments gets a wrong conclusion.  Pass ``strict=False`` to only collect
    the keys in ``report`` instead.
    """
    api, save_id, _warnings = convert_ex(ui, overrides, profile, node_modes, strict=strict, report=report)
    return api, save_id


def resolve_params(ui: dict[str, Any]) -> dict[str, Any]:
    """Merge subgraph-stub widget values with per-input names for display."""
    stub = find_subgraph_node(ui)
    if stub is None:
        return {}
    sg = find_subgraph(ui, stub) or {}
    _seed_stub_values(sg, stub)
    out: dict[str, Any] = {}
    for iface in sg.get("inputs", []):
        out[iface.get("name")] = iface.get("_stub_value")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("workflow", help="UI workflow JSON path")
    ap.add_argument("-o", "--out", help="where to write API-format JSON")
    ap.add_argument("--prompt")
    ap.add_argument("--negative", default=None, help="reserved; Z-Image-Turbo workflow has no negative branch")
    ap.add_argument("--width", type=int)
    ap.add_argument("--height", type=int)
    ap.add_argument("--seed", type=int)
    ap.add_argument("--steps", type=int)
    ap.add_argument("--unet-name")
    ap.add_argument("--clip-name")
    ap.add_argument("--vae-name")
    ap.add_argument("--filename-prefix")
    ap.add_argument("--batch", "--batch-size", dest="batch_size", type=int, help="images per request")
    ap.add_argument("--list", action="store_true", help="print discoverable parameters and exit")
    ap.add_argument("--allow-unapplied", action="store_true",
                    help="do not fail when a requested parameter has no input to land on")
    ap.add_argument("--node-info", help="cached /object_info subset used to name widget inputs")
    args = ap.parse_args(argv)

    if args.node_info:
        load_node_info(args.node_info)
    ui = json.load(open(args.workflow, encoding="utf-8"))
    if args.list:
        print(json.dumps(resolve_params(ui), ensure_ascii=False, indent=2))
        return 0

    overrides = {
        k: getattr(args, k)
        for k in (
            "prompt",
            "width",
            "height",
            "seed",
            "steps",
            "unet_name",
            "clip_name",
            "vae_name",
            "filename_prefix",
            "batch_size",
        )
    }
    report: dict[str, Any] = {}
    try:
        api, save_id = convert(ui, overrides, strict=not args.allow_unapplied, report=report)
    except UnappliedOverrideError as exc:
        print(f"error: {exc}", file=sys.stderr)
        print(f"       applied: {', '.join(report.get('applied', [])) or '(none)'}", file=sys.stderr)
        return 2
    if report.get("unapplied"):
        print(f"warning: unapplied {report['unapplied']}", file=sys.stderr)
    text = json.dumps(api, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print(f"wrote {args.out} ({len(api)} nodes, output node {save_id})")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
