# LOPK.py
import os
import sys
import time

print("由I-love-china制作")
"""
由I-love-china制作
2025/89/19
"""

class ProgressBar:
    def __init__(self, total, prefix='', suffix='', length=50, fill='█', print_end="\r"):
        """
        初始化进度条
        :param total: 总进度
        :param prefix: 前缀字符串
        :param suffix: 后缀字符串
        :param length: 进度条长度
        :param fill: 进度条填充字符
        :param print_end: 每次打印结束的字符
        """
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.fill = fill
        self.print_end = print_end
        self.progress = 0

    def update(self, progress=None):
        """
        更新进度条
        :param progress: 当前进度，如果为None，则自动加1
        """
        if progress is not None:
            self.progress = progress
        else:
            self.progress += 1

        percent = ("{0:.1f}").format(100 * (self.progress / float(self.total)))
        filled_length = int(self.length * self.progress // self.total)
        bar = self.fill * filled_length + '-' * (self.length - filled_length)
        print(f'\r{self.prefix} |{bar}| {percent}% {self.progress}/{self.total} {self.suffix}', end=self.print_end)

        if self.progress == self.total:
            print()

    def reset(self):
        """
        重置进度条
        """
        self.progress = 0

def AK():
    input("按下回车继续")
def cls():
    if os.name == "nt":
        os.system("cls")
    else:

        os.system("clear")
