@echo off
REM Video2Txt Web 应用启动脚本 (Windows)

echo ========================================
echo    Video2Txt Web 应用启动脚本
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到 Python
    echo 请先安装 Python: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✓ Python 已安装

REM 检查并安装 Flask
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Flask 未安装，正在安装...
    pip install flask
)

REM 检查并安装 Whisper
python -c "import whisper" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Whisper 未安装，正在安装...
    pip install openai-whisper
)

echo.
echo ✓ 所有依赖已就绪
echo.
echo ========================================
echo   启动 Web 服务器...
echo ========================================
echo.

REM 启动应用
cd app
python app.py

pause
