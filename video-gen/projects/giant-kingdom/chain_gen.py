#!/usr/bin/env python3
"""
蝴蝶女大冒险 - 链式续接视频生成（一致性保证）

核心逻辑（用户确认的正确方式）：
  镜1: 分镜图当首帧 + return_last_frame → 视频 + 尾帧
  镜2: 上一镜尾帧当首帧 + return_last_frame → 视频 + 尾帧
  镜3: ... 依次链下去
每镜首帧 = 上一镜真实末帧 → 人物/场景/光线自然延续，一致性有保证。

用法：
  python3 chain_gen.py                       # 跑完整 5 镜链
  python3 chain_gen.py --start 2             # 从第 2 镜开始（跳过已生成的）
"""
import json
import os
import sys
import time
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))
import importlib.util
spec = importlib.util.spec_from_file_location("gv", "scripts/gen_video.py")
gv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gv)

OUT_VIDEO = os.path.join(os.path.dirname(__file__), "out", "video")
OUT_STORY = os.path.join(os.path.dirname(__file__), "out", "storyboard")

# 5 镜冒险线：每镜 prompt（安全版：女主宽松家居服、蝴蝶女精灵少女聚焦冒险，规避敏感描述）
SHOTS = [
    {  # 镜1：初次观察（分镜图当首帧）
        "first": os.path.join(OUT_STORY, "shot1_final.jpg"),
        "prompt": ("奇幻微距摄影，微观冒险：一位人类年轻女生（约二十出头，穿宽松家居服）安静坐在书桌旁看书，"
                   "午后阳光从窗户洒在她身上，桌面有摊开的书本、暖光台灯、一杯热茶，她专注翻页神情放松；"
                   "前景书桌角落一盆绿植盆栽；在花盆的枝叶间隙中，藏着一位蝴蝶精灵少女（约3-4厘米，身穿轻盈纱裙，"
                   "背生晶莹的蓝色闪蝶翅膀，清纯可爱），她躲在叶片后偷偷注视着读书的女生，翅膀轻轻颤动，眼神好奇；"
                   "奇幻而温馨的微观世界，电影级写实布光，微距质感，完全写实不卡通，"
                   "音画同步：翻书声、翅膀轻颤、午后环境音"),
    },
    {  # 镜2：第一次靠近（飞上书页）
        "prompt": ("奇幻微距摄影，微观冒险：蝴蝶精灵少女（约3-4厘米，身穿轻盈纱裙，背生晶莹的蓝色闪蝶翅膀，清纯可爱）"
                   "从花盆的绿叶间悄悄飞出，轻盈落在书桌上一本翻开的书页边缘，她好奇地低头看着书页上的文字，"
                   "文字在她眼中如巨大的石雕，她用小手指轻轻触碰纸面，翅膀在阳光下闪着彩色光泽；"
                   "书桌上有一盏暖光台灯和一杯茶，背景是一位女生在安静看书（穿宽松家居服），她浑然不觉；"
                   "午后阳光洒入，光尘漂浮，奇幻而温馨的微观世界，电影级写实，8k质感，"
                   "音画同步：翅膀扇动声、纸张沙沙声"),
    },
    {  # 镜3：冒险行动（茶杯边喝水）
        "prompt": ("奇幻微距摄影，微观冒险：蝴蝶精灵少女（约3-4厘米，身穿轻盈纱裙，背生晶莹的蓝色闪蝶翅膀，清纯可爱）"
                   "从书页上飞起，悬停在书桌上一只白瓷茶杯边缘，双翅轻轻扇动，低头用小手捧起一滴茶水喝，"
                   "茶杯大如一座白色宫殿，杯沿如悬崖，水面如镜子映着她的倒影，热气袅袅；"
                   "她小巧的身影在巨大茶杯对比下显得勇敢又可爱；远处背景是女生安静看书的模糊侧影（穿宽松家居服）；"
                   "暖光台灯照亮，奇幻而温馨的微观世界，电影级写实，8k质感，"
                   "音画同步：水声、翅膀扇动、茶杯轻响"),
    },
    {  # 镜4：惊吓转折（女主翻页的手靠近）
        "prompt": ("奇幻微距摄影，微观冒险，紧张瞬间：蝴蝶精灵少女（约3-4厘米，身穿轻盈纱裙，背生晶莹的蓝色闪蝶翅膀，清纯可爱）"
                   "正在茶杯边喝水，突然一只巨大的手从画面外伸入翻动书页，手指如巨大的柱子，"
                   "翻页带起一阵风差点掀飞她，她惊得翅膀猛地张开，身体向后一缩，眼神惊讶；"
                   "巨大的手与渺小的蝴蝶精灵形成强烈对比，危险近在咫尺；"
                   "电影级写实布光，微距质感，紧张惊险氛围，完全写实不卡通，"
                   "音画同步：翻页巨响、翅膀急振、风声"),
    },
    {  # 镜5：逃离收尾（飞出窗外）
        "prompt": ("奇幻微距摄影，微观冒险，逃离收尾：蝴蝶精灵少女（约3-4厘米，身穿轻盈纱裙，背生晶莹的蓝色闪蝶翅膀，清纯可爱）"
                   "惊魂未定地从书桌上飞起，快速飞向窗户，她的身影穿过纱帘，窗外的阳光明亮耀眼，她在阳光中回望一眼"
                   "这间屋子——看书的女生依然浑然不觉；她转身飞出窗外，消失在明亮的阳光里，翅膀洒下一串光尘；"
                   "电影级写实布光，微距质感，自由与余韵氛围，完全写实不卡通，"
                   "音画同步：风声、翅膀扇动、窗外环境音"),
    },
]


def run_chain(start=1, end=5):
    os.makedirs(OUT_VIDEO, exist_ok=True)
    first = None
    for i in range(start, end + 1):
        shot = SHOTS[i - 1]
        print(f"\n===== 镜 {i}/5 =====")
        # 首帧：镜1用分镜图，其余用上一镜尾帧
        first_input = first if first else shot.get("first")
        if not first_input:
            print("⚠️ 无首帧，跳过")
            continue
        print(f"首帧: {os.path.basename(first_input)}")
        out_path = os.path.join(OUT_VIDEO, f"chain_shot{i}.mp4")
        # 创建任务（复用 gen_video 的 create_task，但手工传首帧）
        content = [{"type": "text", "text": shot["prompt"]}]
        if first_input.endswith((".png", ".jpg", ".jpeg")):
            content.append({
                "type": "image_url",
                "image_url": {"url": gv._read_asset(first_input)},
                "role": "first_frame",
            })
        body = {
            "model": gv.MODEL,
            "content": content,
            "generate_audio": True,
            "ratio": "16:9",
            "resolution": "480p",
            "duration": 5,
            "watermark": False,
            "return_last_frame": True,
        }
        headers = {"Authorization": f"Bearer {gv.API_KEY}", "Content-Type": "application/json"}
        resp = requests.post(gv.CREATE_URL, headers=headers, json=body, timeout=60)
        if resp.status_code != 200:
            print(f"❌ 创建失败 {resp.status_code}: {resp.text}")
            return
        task_id = resp.json().get("id")
        print(f"✅ 任务: {task_id}")
        data = gv.poll_task(task_id, interval=10, timeout=1800)
        # 下载视频 + 尾帧
        content_res = data.get("content", {})
        video_url = content_res.get("video_url")
        last_frame_url = content_res.get("last_frame_url")
        r = requests.get(video_url, timeout=120)
        with open(out_path, "wb") as f:
            f.write(r.content)
        print(f"✅ 视频: {out_path} ({len(r.content)/1024/1024:.1f}MB)")
        if last_frame_url:
            lf_path = os.path.join(OUT_VIDEO, f"chain_frame{i}.png")
            r2 = requests.get(last_frame_url, timeout=60)
            with open(lf_path, "wb") as f:
                f.write(r2.content)
            print(f"✅ 尾帧: {lf_path}")
            first = lf_path  # 下一镜用这个尾帧
        else:
            print("⚠️ 无尾帧返回")
    print("\n===== 链式生成完成 =====")


if __name__ == "__main__":
    start = 1
    end = 5
    args = sys.argv[1:]
    for a in args:
        if a.startswith("--start"):
            start = int(a.split("=")[1])
        elif a.startswith("--end"):
            end = int(a.split("=")[1])
    run_chain(start, end)
