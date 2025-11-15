# 🎬 Video2Txt - 视频音频转文本工具

一个基于 OpenAI Whisper 的完整解决方案，提供 Web 界面和命令行工具。

## ⚡ 快速开始

### 1. 启动 Web 应用

```bash
./start.sh
```

### 2. 打开浏览器

```
http://localhost:5000
```

### 3. 拖拽视频/音频文件，点击转换！

就这么简单！ 🎉

---

## ✨ 主要特性

- 🎯 **拖拽上传** - 支持拖拽文件到浏览器
- 🎬 **多格式支持** - MP4, AVI, MOV, MP3, WAV 等
- 🧠 **三种模型** - Small/Medium/Large 可选
- 📊 **实时进度** - 可视化转写进度
- 💾 **一键下载** - 直接下载文本文件
- 🎨 **美观界面** - 现代化紫色渐变设计

---

## 📋 完整功能列表

### Web 应用
- ✅ 可视化界面
- ✅ 拖拽上传
- ✅ 实时进度显示
- ✅ 在线预览结果
- ✅ 一键下载

### 命令行工具
- ✅ 单文件转写
- ✅ 批量处理
- ✅ 多种输出格式（TXT/SRT/VTT/JSON）

---

## 📁 支持的格式

### 视频
MP4, AVI, MOV, MKV, FLV, WMV, M4V, WEBM

### 音频
MP3, WAV, FLAC, M4A, AAC, OGG, WMA

---

## 🎯 使用场景

- 📝 视频字幕生成
- 🎤 采访录音整理
- 🎓 讲座笔记转写
- 💼 会议记录归档
- 🎙️ 播客内容转录

---

## 📖 文档指南

| 文档 | 说明 |
|------|------|
| [HOW_TO_USE.md](HOW_TO_USE.md) | 📘 **推荐新手阅读** - 详细使用教程 |
| [QUICK_START.md](QUICK_START.md) | ⚡ 一分钟快速上手 |
| [WEB_APP_GUIDE.md](WEB_APP_GUIDE.md) | 📖 Web 应用完整指南 |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | 📊 项目功能总结 |

---

## 🔧 技术栈

- **后端**: Flask + OpenAI Whisper
- **前端**: HTML5 + CSS3 + JavaScript
- **AI 引擎**: Whisper (Small/Medium/Large)

---

## 📦 安装依赖

```bash
pip3 install -r requirements.txt
```

主要依赖：
- openai-whisper
- flask
- torch
- ffmpeg

---

## 🚀 三种使用方式

### 方式 1: Web 应用（推荐）

```bash
./start.sh
# 访问 http://localhost:5000
```

### 方式 2: 命令行单文件

```bash
python3 video2txt.py video.mp4 medium txt zh
```

### 方式 3: 批量处理

```bash
# 将视频放入 videos 文件夹
python3 batch_transcribe.py
```

---

## ⚙️ 模型选择

| 模型 | 大小 | 速度 | 准确率 | 推荐场景 |
|------|------|------|--------|----------|
| Small | ~500MB | ⚡⚡⚡ | ⭐⭐⭐ | 快速测试 |
| Medium | ~1.5GB | ⚡⚡ | ⭐⭐⭐⭐ | **日常推荐** |
| Large | ~3GB | ⚡ | ⭐⭐⭐⭐⭐ | 专业需求 |

---

## 🎨 界面预览

Web 应用提供：
- 现代化渐变设计
- 响应式布局
- 实时进度条
- 错误提示
- 结果预览

---

## 🔐 安全特性

- ✅ 文件类型验证
- ✅ 大小限制（500MB）
- ✅ 临时文件清理
- ✅ 安全文件名处理

---

## ❓ 常见问题

### Q: 首次使用很慢？
A: 首次会下载模型文件，之后就快了。

### Q: 如何提高准确率？
A: 使用 Large 模型，确保音频清晰。

### Q: 支持其他语言吗？
A: 支持！编辑配置文件改为 English, Japanese 等。

更多问题请查看 [HOW_TO_USE.md](HOW_TO_USE.md)

---

## 📂 项目结构

```
video2txt/
├── app/                  # Web 应用
│   ├── app.py           # Flask 后端
│   └── templates/       # HTML 模板
├── start.sh             # 启动脚本
├── video2txt.py         # 单文件 CLI
├── batch_transcribe.py  # 批量 CLI
└── 各种文档.md          # 详细文档
```

---

## 🎓 适用人群

- 内容创作者
- 学生和研究者
- 记者和编辑
- 企业用户
- 个人用户

---

## 📝 许可证

基于 OpenAI Whisper，供学习和个人使用。

---

## 🎉 立即开始

```bash
./start.sh
```

访问：http://localhost:5000

**享受 AI 驱动的转写体验！** 🚀

---

**Star ⭐ 这个项目如果你觉得有用！**
