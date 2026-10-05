#!/usr/bin/env python3
"""轮次驱动入口（动物拼接项目）。

用法：
  python3 run_round.py 6                                  # 默认子主题 cat-eagle
  python3 run_round.py --subject dragon-nines 1            # 指定子主题
  python3 run_round.py 6 --dry                             # 打印逐字 prompt，不出图
  python3 run_round.py --subject dragon-nines --prompts     # 重生成 prompt 存档
  python3 run_round.py --help

结构：
  runkit 逻辑都在 `roundkit.py`（跑轮 / 存档 / 分句换行）
  每个子主题的 prompt 与 ROUNDS 在 `subjects/<子主题>/rounds.py`
  探索产物写到 `work/rN/`（**不进仓库**），成品由 `curate.py` 提升到
  `subjects/<子主题>/period-NN/`，并由 `score.py` 打分复核。
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roundkit import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
