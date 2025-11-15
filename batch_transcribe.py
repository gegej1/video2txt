#!/usr/bin/env python3
"""
批量视频转文本工具
使用 OpenAI Whisper 将视频文件批量转换为文本
"""

import whisper
import os
import sys

def batch_transcribe(video_dir="./videos", output_dir="./whisper_output", model_name="medium", language="Chinese"):
    """
    批量转写视频文件

    参数:
        video_dir: 视频文件夹路径（默认: ./videos）
        output_dir: 输出文件夹路径（默认: ./whisper_output）
        model_name: Whisper 模型名称（可选: tiny, base, small, medium, large）
        language: 语言（默认: Chinese）
    """
    print(f"正在加载 Whisper 模型: {model_name}")
    print("首次运行会下载模型文件，请耐心等待...")

    model = whisper.load_model(model_name)

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 支持的视频格式
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.m4v', '.webm')

    # 检查视频目录是否存在
    if not os.path.exists(video_dir):
        print(f"错误: 视频目录 '{video_dir}' 不存在")
        print(f"请创建目录并将视频文件放入其中")
        return

    # 获取所有视频文件
    video_files = [f for f in os.listdir(video_dir)
                   if f.lower().endswith(video_extensions)]

    if not video_files:
        print(f"在 '{video_dir}' 目录中未找到视频文件")
        print(f"支持的格式: {', '.join(video_extensions)}")
        return

    print(f"\n找到 {len(video_files)} 个视频文件")
    print("-" * 60)

    # 批量处理
    for i, file in enumerate(video_files, 1):
        print(f"\n[{i}/{len(video_files)}] 正在处理: {file}")

        video_path = os.path.join(video_dir, file)

        try:
            # 转写
            result = model.transcribe(video_path, language=language)

            # 保存文本
            base_name = os.path.splitext(file)[0]
            txt_path = os.path.join(output_dir, f"{base_name}.txt")

            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(result["text"])

            print(f"✓ 完成! 输出文件: {txt_path}")
            print(f"  文本长度: {len(result['text'])} 字符")

        except Exception as e:
            print(f"✗ 处理失败: {str(e)}")
            continue

    print("\n" + "=" * 60)
    print("批量转写完成!")
    print(f"输出目录: {output_dir}")


if __name__ == "__main__":
    # 可以通过命令行参数自定义配置
    if len(sys.argv) > 1:
        # 使用命令行参数
        video_dir = sys.argv[1] if len(sys.argv) > 1 else "./videos"
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "./whisper_output"
        model_name = sys.argv[3] if len(sys.argv) > 3 else "medium"
        language = sys.argv[4] if len(sys.argv) > 4 else "Chinese"
    else:
        # 使用默认配置
        video_dir = "./videos"
        output_dir = "./whisper_output"
        model_name = "medium"  # 可选: tiny, base, small, medium, large
        language = "Chinese"   # 中文

    batch_transcribe(video_dir, output_dir, model_name, language)
