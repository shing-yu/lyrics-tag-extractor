import os
import eyed3
from mutagen.flac import FLAC
import locale


def extract_lyrics(mp3_file):
    try:
        audio = eyed3.load(mp3_file)
        if audio.tag:
            return audio.tag.lyrics[0].text
        else:
            return None
    except Exception as e:
        if is_chinese:
            print(f"从 {mp3_file} 中提取歌词时出错: {e}")
        else:
            print(f"Error while extracting lyrics from {mp3_file}: {e}")
        return None


def extract_flac_lyrics(flac_file):
    try:
        audio = FLAC(flac_file)
        if 'lyrics' in audio:
            return audio['lyrics'][0]
        else:
            return None
    except Exception as e:
        if is_chinese:
            print(f"从 {flac_file} 中提取歌词时出错: {e}")
        else:
            print(f"Error while extracting lyrics from {flac_file}: {e}")
        return None


def write_lrc_file(audio_file, lyrics):
    lrc_file = os.path.splitext(audio_file)[0] + ".lrc"
    try:
        with open(lrc_file, "w", encoding="utf-8") as f:
            f.write(lyrics)
        if is_chinese:
            print(f"写入 LRC 文件成功: {lrc_file}")
        else:
            print(f"Successfully wrote LRC file: {lrc_file}")
    except Exception as e:
        if is_chinese:
            print(f"写入 LRC 文件 {lrc_file} 时出错: {e}")
        else:
            print(f"Error while writing LRC file {lrc_file}: {e}")


def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".mp3"):
                audio_file = os.path.join(root, file)
                lrc_file = os.path.splitext(audio_file)[0] + ".lrc"
                if os.path.exists(lrc_file):
                    if is_chinese:
                        print(f"已存在同名的 LRC 文件，跳过: {lrc_file}")
                    else:
                        print(f"Already exists a LRC file with the same name, skipping: {lrc_file}")
                    continue
                lyrics = extract_lyrics(audio_file)
                if lyrics:
                    write_lrc_file(audio_file, lyrics)
                else:
                    if is_chinese:
                        print(f"无法提取歌词，跳过文件: {audio_file}")
                    else:
                        print(f"Cannot extract lyrics, skipping file: {audio_file}")
            elif file.lower().endswith(".flac"):
                audio_file = os.path.join(root, file)
                lrc_file = os.path.splitext(audio_file)[0] + ".lrc"
                if os.path.exists(lrc_file):
                    if is_chinese:
                        print(f"已存在同名的 LRC 文件，跳过: {lrc_file}")
                    else:
                        print(f"Already exists a LRC file with the same name, skipping: {lrc_file}")
                    continue
                lyrics = extract_flac_lyrics(audio_file)
                if lyrics:
                    write_lrc_file(audio_file, lyrics)
                else:
                    if is_chinese:
                        print(f"无法提取歌词，跳过文件: {audio_file}")
                    else:
                        print(f"Cannot extract lyrics, skipping file: {audio_file}")


if __name__ == "__main__":
    # Double language support
    language, _ = locale.getlocale()
    is_chinese = language.startswith("zh")
    if is_chinese:
        directory_ = input("请输入要提取的文件夹路径：")
    else:
        directory_ = input("Please input the directory path: ")
    if os.path.isdir(directory_):
        process_directory(directory_)
    else:
        if is_chinese:
            print("无效的文件夹路径")
        else:
            print("Invalid directory path")
