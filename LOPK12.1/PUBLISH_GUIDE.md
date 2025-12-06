# LOPK11 PyPI 发布指南

## 准备工作

### 1. 安装必要的工具
```bash
pip install twine setuptools wheel
```

### 2. 注册PyPI账号
- 访问 [PyPI官网](https://pypi.org/) 注册账号
- 访问 [TestPyPI官网](https://test.pypi.org/) 注册测试账号

### 3. 创建API令牌
- 登录PyPI → Account Settings → API tokens → Add API token
- 设置权限范围（建议选择整个账户）
- 复制生成的token（只会显示一次）

## 发布流程

### 第一步：测试打包
```bash
cd LOPK11
python setup.py sdist bdist_wheel
```

这会生成两个目录：
- `dist/` - 包含打包文件
- `build/` - 临时构建文件

### 第二步：检查打包文件
```bash
# 检查打包文件内容
tree dist/

# 验证打包文件
twine check dist/*
```

### 第三步：测试发布到TestPyPI
```bash
# 发布到测试服务器
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# 测试安装
pip install --index-url https://test.pypi.org/simple/ lopk
```

### 第四步：正式发布到PyPI
```bash
# 正式发布
twine upload dist/*

# 验证安装
pip install lopk
```

## 详细命令示例

### Windows PowerShell
```powershell
# 进入项目目录
cd "c:\Users\DELL\Desktop\Lightweight-Operational-Progress-Kit\LOPK11"

# 清理之前的构建
Remove-Item -Recurse -Force build, dist, *.egg-info -ErrorAction SilentlyContinue

# 打包
python setup.py sdist bdist_wheel

# 检查打包文件
Get-ChildItem dist/
twine check dist/*

# 测试发布（需要TestPyPI token）
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "你的TestPyPI_token"
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# 正式发布（需要PyPI token）
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "你的PyPI_token"
twine upload dist/*
```

### 环境变量配置（推荐）
创建 `.pypirc` 文件在用户目录：
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = 你的PyPI_token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = 你的TestPyPI_token
```

然后可以使用简化命令：
```bash
twine upload --repository testpypi dist/*  # 测试发布
twine upload dist/*  # 正式发布
```

## 验证发布成功

### 1. 检查PyPI页面
访问：https://pypi.org/project/lopk/

### 2. 测试安装
```bash
# 创建虚拟环境测试
python -m venv test_env
test_env\Scripts\activate  # Windows
pip install lopk

# 测试功能
python -c "import LOPK11; LOPK11.main()"
lopk-info
lopk-demo
```

### 3. 测试导入和使用
```python
import LOPK11
print(LOPK11.__version__)
print(LOPK11.__author__)

# 测试进度条
from LOPK11 import ProgressBar
bar = ProgressBar(100, "测试")
for i in range(101):
    bar.update(i)
```

## 常见问题解决

### 1. 包名冲突
如果 `lopk` 名称已被占用，需要修改 `setup.py` 中的 `name`：
```python
name = "lopk-china"  # 或其他唯一名称
```

### 2. 版本冲突
每次发布需要更新版本号，修改 `__init__.py`：
```python
__version__ = "2.0.1"  # 递增版本号
```

### 3. 依赖问题
确保所有依赖在 `install_requires` 中正确声明。

### 4. 权限错误
确保API token有正确的权限。

## 更新版本流程

1. 更新 `LOPK11/__init__.py` 中的版本号
2. 更新 `README.md` 中的版本信息
3. 重新打包：`python setup.py sdist bdist_wheel`
4. 发布新版本：`twine upload dist/*`

## 最佳实践

- ✅ 每次发布前先在TestPyPI测试
- ✅ 使用虚拟环境测试安装
- ✅ 保持版本号语义化（major.minor.patch）
- ✅ 更新CHANGELOG.md记录变更
- ✅ 为重要版本创建git tag

## 联系方式

- 作者: I-love-china
- 邮箱: 13709048021@163.com
- 项目: https://github.com/I-love-china/lopk

---

**祝发布顺利！** 🚀