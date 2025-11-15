#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频转文本工具
使用 OpenAI Whisper 将视频文件转换为文本
"""

import whisper
import sys
import os
from pathlib import Path


def transcribe_video(video_path, model_size="base", output_format="txt", language=None):
    """
    将视频文件转换为文本
    
    参数:
        video_path: 视频文件路径
        model_size: Whisper 模型大小 (tiny, base, small, medium, large)
        output_format: 输出格式 (txt, srt, vtt, tsv, json)
        language: 语言代码 (如 'zh', 'en')，None 表示自动检测
    """
    # 检查文件是否存在
    if not os.path.exists(video_path):
        print(f"错误: 文件不存在: {video_path}")
        return None
    
    print(f"正在加载 Whisper 模型: {model_size}...")
    model = whisper.load_model(model_size)
    
    print(f"正在转录视频: {video_path}...")
    result = model.transcribe(video_path, language=language)
    
    # 生成输出文件名
    video_name = Path(video_path).stem
    output_path = f"{video_name}.{output_format}"
    
    # 根据格式保存结果
    if output_format == "txt":
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result["text"])
    elif output_format == "srt":
        # 生成 SRT 字幕文件
        with open(output_path, "w", encoding="utf-8") as f:
            for i, segment in enumerate(result["segments"], 1):
                start = format_time(segment["start"])
                end = format_time(segment["end"])
                f.write(f"{i}\n{start} --> {end}\n{segment['text']}\n\n")
    elif output_format == "vtt":
        # 生成 VTT 字幕文件
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")
            for segment in result["segments"]:
                start = format_time_vtt(segment["start"])
                end = format_time_vtt(segment["end"])
                f.write(f"{start} --> {end}\n{segment['text']}\n\n")
    elif output_format == "json":
        import json
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    else:
        print(f"不支持的输出格式: {output_format}")
        return None
    
    print(f"转录完成！输出文件: {output_path}")
    print(f"检测到的语言: {result.get('language', '未知')}")
    
    return output_path


def format_time(seconds):
    """将秒数转换为 SRT 格式时间 (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def format_time_vtt(seconds):
    """将秒数转换为 VTT 格式时间 (HH:MM:SS.mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python video2txt.py <视频文件路径> [模型大小] [输出格式] [语言]")
        print("\n参数说明:")
        print("  视频文件路径: 要转换的视频文件")
        print("  模型大小: tiny, base, small, medium, large (默认: base)")
        print("  输出格式: txt, srt, vtt, json (默认: txt)")
        print("  语言: 语言代码，如 'zh' 中文, 'en' 英文 (默认: 自动检测)")
        print("\n示例:")
        print("  python video2txt.py video.mp4")
        print("  python video2txt.py video.mp4 base txt zh")
        print("  python video2txt.py video.mp4 large srt")
        sys.exit(1)
    
    video_path = sys.argv[1]
    model_size = sys.argv[2] if len(sys.argv) > 2 else "base"
    output_format = sys.argv[3] if len(sys.argv) > 3 else "txt"
    language = sys.argv[4] if len(sys.argv) > 4 else None
    
    transcribe_video(video_path, model_size, output_format, language)


if __name__ == "__main__":
    main()

