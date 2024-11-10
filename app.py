from flask import Flask, jsonify, request, send_from_directory, render_template
import os
from urllib.parse import unquote
from recommendation import load_songs, generate_recommendations, simulate_user_behavior, user_preferences, print_current_preferences

app = Flask(__name__)

# 加载歌曲数据
songs = load_songs()

# 首页路由，渲染 HTML 页面
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/recommend', methods=['GET'])
def get_recommendations():
    recommended_songs = generate_recommendations(songs)
    return jsonify([
        {
            "title": song["title"],
            "tags": song["tags"],
            "file_path": f"/music/{os.path.relpath(song['file_path'], 'music_data/风格')}"
        }
        for song in recommended_songs
    ])

# 播放行为更新接口
@app.route('/api/play', methods=['POST'])
def play_song():
    data = request.get_json()
    song_title = data.get("title")
    play_mode = data.get("mode", "random")  # 默认模式为随机播放

    # 找到播放的歌曲对象
    song = next((s for s in songs if s["title"] == song_title), None)
    if song:
        simulate_user_behavior(song, mode=play_mode)  # 更新偏好
        print_current_preferences()  # 实时打印当前权重分配
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"error": "Song not found"}), 404

@app.route('/music/<path:filename>')
def serve_music(filename):
    # 解码文件名，处理空格和中文字符
    decoded_filename = unquote(filename)
    return send_from_directory('music_data/风格', decoded_filename)
# 打印当前用户偏好权重
def print_current_preferences():
    print("Current weight distribution:")
    for tag, weight in user_preferences.items():
        print(f"  {tag}: {weight}")

if __name__ == '__main__':
    app.run(debug=True)
