#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LOPK 1.2 基于tkinter的进度条简单测试脚本
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk
import time

# 简单的tkinter进度条测试
def simple_tk_test():
    """简单测试，直接在主线程中创建和更新进度条"""
    print("=== 简单tkinter进度条测试 ===")
    
    try:
        # 创建tkinter窗口
        root = tk.Tk()
        root.title("简单进度条测试")
        root.geometry("400x100")
        root.attributes("-topmost", True)
        
        # 创建进度条
        progress_var = tk.DoubleVar(value=0)
        progress_bar = ttk.Progressbar(
            root, 
            variable=progress_var, 
            maximum=100, 
            length=350,
            mode="determinate"
        )
        progress_bar.pack(pady=20)
        
        # 创建标签
        label = ttk.Label(root, text="进度: 0%")
        label.pack()
        
        # 更新进度条的函数
        def update_progress():
            for i in range(101):
                progress_var.set(i)
                label.config(text=f"进度: {i:.1f}%")
                root.update()  # 立即更新窗口
                time.sleep(0.05)
            root.after(1000, root.destroy)  # 1秒后关闭窗口
        
        # 启动更新
        root.after(100, update_progress)
        
        # 运行主循环
        root.mainloop()
        
        print("简单测试通过!")
        return True
    except Exception as e:
        print(f"简单测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

# 测试LOPK的TkProgressBar
def lopk_tk_test():
    """测试LOPK的TkProgressBar类"""
    print("\n=== LOPK TkProgressBar测试 ===")
    
    try:
        from lopk import TkProgressBar
        
        # 创建进度条
        tk_bar = TkProgressBar(100, title="LOPK进度条测试", prefix="测试进度")
        
        # 更新进度
        for i in range(101):
            tk_bar.update(i)
            time.sleep(0.02)
        
        # 运行主循环
        tk_bar.show()
        
        print("LOPK测试通过!")
        return True
    except Exception as e:
        print(f"LOPK测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("开始tkinter进度条测试...")
    print("=" * 50)
    
    simple_tk_test()
    lopk_tk_test()
    
    print("=" * 50)
    print("测试结束!")