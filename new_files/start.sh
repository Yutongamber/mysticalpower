#!/bin/bash
# 易经占卜系统 - 启动脚本

echo "🔮 易经占卜系统 - 启动脚本"
echo "================================"
echo

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3"
    exit 1
fi

# 检查是否在正确的目录
if [ ! -f "backend.py" ]; then
    echo "❌ 错误: 未找到 backend.py，请在项目根目录运行此脚本"
    exit 1
fi

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📦 安装依赖..."
pip install -q -r requirements.txt

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "📝 创建 .env 文件..."
    cp .env.example .env
fi

echo
echo "✅ 准备就绪！"
echo
echo "启动后端服务，请运行："
echo "  source venv/bin/activate"
echo "  python backend.py"
echo
echo "或者直接运行："
echo "  ./venv/bin/python backend.py"
echo
echo "然后在浏览器中打开 index_v3.html"
echo
