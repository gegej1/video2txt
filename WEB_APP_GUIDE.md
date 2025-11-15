# Video2Txt Web 应用使用指南

## 📖 简介

Video2Txt Web 应用是一个基于 OpenAI Whisper 的可视化视频/音频转文本工具。通过友好的 Web 界面，您可以轻松地将视频或音频文件转换为文本，无需手动运行命令行。

### ✨ 主要特性

- 🎯 **拖拽上传** - 支持拖拽文件到浏览器窗口
- 🎬 **多格式支持** - 支持 MP4, AVI, MOV, MP3, WAV 等常见格式
- 🧠 **模型可选** - 提供 Small/Medium/Large 三种模型选择
- 📊 **实时进度** - 显示转写进度和状态
- 💾 **一键下载** - 完成后直接下载文本文件
- 🎨 **美观界面** - 现代化设计，操作简单直观

---

## 🚀 快速开始

### 1. 安装依赖

确保已安装以下组件（如果之前已安装 Whisper，可跳过）：

```bash
# 安装所有依赖
pip3 install -r requirements.txt

# 或单独安装
pip3 install flask openai-whisper
```

### 2. 启动应用

#### macOS / Linux

```bash
# 方法 1: 使用启动脚本（推荐）
./start.sh

# 方法 2: 手动启动
cd app
python3 app.py
```

#### Windows

```bash
# 方法 1: 双击运行
start.bat

# 方法 2: 手动启动
cd app
python app.py
```

### 3. 访问应用

启动成功后，在浏览器中打开：

```
http://localhost:5000
```

---

## 📱 使用方法

### 步骤 1: 上传文件

有两种方式上传文件：

1. **拖拽上传**：将视频/音频文件拖拽到上传区域
2. **点击上传**：点击上传区域，在弹出的文件选择器中选择文件

### 步骤 2: 选择模型

根据您的需求选择合适的模型：

| 模型 | 大小 | 速度 | 准确率 | 推荐场景 |
|------|------|------|--------|----------|
| **Small** | ~500MB | 快速 | 一般 | 快速处理，要求不高 |
| **Medium** | ~1.5GB | 中等 | 高 | ⭐ **推荐日常使用** |
| **Large** | ~3GB | 较慢 | 最高 | 专业需求，追求最高准确率 |

> 💡 **提示**：首次使用某个模型时，系统会自动下载模型文件，请耐心等待。

### 步骤 3: 开始转换

点击"开始转换"按钮，系统将：

1. 上传文件到服务器
2. 加载选定的 Whisper 模型
3. 执行语音识别转写
4. 显示实时进度

### 步骤 4: 查看和下载结果

转写完成后：

- 📄 **在线查看**：结果直接显示在页面上
- 💾 **下载文件**：点击"下载文本"按钮保存为 `.txt` 文件
- 🔄 **继续转换**：点击"转换新文件"处理更多文件

---

## 📁 项目结构

```
video2txt/
├── app/
│   ├── app.py              # Flask 后端服务
│   ├── templates/
│   │   └── index.html      # Web 前端界面
│   └── static/             # 静态资源（如需要）
├── uploads/                # 临时上传文件夹
├── outputs/                # 转写结果输出文件夹
├── start.sh                # macOS/Linux 启动脚本
├── start.bat               # Windows 启动脚本
├── requirements.txt        # Python 依赖列表
└── WEB_APP_GUIDE.md       # 本使用指南
```

---

## 🎯 支持的文件格式

### 视频格式
- `.mp4` - MP4 视频
- `.avi` - AVI 视频
- `.mov` - QuickTime 视频
- `.mkv` - Matroska 视频
- `.flv` - Flash 视频
- `.wmv` - Windows Media 视频
- `.m4v` - iTunes 视频
- `.webm` - WebM 视频

### 音频格式
- `.mp3` - MP3 音频
- `.wav` - WAV 音频
- `.flac` - FLAC 无损音频
- `.m4a` - M4A 音频
- `.aac` - AAC 音频
- `.ogg` - OGG 音频
- `.wma` - Windows Media 音频

---

## ⚙️ 技术架构

### 后端
- **Flask** - Python Web 框架
- **OpenAI Whisper** - 语音识别引擎
- **多线程处理** - 后台异步转写，不阻塞界面

### 前端
- **原生 HTML5/CSS3/JavaScript** - 无需额外框架
- **拖拽 API** - 支持文件拖拽上传
- **AJAX 轮询** - 实时获取转写进度
- **响应式设计** - 适配各种屏幕尺寸

### API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 主页界面 |
| `/api/upload` | POST | 上传文件并启动转写任务 |
| `/api/status/<task_id>` | GET | 查询任务进度和状态 |
| `/api/download/<task_id>` | GET | 下载转写结果 |
| `/api/models` | GET | 获取可用模型列表 |

---

## 🔧 常见问题

### 1. 启动时提示"Flask 未安装"

```bash
pip3 install flask
```

### 2. 首次使用模型时很慢

首次使用会下载模型文件（存储在 `~/.cache/whisper/`），下载完成后就会很快。

### 3. 文件上传失败

- 检查文件大小是否超过 500MB（如需修改，编辑 `app/app.py` 中的 `MAX_CONTENT_LENGTH`）
- 确认文件格式是否支持
- 检查磁盘空间是否充足

### 4. 转写准确率不高

- 尝试使用更大的模型（如 Large）
- 确保音频清晰，背景噪音较少
- 如果是其他语言，修改 [app/app.py:129](app/app.py#L129) 中的 `language='Chinese'`

### 5. 端口 5000 被占用

编辑 [app/app.py:190](app/app.py#L190)，修改端口号：

```python
app.run(debug=True, host='0.0.0.0', port=8000, threaded=True)
```

### 6. 如何在局域网其他设备访问

确保：
1. 服务器启动时使用 `host='0.0.0.0'`（默认已配置）
2. 查看本机 IP 地址（如 `192.168.1.100`）
3. 在其他设备浏览器访问：`http://192.168.1.100:5000`

---

## 🎨 自定义配置

### 修改默认语言

编辑 [app/app.py:129](app/app.py#L129)：

```python
result = model.transcribe(
    task['file_path'],
    language='English',  # 改为其他语言：English, Japanese, Korean 等
    verbose=False
)
```

### 修改最大文件大小

编辑 [app/app.py:17](app/app.py#L17)：

```python
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024  # 修改为 1GB
```

### 添加更多模型选项

编辑 [app/app.py:174-180](app/app.py#L174-L180)，添加更多模型：

```python
'models': [
    {'value': 'tiny', 'name': 'Tiny (最快)', 'size': '~75MB'},
    {'value': 'base', 'name': 'Base (平衡)', 'size': '~150MB'},
    {'value': 'small', 'name': 'Small (快速)', 'size': '~500MB'},
    {'value': 'medium', 'name': 'Medium (推荐)', 'size': '~1.5GB'},
    {'value': 'large', 'name': 'Large (最佳)', 'size': '~3GB'}
]
```

---

## 🔒 安全建议

- 本应用默认绑定到 `0.0.0.0:5000`，允许局域网访问
- 如果部署到公网，建议：
  - 添加用户认证
  - 使用 HTTPS
  - 限制文件大小和类型
  - 添加请求频率限制

---

## 🤝 反馈与支持

如有问题或建议，请：

1. 检查本指南的"常见问题"部分
2. 查看控制台输出的错误信息
3. 提交 Issue 或联系开发者

---

## 📄 许可证

本项目基于 OpenAI Whisper 开发，仅供学习和个人使用。

---

**享受使用 Video2Txt Web 应用！** 🎉
