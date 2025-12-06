#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试LOPK 1.2 基于tkinter的进度条演示函数
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lopk import demo_tk

if __name__ == "__main__":
    demo_tk()