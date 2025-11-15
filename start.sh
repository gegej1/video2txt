#!/bin/bash
# Video2Txt Web 应用启动脚本

echo "========================================"
echo "   Video2Txt Web 应用启动脚本"
echo "========================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    echo "请先安装 Python 3: https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Python 版本: $(python3 --version)"

# 检查 Flask
if ! python3 -c "import flask" 2>/dev/null; then
    echo ""
    echo "⚠️  Flask 未安装，正在安装..."
    pip3 install flask
fi

# 检查 Whisper
if ! python3 -c "import whisper" 2>/dev/null; then
    echo ""
    echo "⚠️  Whisper 未安装，正在安装..."
    pip3 install openai-whisper
fi

echo ""
echo "✓ 所有依赖已就绪"
echo ""
echo "========================================"
echo "  启动 Web 服务器..."
echo "========================================"
echo ""

# 启动应用
cd app
python3 app.py
