#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video2Txt Web Application
视频转文本 Web 应用 - 后端服务
"""

import os
import sys
from faster_whisper import WhisperModel
import uuid
import json
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import threading

# 应用启动路径日志（符合 CLAUDE.md 规范）
print('cwd=', os.getcwd(), 'dirname=', os.path.dirname(__file__))

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB 最大文件大小
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'uploads')
app.config['OUTPUT_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'outputs')

# 确保目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# 支持的文件格式
ALLOWED_EXTENSIONS = {
    'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv', 'm4v', 'webm',  # 视频
    'mp3', 'wav', 'flac', 'm4a', 'aac', 'ogg', 'wma'  # 音频
}

# 任务状态管理
tasks = {}


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """处理文件上传"""
    if 'file' not in request.files:
        return jsonify({'error': '没有文件被上传'}), 400

    file = request.files['file']
    model_size = request.form.get('model', 'medium')
    language = request.form.get('language', 'zh')

    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': '不支持的文件格式'}), 400

    # 生成唯一任务ID
    task_id = str(uuid.uuid4())

    # 保存上传的文件
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{task_id}_{filename}")
    file.save(file_path)

    # 创建任务记录
    tasks[task_id] = {
        'status': 'pending',
        'filename': filename,
        'model': model_size,
        'language': language,
        'progress': 0,
        'file_path': file_path,
        'output_path': None,
        'error': None
    }

    # 启动后台转写任务
    thread = threading.Thread(target=transcribe_task, args=(task_id,))
    thread.daemon = True
    thread.start()

    return jsonify({
        'task_id': task_id,
        'message': '文件上传成功，开始转写...'
    })


def transcribe_task(task_id):
    """后台执行转写任务"""
    try:
        task = tasks[task_id]
        task['status'] = 'processing'
        task['progress'] = 10

        # 加载模型（使用 Faster-Whisper）
        print(f"[任务 {task_id}] 加载 Faster-Whisper 模型: {task['model']}")
        model = WhisperModel(
            task['model'],
            device="cpu",
            compute_type="int8"  # 使用 int8 量化，速度更快
        )
        task['progress'] = 30

        # 执行转写
        print(f"[任务 {task_id}] 开始转写: {task['filename']}, 语言: {task['language']}")

        # 处理语言参数：如果是 'auto'，则不指定语言让模型自动检测
        language_param = task['language'] if task['language'] != 'auto' else None

        segments, info = model.transcribe(
            task['file_path'],
            language=language_param,
            beam_size=5,
            vad_filter=True  # 语音活动检测，跳过静音
        )
        task['progress'] = 50

        # 收集所有文本片段
        print(f"[任务 {task_id}] 收集转写结果...")
        full_text = []
        for segment in segments:
            full_text.append(segment.text.strip())

        result_text = "".join(full_text)
        task['progress'] = 80

        # 保存结果
        base_name = Path(task['filename']).stem
        output_filename = f"{task_id}_{base_name}.txt"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result_text)

        task['output_path'] = output_path
        task['output_filename'] = output_filename
        task['text'] = result_text
        task['status'] = 'completed'
        task['progress'] = 100

        print(f"[任务 {task_id}] 转写完成")

        # 清理上传的文件
        try:
            os.remove(task['file_path'])
        except:
            pass

    except Exception as e:
        print(f"[任务 {task_id}] 错误: {str(e)}")
        task['status'] = 'failed'
        task['error'] = str(e)

        # 清理文件
        try:
            os.remove(task['file_path'])
        except:
            pass


@app.route('/api/status/<task_id>')
def get_status(task_id):
    """获取任务状态"""
    if task_id not in tasks:
        return jsonify({'error': '任务不存在'}), 404

    task = tasks[task_id]
    return jsonify({
        'status': task['status'],
        'progress': task['progress'],
        'filename': task['filename'],
        'error': task.get('error'),
        'text': task.get('text') if task['status'] == 'completed' else None
    })


@app.route('/api/download/<task_id>')
def download_file(task_id):
    """下载转写结果"""
    if task_id not in tasks:
        return jsonify({'error': '任务不存在'}), 404

    task = tasks[task_id]

    if task['status'] != 'completed':
        return jsonify({'error': '任务未完成'}), 400

    return send_file(
        task['output_path'],
        as_attachment=True,
        download_name=task['output_filename']
    )


@app.route('/api/models')
def get_models():
    """获取可用模型列表"""
    return jsonify({
        'models': [
            {'value': 'small', 'name': 'Small (快速，准确率一般)', 'size': '~500MB'},
            {'value': 'medium', 'name': 'Medium (推荐，准确率高)', 'size': '~1.5GB'},
            {'value': 'large', 'name': 'Large (最慢，准确率最高)', 'size': '~3GB'}
        ],
        'default': 'medium'
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Video2Txt Web 应用正在启动...")
    print("="*60)
    print(f"上传目录: {app.config['UPLOAD_FOLDER']}")
    print(f"输出目录: {app.config['OUTPUT_FOLDER']}")
    print("\n请在浏览器中打开: http://localhost:5003")
    print("按 Ctrl+C 停止服务")
    print("="*60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5003, threaded=True)
