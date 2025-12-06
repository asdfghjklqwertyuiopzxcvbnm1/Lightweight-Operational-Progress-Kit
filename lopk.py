"""
Lightweight Operational Progress Kit (LOPK) v3.0
高级进度条和终端操作工具包

Features:
- 彩色进度条
- 旋转指示器
- 多进度条管理
- 倒计时器
- 终端工具函数
- 跨平台支持
- ETA（预计剩余时间）
- 性能优化

Author: I-love-china
Version: 3.0.0
"""

import os
import sys
import time
import threading
from typing import Optional, Union, List, Callable

# 检查是否支持彩色输出
try:
    import colorama
    colorama.init()
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False

# 全局颜色映射，避免重复创建
COLORS = {
    'green': '\033[92m',
    'blue': '\033[94m', 
    'red': '\033[91m',
    'yellow': '\033[93m',
    'cyan': '\033[96m',
    'magenta': '\033[95m',
    'reset': '\033[0m'
}

class ProgressBar:
    """高级进度条类"""
    
    def __init__(self, total: int, prefix: str = '', suffix: str = '', 
                 length: int = 50, fill: str = '█', print_end: str = "\r",
                 color: str = 'green', show_time: bool = True, show_eta: bool = True):
        """
        初始化进度条
        
        Args:
            total: 总进度
            prefix: 前缀字符串
            suffix: 后缀字符串  
            length: 进度条长度
            fill: 进度条填充字符
            print_end: 每次打印结束的字符
            color: 进度条颜色 (green, blue, red, yellow, cyan, magenta)
            show_time: 是否显示耗时
            show_eta: 是否显示预计剩余时间
        """
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.fill = fill
        self.print_end = print_end
        self.color = color
        self.show_time = show_time
        self.show_eta = show_eta
        self.progress = 0
        self.start_time = time.time()
        self.last_update = 0
        self.last_progress = -1
        # 缓存颜色代码
        self.color_code = COLORS.get(color, '') if HAS_COLORAMA else ''
        self.reset_code = COLORS['reset'] if HAS_COLORAMA else ''

    def update(self, progress: Optional[int] = None, suffix: Optional[str] = None):
        """
        更新进度条
        
        Args:
            progress: 当前进度，如果为None则自动加1
            suffix: 临时后缀，如果提供则覆盖原后缀
        """
        if progress is not None:
            self.progress = progress
        else:
            self.progress += 1

        # 限制进度范围
        self.progress = min(max(self.progress, 0), self.total)
        
        # 只有当进度变化或超过0.1秒时才更新，减少终端IO
        current_time = time.time()
        if self.progress == self.last_progress and (current_time - self.last_update) < 0.1:
            return
        self.last_progress = self.progress
        self.last_update = current_time
        
        # 计算百分比和填充长度
        percent = ("{0:.1f}").format(100 * (self.progress / float(self.total)))
        filled_length = int(self.length * self.progress // self.total)
        bar = self.fill * filled_length + '-' * (self.length - filled_length)
        
        # 计算耗时和ETA
        elapsed_time = current_time - self.start_time
        time_str = f" [{elapsed_time:.1f}s]" if self.show_time else ""
        
        # 计算ETA
        eta_str = ""
        if self.show_eta and self.progress > 0:
            eta = (elapsed_time / self.progress) * (self.total - self.progress)
            eta_str = f" [ETA: {eta:.1f}s]" if eta > 0 else " [ETA: 0.0s]"
        
        # 使用临时后缀或原后缀
        current_suffix = suffix if suffix is not None else self.suffix
        
        # 构建输出字符串
        output = f'\r{self.prefix} |{self.color_code}{bar}{self.reset_code}| {percent}% {self.progress}/{self.total} {current_suffix}{time_str}{eta_str}'
        print(output, end=self.print_end)
        sys.stdout.flush()

        # 完成时换行
        if self.progress == self.total:
            print()

    def reset(self):
        """重置进度条"""
        self.progress = 0
        self.start_time = time.time()
        self.last_update = 0
        self.last_progress = -1

    def finish(self):
        """强制完成进度条"""
        self.progress = self.total
        self.update()
        self.last_progress = -1


class Spinner:
    """旋转指示器类"""
    
    # 静态变量，避免重复创建
    _spinner_chars = ['|', '/', '-', '\\']
    
    def __init__(self, message: str = "处理中...", delay: float = 0.1):
        self.message = message
        self.delay = delay
        self.running = False
        self.thread = None
        # 缓存消息长度
        self.msg_length = len(message) + 2

    def _spin(self):
        """旋转动画线程"""
        i = 0
        chars = self._spinner_chars
        msg = self.message
        while self.running:
            sys.stdout.write(f'\r{msg} {chars[i]}')
            sys.stdout.flush()
            i = (i + 1) % len(chars)
            time.sleep(self.delay)

    def start(self):
        """开始旋转"""
        self.running = True
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()

    def stop(self):
        """停止旋转"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=0.1)  # 添加超时，避免阻塞
        # 使用缓存的消息长度，减少计算
        sys.stdout.write('\r' + ' ' * self.msg_length + '\r')
        sys.stdout.flush()

    def __enter__(self):
        """上下文管理器入口"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.stop()


class CountdownTimer:
    """倒计时器类"""
    
    def __init__(self, seconds: int, message: str = "倒计时"):
        self.seconds = seconds
        self.message = message
        self.remaining = seconds

    def start(self):
        """开始倒计时"""
        for i in range(self.seconds, 0, -1):
            self.remaining = i
            sys.stdout.write(f'\r{self.message}: {i:2d}秒')
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write('\r' + ' ' * 20 + '\r')
        sys.stdout.flush()

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        pass


class MultiProgressBar:
    """多进度条管理器"""
    
    def __init__(self):
        self.bars = []
        self.lock = threading.Lock()
        self.initialized = False

    def add_bar(self, total: int, prefix: str = '', **kwargs):
        """添加进度条"""
        bar = ProgressBar(total, prefix, **kwargs)
        self.bars.append(bar)
        return len(self.bars) - 1

    def update(self, bar_index: int, progress: Optional[int] = None):
        """更新指定进度条"""
        with self.lock:
            if 0 <= bar_index < len(self.bars):
                # 简化实现，避免复杂的光标移动
                # 清空当前输出并重新打印所有进度条
                # 这种方式在进度条数量不多时更可靠
                sys.stdout.write('\033[F' * len(self.bars))  # 上移n行
                sys.stdout.flush()
                
                for i, bar in enumerate(self.bars):
                    if i == bar_index:
                        bar.update(progress)
                    else:
                        # 直接打印其他进度条，不更新
                        current_time = time.time()
                        elapsed_time = current_time - bar.start_time
                        percent = ("{0:.1f}").format(100 * (bar.progress / float(bar.total)))
                        filled_length = int(bar.length * bar.progress // bar.total)
                        bar_str = bar.fill * filled_length + '-' * (bar.length - filled_length)
                        time_str = f" [{elapsed_time:.1f}s]" if bar.show_time else ""
                        eta_str = ""
                        if bar.show_eta and bar.progress > 0:
                            eta = (elapsed_time / bar.progress) * (bar.total - bar.progress)
                            eta_str = f" [ETA: {eta:.1f}s]" if eta > 0 else " [ETA: 0.0s]"
                        output = f'\r{bar.prefix} |{bar.color_code}{bar_str}{bar.reset_code}| {percent}% {bar.progress}/{bar.total} {bar.suffix}{time_str}{eta_str}'
                        print(output)
                sys.stdout.flush()

    def finish_all(self):
        """完成所有进度条"""
        for bar in self.bars:
            bar.finish()


# 工具函数
def AK():
    """等待用户按下回车继续"""
    input("按下回车继续...")


def cls():
    """清屏函数（跨平台）"""
    os.system("cls" if os.name == "nt" else "clear")


def clear_line():
    """清除当前行"""
    sys.stdout.write('\r' + ' ' * 100 + '\r')
    sys.stdout.flush()


def get_terminal_size() -> tuple:
    """获取终端尺寸"""
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except:
        return 80, 24


def colored_text(text: str, color: str) -> str:
    """彩色文本输出"""
    # 使用全局COLORS字典，避免重复创建
    if HAS_COLORAMA and color in COLORS:
        return f"{COLORS[color]}{text}{COLORS['reset']}"
    return text


def format_file_size(size_bytes: int) -> str:
    """格式化文件大小为人类可读格式"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def format_time(seconds: float) -> str:
    """格式化时间为人类可读格式"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes)}m {int(seconds)}s"
    else:
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"


# 演示函数
def demo():
    """演示函数"""
    print("=== LOPK v2.0 演示 ===")
    
    # 演示进度条
    print("\n1. 彩色进度条演示:")
    bar = ProgressBar(100, "下载", color="cyan", show_time=True)
    for i in range(101):
        bar.update(i)
        time.sleep(0.02)
    
    # 演示旋转指示器
    print("\n2. 旋转指示器演示:")
    with Spinner("正在处理数据"):
        time.sleep(3)
    print("处理完成!")
    
    # 演示倒计时
    print("\n3. 倒计时演示:")
    with CountdownTimer(5, "准备开始"):
        pass
    print("开始!")
    
    print("\n演示完成!")


if __name__ == "__main__":
    demo()
    AK()