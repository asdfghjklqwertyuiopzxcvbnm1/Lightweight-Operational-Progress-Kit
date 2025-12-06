#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LOPK 1.2 测试脚本
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 直接从本地模块导入
from lopk import (
    ProgressBar,
    Spinner,
    CountdownTimer,
    MultiProgressBar,
    colored_text,
    format_file_size,
    format_time
)

import time

def test_progress_bar():
    """测试进度条功能"""
    print("\n=== 测试进度条 ===")
    bar = ProgressBar(100, "测试进度", color="cyan", show_eta=True)
    for i in range(101):
        bar.update(i)
        time.sleep(0.02)

def test_spinner():
    """测试旋转指示器功能"""
    print("\n=== 测试旋转指示器 ===")
    with Spinner("正在处理数据"):
        time.sleep(2)
    print("处理完成!")

def test_multi_progress_bar():
    """测试多进度条功能"""
    print("\n=== 测试多进度条 ===")
    multi_bar = MultiProgressBar()
    
    # 添加两个进度条
    bar1 = multi_bar.add_bar(50, "进度条1", color="green")
    bar2 = multi_bar.add_bar(75, "进度条2", color="blue")
    
    # 更新进度条
    for i in range(51):
        if i <= 75:
            multi_bar.update(bar2, i)
        multi_bar.update(bar1, i)
        time.sleep(0.05)
    
    # 完成所有进度条
    multi_bar.finish_all()

def test_new_functions():
    """测试新增的工具函数"""
    print("\n=== 测试新增工具函数 ===")
    
    # 测试format_file_size
    print(f"文件大小格式化: 1024 bytes = {format_file_size(1024)}")
    print(f"文件大小格式化: 1048576 bytes = {format_file_size(1048576)}")
    print(f"文件大小格式化: 1073741824 bytes = {format_file_size(1073741824)}")
    
    # 测试format_time
    print(f"时间格式化: 5 seconds = {format_time(5)}")
    print(f"时间格式化: 65 seconds = {format_time(65)}")
    print(f"时间格式化: 3665 seconds = {format_time(3665)}")
    
    # 测试colored_text
    print(colored_text("彩色文本测试", "red"))
    print(colored_text("彩色文本测试", "green"))
    print(colored_text("彩色文本测试", "blue"))

def test_countdown():
    """测试倒计时器功能"""
    print("\n=== 测试倒计时器 ===")
    timer = CountdownTimer(3, "准备开始")
    timer.start()
    print("开始!")

if __name__ == "__main__":
    print("LOPK 1.2 功能测试")
    print("=" * 50)
    
    try:
        test_progress_bar()
        test_spinner()
        test_multi_progress_bar()
        test_new_functions()
        test_countdown()
        
        print("\n" + "=" * 50)
        print("所有测试通过! LOPK 1.2 功能正常。")
    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)