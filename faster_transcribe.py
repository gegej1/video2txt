#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Faster-Whisper 快速转写工具
速度比原版 Whisper 快 4-5 倍！
"""

import sys
import os
from pathlib import Path

def check_and_install():
    """检查并安装 faster-whisper"""
    try:
        from faster_whisper import WhisperModel
        print("✓ faster-whisper 已安装")
        return True
    except ImportError:
        print("正在安装 faster-whisper...")
        os.system("pip3 install faster-whisper")
        print("✓ 安装完成！")
        return True

def transcribe_fast(video_path, model_size="medium", language="zh"):
    """
    使用 Faster-Whisper 快速转写

    参数:
        video_path: 视频文件路径
        model_size: 模型大小 (tiny, base, small, medium, large-v2)
        language: 语言 (zh=中文, en=英文)
    """
    from faster_whisper import WhisperModel

    print(f"正在加载模型: {model_size}")
    print("首次使用会下载模型，请稍候...")

    # 初始化模型（使用 CPU）
    model = WhisperModel(
        model_size,
        device="cpu",
        compute_type="int8"  # 使用 int8 量化，速度更快
    )

    print(f"\n开始转写: {video_path}")
    print("=" * 60)

    # 转写
    segments, info = model.transcribe(
        video_path,
        language=language,
        beam_size=5,
        vad_filter=True,  # 启用语音活动检测，跳过静音部分
    )

    print(f"检测到语言: {info.language} (概率: {info.language_probability:.2f})")
    print(f"预计时长: {info.duration:.2f} 秒")
    print("\n正在转写中...")

    # 收集结果
    full_text = []
    for i, segment in enumerate(segments, 1):
        text = segment.text.strip()
        full_text.append(text)
        print(f"[{i}] {segment.start:.2f}s -> {segment.end:.2f}s: {text}")

    # 保存结果
    base_name = Path(video_path).stem
    output_path = f"{base_name}_fast.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(full_text))

    print("\n" + "=" * 60)
    print(f"✓ 转写完成！")
    print(f"✓ 保存到: {output_path}")
    print(f"✓ 总字数: {len(''.join(full_text))} 字符")

    return output_path


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 faster_transcribe.py <视频文件> [模型大小] [语言]")
        print("\n示例:")
        print("  python3 faster_transcribe.py video.mp4")
        print("  python3 faster_transcribe.py video.mp4 small zh")
        print("\n模型大小: tiny, base, small, medium, large-v2")
        print("语言: zh(中文), en(英文)")
        sys.exit(1)

    # 检查并安装依赖
    check_and_install()

    video_path = sys.argv[1]
    model_size = sys.argv[2] if len(sys.argv) > 2 else "medium"
    language = sys.argv[3] if len(sys.argv) > 3 else "zh"

    if not os.path.exists(video_path):
        print(f"错误: 文件不存在: {video_path}")
        sys.exit(1)

    transcribe_fast(video_path, model_size, language)


if __name__ == "__main__":
    main()
