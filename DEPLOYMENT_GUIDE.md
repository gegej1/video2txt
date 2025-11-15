# 🚀 Video2Txt 云端部署指南

## 📋 部署方案对比

由于 Video2Txt 需要运行大型 AI 模型和处理长时间任务，**不适合部署到 Vercel 等 Serverless 平台**。

### ❌ 为什么不能用 Vercel？

| 限制 | 说明 | 影响 |
|------|------|------|
| **执行时间限制** | 免费版 10 秒，付费版 60 秒 | ❌ 转写需要几分钟到几十分钟 |
| **文件存储** | 无持久化存储 | ❌ 上传的视频和结果会丢失 |
| **模型大小** | 无法存储大文件 | ❌ Whisper 模型 1-3GB |
| **计算资源** | CPU/内存有限 | ❌ Whisper 需要大量资源 |

### ✅ 推荐的部署方案

---

## 方案 1: 云服务器部署（推荐 ⭐⭐⭐⭐⭐）

**适合场景**：长期使用，完全控制，成本可控

### 1.1 选择云服务商

| 服务商 | 优点 | 价格参考 | 推荐配置 |
|--------|------|---------|----------|
| **阿里云 ECS** | 国内快，稳定 | ¥60-100/月 | 2核4GB |
| **腾讯云 CVM** | 国内快，价格优 | ¥50-90/月 | 2核4GB |
| **Vultr** | 国际稳定 | $12-24/月 | 2核4GB |
| **DigitalOcean** | 简单易用 | $12-24/月 | 2核4GB |
| **AWS EC2** | 功能强大 | $15-30/月 | t3.medium |

**推荐配置**：
- **CPU**: 2 核或以上
- **内存**: 4GB 或以上（Medium 模型需要）
- **硬盘**: 40GB SSD（存储模型和临时文件）
- **带宽**: 5Mbps+

### 1.2 部署步骤

#### Step 1: 购买服务器

以阿里云为例：
1. 访问 https://ecs.aliyun.com
2. 选择"按量付费"或"包年包月"
3. 配置选择：Ubuntu 22.04，2核4GB
4. 设置安全组：开放 5000 端口

#### Step 2: 连接服务器

```bash
# macOS/Linux
ssh root@your_server_ip

# Windows 使用 PuTTY 或 Windows Terminal
```

#### Step 3: 安装环境

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python 3 和 pip
sudo apt install python3 python3-pip -y

# 安装 FFmpeg
sudo apt install ffmpeg -y

# 安装 Git
sudo apt install git -y
```

#### Step 4: 上传代码

**方法 A - Git 克隆**（如果有 Git 仓库）
```bash
git clone https://github.com/yourusername/video2txt.git
cd video2txt
```

**方法 B - 直接上传**
```bash
# 在本地打包
tar -czf video2txt.tar.gz video2txt/

# 上传到服务器
scp video2txt.tar.gz root@your_server_ip:/root/

# 在服务器解压
ssh root@your_server_ip
tar -xzf video2txt.tar.gz
cd video2txt
```

#### Step 5: 安装依赖

```bash
pip3 install -r requirements.txt
```

#### Step 6: 配置防火墙

```bash
# 开放 5000 端口
sudo ufw allow 5000
sudo ufw enable
```

#### Step 7: 使用 Supervisor 守护进程

```bash
# 安装 Supervisor
sudo apt install supervisor -y

# 创建配置文件
sudo nano /etc/supervisor/conf.d/video2txt.conf
```

添加以下内容：

```ini
[program:video2txt]
directory=/root/video2txt/app
command=python3 app.py
autostart=true
autorestart=true
stderr_logfile=/var/log/video2txt.err.log
stdout_logfile=/var/log/video2txt.out.log
user=root
```

启动服务：

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start video2txt
```

#### Step 8: 配置 Nginx 反向代理（可选）

```bash
# 安装 Nginx
sudo apt install nginx -y

# 创建配置
sudo nano /etc/nginx/sites-available/video2txt
```

添加配置：

```nginx
server {
    listen 80;
    server_name your_domain.com;  # 替换为你的域名

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # 增加上传大小限制
        client_max_body_size 500M;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/video2txt /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 9: 配置 HTTPS（推荐）

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 自动配置 SSL
sudo certbot --nginx -d your_domain.com
```

#### Step 10: 访问应用

```
http://your_server_ip:5000
# 或使用域名
http://your_domain.com
```

---

## 方案 2: Docker 容器部署（推荐 ⭐⭐⭐⭐）

**适合场景**：快速部署，环境隔离，易于迁移

### 2.1 创建 Dockerfile

```dockerfile
FROM python:3.12-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 5000

# 启动应用
CMD ["python", "app/app.py"]
```

### 2.2 创建 docker-compose.yml

```yaml
version: '3.8'

services:
  video2txt:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
      - ./outputs:/app/outputs
      - ~/.cache/whisper:/root/.cache/whisper
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```

### 2.3 部署步骤

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

---

## 方案 3: Railway 一键部署（推荐 ⭐⭐⭐⭐）

**适合场景**：快速上线，简单易用，自动化部署

### 3.1 Railway 优势

- ✅ 支持长时间运行任务
- ✅ 自动 HTTPS
- ✅ 免费额度（每月 $5 信用）
- ✅ GitHub 自动部署
- ✅ 持久化存储

### 3.2 部署步骤

1. 访问 https://railway.app
2. 使用 GitHub 登录
3. 点击"New Project" → "Deploy from GitHub repo"
4. 选择你的仓库
5. Railway 自动检测并部署

### 3.3 配置环境变量

在 Railway 项目设置中添加：

```
PORT=5000
```

---

## 方案 4: Render 部署（推荐 ⭐⭐⭐）

**适合场景**：免费试用，简单部署

### 4.1 Render 优势

- ✅ 免费层可用
- ✅ 自动 HTTPS
- ✅ GitHub 自动部署

### 4.2 部署步骤

1. 访问 https://render.com
2. 创建新的 "Web Service"
3. 连接 GitHub 仓库
4. 配置：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app/app.py`
5. 点击部署

---

## 方案 5: 本地 + 内网穿透（临时方案 ⭐⭐）

**适合场景**：临时分享，快速演示

### 5.1 使用 ngrok

```bash
# 安装 ngrok
brew install ngrok  # macOS
# 或访问 https://ngrok.com/download

# 启动应用
./start.sh

# 另开终端，启动 ngrok
ngrok http 5000
```

会得到一个公网地址：
```
https://xxxx-xx-xx-xx-xx.ngrok.io
```

### 5.2 使用 Cloudflare Tunnel

```bash
# 安装 cloudflared
brew install cloudflare/cloudflare/cloudflared

# 启动隧道
cloudflared tunnel --url http://localhost:5000
```

---

## 📊 方案对比总结

| 方案 | 成本 | 难度 | 速度 | 稳定性 | 推荐度 |
|------|------|------|------|--------|--------|
| 云服务器 | ¥50-100/月 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Docker | ¥50-100/月 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Railway | $5-20/月 | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Render | 免费-$7/月 | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 内网穿透 | 免费 | ⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ |

---

## 🎯 个人推荐

### 预算充足（推荐）
**阿里云/腾讯云 + Docker**
- 性能最佳
- 完全可控
- 国内访问快

### 预算有限
**Railway 或 Render**
- 简单易用
- 自动化部署
- 有免费额度

### 临时演示
**本地 + ngrok**
- 零成本
- 快速分享

---

## ⚠️ 重要提示

1. **不要**部署到 Vercel、Netlify、GitHub Pages 等静态托管平台
2. **不要**部署到 AWS Lambda、Google Cloud Functions 等 Serverless 平台
3. **需要**有持久化存储和长时间运行能力的平台
4. **建议**使用反向代理（Nginx）提升安全性
5. **推荐**配置 HTTPS 保护数据传输

---

## 📞 获取帮助

- 云服务器配置问题：查看服务商文档
- Docker 部署问题：检查日志 `docker-compose logs`
- 网络访问问题：检查防火墙和安全组设置

---

**选择适合你的方案，开始部署吧！** 🚀
