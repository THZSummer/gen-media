#!/usr/bin/env python3
"""
蝴蝶女大冒险 v4 - 参考图独立并行生成

解决 v3 线性强依赖：每镜不依赖上一镜尾帧，直接用参考图库
（多图 reference_image）独立生成，10 镜可完全并行。

用法：
  python3 v4_parallel.py                 # 全部 10 镜（串行演示）
  python3 v4_parallel.py --parallel 3    # 并发 3 镜（后台线程）
  python3 v4_parallel.py --shot 1        # 只生成第 1 镜
"""
import json
import os
import sys
import time
import requests
import threading
import concurrent.futures as cf

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))
import importlib.util
spec = importlib.util.spec_from_file_location("gv", "scripts/gen_video.py")
gv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gv)

OUT = os.path.join(os.path.dirname(__file__), "out", "video")
REFS = os.path.join(os.path.dirname(__file__), "out", "refs")

R = lambda name: os.path.join(REFS, name)
B = "butterfly_front.jpg"
BS = "butterfly_side.jpg"
BB = "butterfly_back.jpg"
RD = "reader_noface.jpg"
SF = "sister_front.jpg"
SD = "scene_desk.jpg"
SD2 = "scene_door.jpg"
SW = "scene_window.jpg"

# 10 镜定义：每镜 = prompt + 参考图列表（全部 reference_image，无尾帧依赖）
SHOTS = [
    {  # 1 初次观察
        "refs": [B, RD, SD],
        "prompt": ("奇幻微距摄影，微观冒险，慵懒午后：参考@图像1的蝴蝶精灵少女形象、@图像2的读书女背影、@图像3的书桌场景。"
            "读书女（约二十出头，慵懒吊带背心配短裤，光脚，长发松散）坐在书桌旁安静看书，午后阳光洒在她身上，桌面有书本、暖光台灯、茶杯、绿植；"
            "前景书桌角落的绿植盆栽枝叶间隙中，藏着蝴蝶精灵少女（约3-4厘米，浅蓝纱裙，蓝色闪蝶翅膀），她躲在叶片后偷偷注视着读书女，翅膀轻轻颤动，眼神好奇；"
            "奇幻温馨的微观世界，电影级写实布光，微距质感，完全写实不卡通，音画同步：翻书声、翅膀轻颤、午后环境音"),
    },
    {  # 2 落上书页
        "refs": [B, RD, SD],
        "prompt": ("奇幻微距摄影，微观冒险：参考@图像1的蝴蝶精灵少女形象、@图像2的读书女背影、@图像3的书桌场景。"
            "蝴蝶精灵少女（约3-4厘米，浅蓝纱裙，蓝色闪蝶翅膀）从花盆绿叶间悄悄飞出，轻盈落在书桌上一本翻开的书页边缘，"
            "她好奇地低头看书页上的文字（文字如巨大石雕），小手指轻触纸面，翅膀在阳光下闪彩色光泽；"
            "书桌上有暖光台灯和一杯茶，背景是读书女在安静看书（背影），她浑然不觉；"
            "午后阳光洒入，光尘漂浮，奇幻温馨微观世界，电影级写实，8k质感，音画同步：翅膀扇动声、纸张沙沙声"),
    },
    {  # 3 茶杯喝水
        "refs": [B, RD, SD],
        "prompt": ("奇幻微距摄影，微观冒险：参考@图像1的蝴蝶精灵少女形象、@图像2的读书女背影、@图像3的书桌场景。"
            "蝴蝶精灵少女（约3-4厘米，浅蓝纱裙，蓝色闪蝶翅膀）悬停在书桌上一只白瓷茶杯边缘，双翅轻轻扇动，低头用小手捧起一滴茶水喝，"
            "茶杯大如白色宫殿，杯沿如悬崖，水面如镜子映着她的倒影，热气袅袅；她小巧的身影在巨大茶杯对比下显得勇敢又可爱；"
            "背景是读书女安静看书的背影（宽松家居服）；暖光台灯照亮，奇幻温馨微观世界，电影级写实，8k质感，音画同步：水声、翅膀扇动、茶杯轻响"),
    },
    {  # 4 翻页惊吓
        "refs": [B, RD, SD],
        "prompt": ("奇幻微距摄影，微观冒险，紧张瞬间：参考@图像1的蝴蝶精灵少女形象、@图像2的读书女背影、@图像3的书桌场景。"
            "蝴蝶精灵少女（约3-4厘米，浅蓝纱裙，蓝色闪蝶翅膀）正在茶杯边喝水，突然一只巨大的手从画面外伸入翻动书页，手指如巨大柱子，"
            "翻页带起一阵风差点掀飞她，她惊得翅膀猛地张开，身体向后一缩，眼神惊讶；巨大的手与渺小的蝴蝶精灵形成强烈对比，危险近在咫尺；"
            "电影级写实布光，微距质感，紧张惊险氛围，完全写实不卡通，音画同步：翻页巨响、翅膀急振、风声"),
    },
    {  # 5 飞出窗外
        "refs": [B, RD, SW],
        "prompt": ("奇幻微距摄影，微观冒险，逃离：参考@图像1的蝴蝶精灵少女形象、@图像2的读书女背影、@图像3的窗外场景。"
            "蝴蝶精灵少女（约3-4厘米，浅蓝纱裙，蓝色闪蝶翅膀）惊魂未定地从书桌上飞起，快速飞向窗户，她的身影穿过纱帘，"
            "窗外的阳光明亮耀眼，她在阳光中回望一眼这间屋子——看书的读书女依然浑然不觉；她转身飞出窗外，消失在明亮的阳光里，翅膀洒下一串光尘；"
            "电影级写实布光，微距质感，自由与余韵氛围，完全写实不卡通，音画同步：风声、翅膀扇动、窗外环境音"),
    },
    {  # 6 小妹妹追捕
        "refs": [B, SF, SD2],
        "prompt": ("奇幻微速摄影，微观冒险，追逐开始：参考@图像1的蝴蝶精灵少女形象、@图像2的小妹妹形象、@图像3的房间场景。"
            "蝴蝶精灵少女（约3-4厘米，浅蓝纱裙，蓝色闪蝶翅膀）刚飞到窗边，突然屋里一个活泼可爱的小女孩（约五六岁，扎双辫子，浅粉色家居服）"
            "兴奋地朝她跑来，伸出小手想抓她，脸上是好奇淘气的笑容；蝴蝶女吓得翅膀一颤，转身飞快逃回屋里，小女孩追在后面；"
            "午后阳光从窗户洒入，温馨家庭氛围中开始一场淘气追逐；电影级写实布光，微距质感，紧张又有趣的氛围，完全写实不卡通，"
            "音画同步：小跑脚步声、翅膀急振、小女孩笑声"),
    },
    {  # 7 书桌闪躲
        "refs": [B, SF, SD],
        "prompt": ("奇幻微距摄影，微观冒险，闪躲追逐：参考@图像1的蝴蝶精灵少女形象、@图像2的小妹妹形象、@图像3的书桌场景。"
            "蝴蝶精灵少女（约3-4厘米，浅蓝纱裙，蓝色闪蝶翅膀）在书桌上飞速闪躲，一只小女孩的胖乎乎小手从上方追过来想抓住她，手指如巨大柱子，"
            "她灵巧地左躲右闪，翅膀急促扇动，在书页、茶杯、台灯之间穿梭躲避；书桌上物品在她眼中都是巨大障碍物，她像敏捷的小蝴蝶在夹缝中穿梭；"
            "背景是午后阳光的书桌，淘气的小女孩追着她玩；电影级写实布光，微距质感，紧张又有趣的追逐氛围，完全写实不卡通，"
            "音画同步：急促翅膀扇动、小女孩笑声、物品轻响"),
    },
    {  # 8 寻求庇护
        "refs": [B, RD, SF],
        "prompt": ("奇幻微距摄影，微观冒险，寻求庇护：参考@图像1的蝴蝶精灵少女形象、@图像2的读书女背影、@图像3的小妹妹形象。"
            "蝴蝶精灵少女（约3-4厘米，浅蓝纱裙，蓝色闪蝶翅膀）被小女孩追得无路可逃，慌乱中飞向坐在书桌旁看书的读书女，"
            "在她肩头、发梢、翻开的书页之间围绕着她灵巧闪躲，像一只寻求保护的小蝴蝶；小女孩的手追到读书女身边停下，不敢太靠近姐姐，撅着嘴看着；"
            "读书女微微抬头，看到蝴蝶精灵落在她的书页上，眼神温柔；午后阳光，温馨氛围，电影级写实布光，微距质感，完全写实不卡通，"
            "音画同步：翅膀扇动、小女孩嘟囔、女生轻声惊讶"),
    },
    {  # 9 被保护
        "refs": [B, RD, SF],
        "prompt": ("奇幻微距摄影，微观冒险，被保护：参考@图像1的蝴蝶精灵少女形象、@图像2的读书女背影、@图像3的小妹妹形象。"
            "蝴蝶精灵少女（约3-4厘米，浅蓝纱裙，蓝色闪蝶翅膀）落在读书女摊开的书本上，翅膀轻轻收拢，安心地站在书页中央，抬起头看向读书女；"
            "读书女温柔地低头看着她，用手掌轻轻护在书页上方，像保护一只珍贵的小蝴蝶，嘴角带着温柔笑意；旁边小女孩（约五六岁）趴在桌边，撅着嘴眼巴巴看着，姐姐不让抓；"
            "午后阳光洒在书页上，蝴蝶女的身影在光里闪闪发光，温馨治愈；电影级写实布光，微距质感，温暖治愈氛围，完全写实不卡通，"
            "音画同步：轻柔翅膀扇动、女生温柔笑声、小女孩嘟囔"),
    },
    {  # 10 温馨收尾
        "refs": [B, RD, SF],
        "prompt": ("奇幻微距摄影，微观冒险，温馨收尾：参考@图像1的蝴蝶精灵少女形象、@图像2的读书女背影、@图像3的小妹妹形象。"
            "蝴蝶精灵少女（约3-4厘米，浅蓝纱裙，蓝色闪蝶翅膀）安心地站在读书女的书页上，翅膀微微舒展，闪着细碎光尘；"
            "读书女低头温柔地看着她，轻轻合拢书本露出一条缝，为她遮挡午后直射光线；小女孩（约五六岁）趴在桌边好奇又羡慕地看着，读书女轻轻摸了摸她的头；"
            "阳光透过纱帘洒下柔和光晕，蝴蝶女在光影中扇动翅膀，画面温馨治愈；电影级写实布光，微距质感，温暖治愈收尾，完全写实不卡通，"
            "音画同步：轻柔翅膀扇动、温馨背景音乐、柔和翻书声"),
    },
]


def gen_shot(i, timeout=1800):
    """生成单镜（独立，无依赖），返回 (i, ok, msg)"""
    shot = SHOTS[i - 1]
    out_path = os.path.join(OUT, f"v4_shot{i}.mp4")
    content = [{"type": "text", "text": shot["prompt"]}]
    for k, name in enumerate(shot["refs"], 1):
        content.append({
            "type": "image_url",
            "image_url": {"url": gv._read_asset(R(name))},
            "role": "reference_image",
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
    try:
        resp = requests.post(gv.CREATE_URL, headers=headers, json=body, timeout=60)
        if resp.status_code != 200:
            return (i, False, f"create {resp.status_code}: {resp.text[:200]}")
        tid = resp.json().get("id")
        print(f"  镜{i} 任务: {tid}", flush=True)
        data = gv.poll_task(tid, interval=10, timeout=timeout)
        c = data.get("content", {})
        r = requests.get(c.get("video_url"), timeout=120)
        with open(out_path, "wb") as f:
            f.write(r.content)
        if c.get("last_frame_url"):
            r2 = requests.get(c["last_frame_url"], timeout=60)
            with open(os.path.join(OUT, f"v4_frame{i}.png"), "wb") as f:
                f.write(r2.content)
        return (i, True, f"saved {out_path}")
    except Exception as e:
        return (i, False, f"error: {e}")


def run_parallel(shots, workers=3):
    os.makedirs(OUT, exist_ok=True)
    print(f"并行生成 {len(shots)} 镜，并发 {workers}...")
    results = {}
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(gen_shot, i): i for i in shots}
        for fut in cf.as_completed(futures):
            i, ok, msg = fut.result()
            results[i] = (ok, msg)
            print(f"✅ 镜{i}: {'成功' if ok else '失败'} - {msg}", flush=True)
    ok_n = sum(1 for v in results.values() if v[0])
    print(f"\n完成 {ok_n}/{len(shots)} 镜")
    for i in sorted(results):
        if not results[i][0]:
            print(f"  ❌ 镜{i}: {results[i][1]}")


if __name__ == "__main__":
    workers = 3
    shots = list(range(1, 11))
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--parallel":
            workers = int(args[i + 1]); i += 2
        elif args[i] == "--shot":
            shots = [int(x) for x in args[i + 1].split(",")]; i += 2
        else:
            i += 1
    run_parallel(shots, workers)
