#!/usr/bin/env python3
"""
移步换景 v2 - 官方 API 直连视频生成脚本（不走 arkcli）

直接调用火山方舟官方 API 创建视频生成任务：
  POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks

关键点（官方文档确认）：
- generate_audio 默认 true：生成与画面同步的有声视频（单声道，Seedance 2.0 系列支持）
- 多模态参考：content 里 type=image_url + role=reference_image；type=audio_url + role=reference_audio
- 首帧/参考图差异：role=first_frame（首帧）vs role=reference_image（参考图，可配合多模态）
- 异步任务：创建后轮询查询接口直到 succeeded/failed
- return_last_frame=true 可返回尾帧（链式续接）

用法：
  python3 gen_video.py                     # 用脚本内置的 5s 测试 prompt
  python3 gen_video.py "自定义prompt" --duration 5 --ratio 16:9 --resolution 480p
"""
import json
import os
import sys
import time
import base64
import requests

# ============ 配置 ============

def _load_key_from_arkcli():
    """从 arkcli 配置读取 platform（数据面）API Key"""
    import glob
    import yaml
    # 优先 platform profile 的 key（数据面有效；agent-plan key 在 /api/v3 会 401）
    conf = os.path.expanduser("~/.arkcli/config.yaml")
    if os.path.exists(conf):
        try:
            d = yaml.safe_load(open(conf))
            for name, prof in (d.get("profiles") or {}).items():
                if "platform" in name and prof.get("api_key"):
                    return prof["api_key"]
        except Exception:
            pass
    for p in glob.glob(os.path.expanduser("~/.arkcli/identities/*/apikey.json")):
        try:
            d = json.load(open(p))
            if d.get("api_key"):
                return d["api_key"]
        except Exception:
            pass
    raise SystemExit("❌ 未找到 platform API Key，请设置 ARK_API_KEY 环境变量")


API_KEY = os.environ.get("ARK_API_KEY") or _load_key_from_arkcli()
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
CREATE_URL = f"{BASE_URL}/contents/generations/tasks"   # POST 创建
GET_URL = f"{BASE_URL}/contents/generations/tasks/{{id}}"  # GET 查询

MODEL = "doubao-seedance-2-0-260128"


def _read_asset(path):
    """本地文件 -> base64 data url（参考图/音频需要公网 URL 或 base64）"""
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    ext = os.path.splitext(path)[1].lstrip(".").lower()
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "mp3": "mpeg",
            "wav": "wav", "mp4": "mp4"}.get(ext, ext)
    return f"data:image/{mime};base64,{b64}" if ext in ("jpg", "jpeg", "png") else f"data:audio/{mime};base64,{b64}"


def create_task(prompt, ref_image=None, ref_audio=None, duration=5, ratio="16:9",
                resolution="480p", generate_audio=True, watermark=False,
                return_last_frame=False):
    """创建视频生成任务，返回 task_id"""
    content = [{"type": "text", "text": prompt}]
    if ref_image:
        content.append({
            "type": "image_url",
            "image_url": {"url": _read_asset(ref_image)},
            "role": "reference_image",
        })
    if ref_audio:
        content.append({
            "type": "audio_url",
            "audio_url": {"url": _read_asset(ref_audio)},
            "role": "reference_audio",
        })

    body = {
        "model": MODEL,
        "content": content,
        "generate_audio": generate_audio,
        "ratio": ratio,
        "resolution": resolution,
        "duration": duration,
        "watermark": watermark,
        "return_last_frame": return_last_frame,
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    resp = requests.post(CREATE_URL, headers=headers, json=body, timeout=60)
    if resp.status_code != 200:
        raise SystemExit(f"❌ 创建失败 {resp.status_code}: {resp.text}")
    data = resp.json()
    task_id = data.get("id")
    print(f"✅ 任务已创建: {task_id} (status={data.get('status')})")
    return task_id


def poll_task(task_id, interval=10, timeout=1800):
    """轮询任务直到 succeeded/failed，返回完整结果"""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    start = time.time()
    while time.time() - start < timeout:
        resp = requests.get(GET_URL.format(id=task_id), headers=headers, timeout=30)
        if resp.status_code != 200:
            print(f"⚠️ 查询异常 {resp.status_code}: {resp.text}")
            time.sleep(interval)
            continue
        data = resp.json()
        status = data.get("status")
        print(f"  [{time.time()-start:.0f}s] status={status}")
        if status == "succeeded":
            return data
        if status == "failed":
            raise SystemExit(f"❌ 任务失败: {json.dumps(data.get('error', {}), ensure_ascii=False)}")
        time.sleep(interval)
    raise SystemExit("❌ 轮询超时")


def download_result(data, out_path):
    """下载生成视频到本地，并打印元信息"""
    print("----- 任务成功 -----")
    content = data.get("content")
    video_url = None
    last_frame_url = None
    if isinstance(content, dict):
        video_url = content.get("video_url")
        last_frame_url = content.get("last_frame_url")
    elif isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and item.get("type") == "video_url":
                video_url = item["video_url"]["url"]
            if isinstance(item, dict) and item.get("type") == "image_url" and "last_frame" in str(item.get("role", "")).lower():
                last_frame_url = item["image_url"]["url"]
    if not video_url:
        # 兼容返回结构：output_url / video_url 顶层字段
        video_url = data.get("output_url") or data.get("video_url")
    if not last_frame_url:
        last_frame_url = data.get("last_frame_url") or data.get("last_frame")
    if not video_url:
        print("⚠️ 未找到视频 URL，完整结果：")
        print(json.dumps(data, ensure_ascii=False, indent=1)[:2500])
        return
    print(f"下载: {video_url[:100]}...")
    r = requests.get(video_url, timeout=120)
    with open(out_path, "wb") as f:
        f.write(r.content)
    print(f"✅ 已保存: {out_path} ({len(r.content)/1024/1024:.1f} MB)")
    if last_frame_url:
        lf_path = os.path.splitext(out_path)[0] + "_lastframe.png"
        try:
            r2 = requests.get(last_frame_url, timeout=60)
            with open(lf_path, "wb") as f:
                f.write(r2.content)
            print(f"✅ 尾帧已保存: {lf_path}")
        except Exception as e:
            print(f"⚠️ 尾帧下载失败: {e}")
    else:
        print("⚠️ 本次返回无尾帧字段")
    # 打印关键元信息
    for k in ("duration", "ratio", "resolution", "generate_audio", "usage"):
        if k in data:
            print(f"  {k}: {data[k]}")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    kwargs = {}
    i = 1
    argv = sys.argv[1:]
    while i < len(argv):
        if argv[i] == "--duration":
            kwargs["duration"] = int(argv[i + 1]); i += 2
        elif argv[i] == "--ratio":
            kwargs["ratio"] = argv[i + 1]; i += 2
        elif argv[i] == "--resolution":
            kwargs["resolution"] = argv[i + 1]; i += 2
        elif argv[i] == "--ref-image":
            kwargs["ref_image"] = argv[i + 1]; i += 2
        elif argv[i] == "--ref-audio":
            kwargs["ref_audio"] = argv[i + 1]; i += 2
        elif argv[i] == "--no-audio":
            kwargs["generate_audio"] = False; i += 1
        elif argv[i] == "--last-frame":
            kwargs["return_last_frame"] = True; i += 1
        else:
            i += 1

    prompt = args[0] if args else (
        "电影级写实，跨步落地换景：清纯东方少女（约十六七岁，婴儿肥鹅蛋脸，清澈眼眸，"
        "额心朱砂，高马尾发梢化开光尘，素纱水墨长裙）站在青翠竹林中，以极缓慢的慢动作"
        "抬起右脚向前跨出，脚落地的瞬间竹林炸裂化作金黄沙漠，沙粒飞扬热浪蒸腾；"
        "她的动作缓慢从容，世界在落地瞬间切换；"
        "音画同步：竹林风声、脚落地踏沙声、沙粒簌簌"
    )
    task_id = create_task(prompt, **kwargs)
    data = poll_task(task_id)
    out = f"out/video/api_{int(time.time())}.mp4"
    os.makedirs("out/video", exist_ok=True)
    download_result(data, out)


if __name__ == "__main__":
    main()
