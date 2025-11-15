# Video2Txt - 视频转文本工具

使用 OpenAI Whisper 将视频文件转换为文本的工具。

## 🌟 新功能：Web 应用界面

现在提供了友好的 Web 界面，支持拖拽上传、实时进度显示、一键下载！

### 快速启动 Web 应用

```bash
# macOS/Linux
./start.sh

# Windows
start.bat
```

然后在浏览器打开：http://localhost:5000

📖 详细使用指南请查看：[WEB_APP_GUIDE.md](WEB_APP_GUIDE.md)

---

## 安装

### 1. 安装依赖

```bash
pip3 install -r requirements.txt
```

或者直接安装 Whisper：

```bash
pip3 install openai-whisper
```

### 2. 安装 FFmpeg（必需）

Whisper 需要 FFmpeg 来处理视频文件。

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install ffmpeg
```

**Windows:**
下载并安装 [FFmpeg](https://ffmpeg.org/download.html)，确保添加到 PATH。

## 使用方法

### 命令行使用

```bash
python3 video2txt.py <视频文件路径> [模型大小] [输出格式] [语言]
```

**参数说明：**
- `视频文件路径`: 要转换的视频文件（必需）
- `模型大小`: `tiny`, `base`, `small`, `medium`, `large`（默认: `base`）
  - `tiny`: 最快，准确度较低
  - `base`: 平衡速度和准确度（推荐）
  - `small`: 更好的准确度
  - `medium`: 高准确度
  - `large`: 最高准确度，但最慢
- `输出格式`: `txt`, `srt`, `vtt`, `json`（默认: `txt`）
- `语言`: 语言代码，如 `zh`（中文）、`en`（英文），留空则自动检测

### 使用示例

```bash
# 基本使用（自动检测语言，输出 txt 文件）
python3 video2txt.py video.mp4

# 指定中文，使用 base 模型
python3 video2txt.py video.mp4 base txt zh

# 生成字幕文件（SRT 格式）
python3 video2txt.py video.mp4 base srt

# 使用大模型获得最高准确度
python3 video2txt.py video.mp4 large txt zh

# 生成 JSON 格式（包含时间戳等详细信息）
python3 video2txt.py video.mp4 base json
```

### Python 代码中使用

```python
import whisper

# 加载模型
model = whisper.load_model("base")

# 转录视频
result = model.transcribe("video.mp4", language="zh")

# 获取文本
print(result["text"])

# 获取分段信息（带时间戳）
for segment in result["segments"]:
    print(f"[{segment['start']:.2f}s -> {segment['end']:.2f}s] {segment['text']}")
```

## 模型说明

首次使用某个模型时，Whisper 会自动下载模型文件。模型文件会保存在 `~/.cache/whisper/` 目录下。

- **tiny**: ~39 MB，最快，适合快速测试
- **base**: ~74 MB，推荐用于大多数场景
- **small**: ~244 MB，更好的准确度
- **medium**: ~769 MB，高准确度
- **large**: ~1550 MB，最高准确度

## 输出格式

- **txt**: 纯文本文件，只包含转录的文本
- **srt**: 字幕文件，包含时间戳，可用于视频播放器
- **vtt**: WebVTT 格式字幕文件
- **json**: JSON 格式，包含完整信息（文本、时间戳、置信度等）

## 注意事项

1. 首次运行会下载模型文件，需要网络连接
2. 处理大视频文件可能需要较长时间
3. 使用 `large` 模型需要更多内存和计算资源
4. 确保视频文件格式被 FFmpeg 支持（MP4, AVI, MOV 等常见格式都可以）

## 故障排除

### 如果遇到 "ffmpeg not found" 错误

确保已安装 FFmpeg 并添加到系统 PATH 中。

### 如果内存不足

尝试使用较小的模型（如 `tiny` 或 `base`）。

### 如果处理速度慢

- 使用较小的模型
- 确保使用 GPU（如果可用）
- 考虑将视频转换为较小的分辨率

