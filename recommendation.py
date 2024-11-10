import os
from collections import defaultdict
import  random
# 用户偏好记录
user_preferences = defaultdict(int)


# 加载音乐数据（每首歌的分类标签）
def load_songs():
    """
    从指定的音乐文件夹中加载歌曲数据，每首歌的分类标签来源于文件夹路径的层级。
    返回一个包含歌曲信息的列表。
    """
    music_folder = 'music_data/风格'  # 根目录为 music_data/风格
    songs = []

    for root, dirs, files in os.walk(music_folder):
        for file in files:
            if file.endswith('.mp3'):
                # 获取文件的完整路径
                file_path = os.path.join(root, file)

                # 获取歌曲的标签，使用文件路径中目录的层次作为标签
                genre_tags = os.path.relpath(root, music_folder).split(os.sep)

                songs.append({
                    "title": file,
                    "tags": genre_tags,  # 使用路径中的目录层级作为标签
                    "file_path": file_path,
                    "play_count": 0
                })
    return songs


# 根据用户偏好生成推荐
def generate_recommendations(songs, top_n=5):
    """
    根据用户偏好权重和播放次数为每首歌曲评分，并返回分数最高的推荐列表。
    """
    scores = []
    for song in songs:
        # 计算每首歌的得分，基于标签偏好和播放次数
        score = sum(user_preferences[tag] for tag in song["tags"]) + song["play_count"]
        scores.append((song, score))

    scores.sort(key=lambda x: x[1], reverse=True)
    recommendations = [song for song, _ in scores[:top_n]]
    return recommendations


# 模拟用户播放行为
def simulate_user_behavior(song, mode="random"):
    """
    模拟用户的播放行为，根据播放模式和播放时长调整用户偏好权重。
    参数:
        - song: 当前播放的歌曲
        - mode: 播放模式（"random" 或 "loop"）
    """
    play_time = random.uniform(0.1, 1.0)  # 随机模拟播放时间（0-1之间，1表示完整播放）

    # 根据播放模式调整播放次数权重
    if mode == "loop":
        song["play_count"] += 2
    else:
        song["play_count"] += 1

    # 根据播放时间调整偏好
    if play_time > 0.7:  # 超过70%播放时间即为喜欢
        for tag in song["tags"]:
            user_preferences[tag] += song["play_count"]
    elif play_time < 0.3:  # 短时跳过
        for tag in song["tags"]:
            user_preferences[tag] -= song["play_count"]

    return play_time


# 打印当前用户偏好权重分配
def print_current_preferences():
    """
    实时打印当前用户的偏好权重分配，供调试使用。
    """
    print("Current weight distribution:")
    for tag, weight in user_preferences.items():
        print(f"  {tag}: {weight}")
