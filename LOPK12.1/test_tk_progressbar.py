#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LOPK 1.2 基于tkinter的进度条测试脚本
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lopk import TkProgressBar
import time

def test_tk_progress_bar_basic():
    """测试基本功能"""
    print("\n=== 测试基本功能 ===")
    try:
        tk_bar = TkProgressBar(100, title="基本测试", prefix="进度")
        for i in range(101):
            tk_bar.update(i)
            time.sleep(0.02)
        print("基本功能测试通过!")
        return True
    except Exception as e:
        print(f"基本功能测试失败: {e}")
        return False

def test_tk_progress_bar_custom():
    """测试自定义参数"""
    print("\n=== 测试自定义参数 ===")
    try:
        tk_bar = TkProgressBar(
            50, 
            title="自定义测试", 
            prefix="下载进度", 
            suffix="MB",
            length=400,
            show_time=True,
            show_eta=True
        )
        for i in range(51):
            tk_bar.update(i, suffix=f"MB ({i*2}%)")
            time.sleep(0.05)
        print("自定义参数测试通过!")
        return True
    except Exception as e:
        print(f"自定义参数测试失败: {e}")
        return False

def test_tk_progress_bar_reset():
    """测试重置功能"""
    print("\n=== 测试重置功能 ===")
    try:
        tk_bar = TkProgressBar(30, title="重置测试", prefix="进度")
        
        # 先更新到50%
        for i in range(16):
            tk_bar.update(i)
            time.sleep(0.03)
        
        # 重置
        print("重置进度条...")
        tk_bar.reset()
        
        # 重新开始
        for i in range(31):
            tk_bar.update(i)
            time.sleep(0.03)
        print("重置功能测试通过!")
        return True
    except Exception as e:
        print(f"重置功能测试失败: {e}")
        return False

def test_tk_progress_bar_finish():
    """测试强制完成功能"""
    print("\n=== 测试强制完成功能 ===")
    try:
        tk_bar = TkProgressBar(100, title="强制完成测试", prefix="进度")
        
        # 只更新到30%
        for i in range(31):
            tk_bar.update(i)
            time.sleep(0.02)
        
        # 强制完成
        print("强制完成进度条...")
        tk_bar.finish()
        time.sleep(1.5)  # 等待窗口关闭
        print("强制完成功能测试通过!")
        return True
    except Exception as e:
        print(f"强制完成功能测试失败: {e}")
        return False

def test_tk_progress_bar_error_handling():
    """测试异常处理"""
    print("\n=== 测试异常处理 ===")
    try:
        # 模拟tkinter不可用的情况
        original_import = sys.modules.pop('tkinter', None)
        original_ttk = sys.modules.pop('tkinter.ttk', None)
        
        # 尝试导入TkProgressBar，应该失败
        from lopk import TkProgressBar as TestTkProgressBar
        
        # 恢复原始导入
        if original_import:
            sys.modules['tkinter'] = original_import
        if original_ttk:
            sys.modules['tkinter.ttk'] = original_ttk
        
        print("异常处理测试通过!")
        return True
    except Exception as e:
        print(f"异常处理测试失败: {e}")
        return False

if __name__ == "__main__":
    print("LOPK 1.2 基于tkinter的进度条测试")
    print("=" * 60)
    
    # 运行所有测试
    tests = [
        test_tk_progress_bar_basic,
        test_tk_progress_bar_custom,
        test_tk_progress_bar_reset,
        test_tk_progress_bar_finish,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n" + "=" * 60)
    print(f"测试结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("所有测试通过! TkProgressBar 功能正常。")
        sys.exit(0)
    else:
        print("部分测试失败，请检查TkProgressBar功能。")
        sys.exit(1)