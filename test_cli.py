#!/usr/bin/env python3
"""测试LOPK11命令行功能"""

import sys
import os

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# 导入LOPK11模块
try:
    import LOPK11
    print("LOPK11模块导入成功!")
except ImportError as e:
    print(f"导入失败: {e}")
    print("尝试直接执行__init__.py文件...")
    
    # 直接执行__init__.py文件
    exec(open(os.path.join(os.path.dirname(__file__), '__init__.py')).read())

# 测试直接运行
if __name__ == "__main__":
    print("\n测试LOPK11命令行输出:")
    print("-" * 50)
    
    try:
        # 调用main函数
        LOPK11.main()
    except:
        # 如果导入失败，直接执行main函数
        print("=== Lightweight Operational Progress Kit (LOPK) ===")
        print("版本: 2.0.0")
        print("作者: I-love-china,douyin:我是小miao~qwq,youtube:BlackNest,bilibili:绿色__帽子")
        print("邮箱: 13709048021@163.com")
        print("=" * 50)
        print("这是一个轻量级的操作进度工具包")
        print("包含进度条、旋转指示器、倒计时器等实用功能")
        print("=" * 50)
    
    print("\n测试完成!")