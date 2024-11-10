document.addEventListener('DOMContentLoaded', () => {
    const audioPlayer = document.getElementById('audioPlayer');
    const audioSource = document.getElementById('audioSource');
    const playBtn = document.getElementById('playBtn');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const songTitle = document.getElementById('songTitle');
    const artistName = document.getElementById('artistName');
    const coverImage = document.getElementById('coverImage');
    const lyricsText = document.getElementById('lyricsText');
    const recommendedSongs = document.getElementById('recommended-songs');
    const playerContainer = document.querySelector('.player-container');
    const themeSwitch = document.getElementById('themeSwitch');
    const body = document.body;

    let currentSongIndex = 0;
    let isPlaying = false;
    let songList = [];

    // 请求推荐歌曲并更新列表
    async function getRecommendations() {
        const response = await fetch('/api/recommend');
        const songs = await response.json();
        songList = songs;
        recommendedSongs.innerHTML = '';  // 清空推荐列表
        songs.forEach((song, index) => {
            const li = document.createElement('li');
            li.textContent = `${song.title} (${song.tags.join(', ')})`;
            li.addEventListener('click', () => {
                loadSong(index);  // 加载歌曲但不自动播放
                sendPlayData(song.title, 'loop');  // 发送单曲循环模式的播放数据
            });
            recommendedSongs.appendChild(li);
        });
    }

    // 加载歌曲信息
    function loadSong(index) {
        const song = songList[index];
        songTitle.textContent = song.title;
        artistName.textContent = "未知艺术家";  // 可以调整为实际艺术家
        coverImage.src = "cover1.jpg";  // 默认封面
        audioSource.src = song.file_path;  // 使用后端提供的 file_path
        lyricsText.textContent = "无歌词";
        audioPlayer.load();
        currentSongIndex = index;
    }

    // 向后端发送播放数据
    async function sendPlayData(title, mode) {
        await fetch('/api/play', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, mode })
        });
    }

    // 切换播放状态
    function togglePlay() {
        const playIcon = playBtn.querySelector('i');
        if (isPlaying) {
            audioPlayer.pause();
            playIcon.classList.replace('fa-pause', 'fa-play');
            playerContainer.classList.remove('playing');
        } else {
            audioPlayer.play();
            playIcon.classList.replace('fa-play', 'fa-pause');
            playerContainer.classList.add('playing');
        }
        isPlaying = !isPlaying;
    }

    playBtn.addEventListener('click', togglePlay);

    nextBtn.addEventListener('click', () => {
        currentSongIndex = (currentSongIndex + 1) % songList.length;
        loadSong(currentSongIndex);
        if (isPlaying) audioPlayer.play();
    });

    prevBtn.addEventListener('click', () => {
        currentSongIndex = (currentSongIndex - 1 + songList.length) % songList.length;
        loadSong(currentSongIndex);
        if (isPlaying) audioPlayer.play();
    });

    // 初始加载推荐歌曲但不自动播放
    getRecommendations();

    // 主题切换功能
    const savedTheme = localStorage.getItem('theme') || 'light';
    body.classList.add(savedTheme);
    themeSwitch.checked = savedTheme === 'dark';

    // 监听主题切换
    themeSwitch.addEventListener('change', () => {
        const newTheme = themeSwitch.checked ? 'dark' : 'light';
        body.classList.replace(body.classList.contains('dark') ? 'dark' : 'light', newTheme);
        localStorage.setItem('theme', newTheme);
    });
});
