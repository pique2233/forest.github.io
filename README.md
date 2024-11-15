# Forest 音乐播放器
# 音乐推荐系统文档

## 目录
- [前端框架](#前端框架)
- [后端集成](#后端集成)
- [算法集成](#算法集成)
- 静态网页运行浏览：https://pique2233.github.io/forest.github.io/templates/index1.html

---

### 前端框架

前端框架主要用于构建用户交互界面，实现音乐推荐、播放控制、反馈收集等功能。

#### 1. 技术栈

- **HTML/CSS/JavaScript**：用于页面结构、样式和基本交互。
- **前端框架 (可选)**：如`React`或`Vue`，提升代码的组织性和可复用性。
- **样式库**：如`Bootstrap`，实现基础的响应式设计。

#### 2. 关键功能

- **音乐推荐模块**：展示推荐的歌曲，并支持用户交互反馈（如喜欢、跳过、播放等）。
- **播放控制模块**：实现播放、暂停、下一首等功能。
- **用户反馈收集**：每次推荐一首歌曲后，用户可提供反馈（如喜欢、不喜欢、跳过等），将反馈数据传输到后端，以更新用户偏好。

#### 3. 前端组件设计

- **推荐卡片组件**：展示歌曲的名称、风格、情绪标签，并提供反馈按钮。
- **播放控制组件**：用于控制歌曲播放，显示当前播放状态。
- **反馈收集组件**：提供“喜欢”、“不喜欢”、“跳过”等按钮，供用户选择反馈。

---

### 后端集成

后端主要负责处理用户反馈、管理用户偏好数据和实现推荐算法。

#### 1. 技术栈

- **Flask/Django (Python)**：用于构建后端服务器，接收前端的请求，并将推荐结果传回前端。
- **数据库 (SQLite/MySQL)**：存储用户偏好向量、歌曲特征向量等数据，便于推荐算法调用。

#### 2. API 设计

- **GET /recommend**：返回推荐歌曲列表。
- **POST /feedback**：接收用户反馈，更新用户偏好向量。
- **GET /songs**：提供可选歌曲信息，支持前端的分类浏览。

#### 3. 数据流

- **用户请求推荐**：前端向后端发送推荐请求，后端根据用户偏好向量和推荐算法，返回符合用户偏好的歌曲。
- **用户反馈提交**：用户在前端提供反馈信息（如喜欢/不喜欢），反馈通过API传送到后端，更新用户偏好向量。

---

### 算法集成

推荐算法根据用户的历史偏好、反馈和标签信息，动态调整推荐权重，以提供个性化的音乐推荐。

#### 1. 算法概述

推荐算法基于用户的偏好向量 \( U \) 和每首歌曲的特征向量 \( V_{s_i} \)，计算推荐得分。公式如下：

$$
S_{s_i} = U \cdot V_{s_i} = \sum_{j=1}^{M} u_{g_j} \cdot v_{s_i, g_j} + \sum_{k=1}^{L} u_{e_k} \cdot v_{s_i, e_k}
$$

其中：
-  $$ \( S_{s_i} \)  $$ 为推荐得分
-  $$ \( u_{g_j} \)  $$ 和  $$ \( u_{e_k} \)  $$ 分别为用户对第  $$ \( j \)  $$ 个风格标签和第  $$ \( k \)  $$ 个情绪标签的偏好权重
-  $$ \( v_{s_i, g_j} \)  $$ 和   $$\( v_{s_i, e_k} \)  $$ 为歌曲的标签向量元素

#### 2. 用户偏好更新

根据用户反馈（如喜欢、不喜欢、跳过等），动态调整偏好向量。更新公式如下：

- **正反馈（喜欢/完整播放）**：
 
 $$ u_{t} = u_{t} + \alpha \cdot (1 - u_{t})  $$

- **负反馈（不喜欢/跳过）**：
 
 $$  u_{t} = u_{t} - \beta \cdot u_{t}  $$


其中  $$ \( \alpha \)  $$ 和   $$ \( \beta \)   $$是学习率，用于控制偏好更新的幅度，通常取值在 \( [0, 1] \) 之间。

#### 3. 推荐流程

1. **初始化用户偏好向量**：初始状态下，假设用户对所有标签的偏好均等。
2. **计算推荐得分**：每首歌曲的推荐得分 \( S_{s_i} \) 由用户偏好向量与歌曲特征向量的点积得出。
3. **排序和推荐**：根据推荐得分从高到低排序，向用户推荐得分最高的歌曲。
4. **偏好更新**：根据用户的反馈（如喜欢、不喜欢、跳过）动态调整用户偏好向量，更新后的向量用于下一次推荐。

#### 4. Python 实现示例

```python
import numpy as np

# 假设已构建的歌曲特征向量
song_vectors = np.array([
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 0],  # Song A
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 1],  # Song B
    # 其他歌曲向量...
])

# 初始化用户偏好向量
user_preference = np.ones(song_vectors.shape[1]) / song_vectors.shape[1]

# 计算推荐得分
def calculate_scores(preference, vectors):
    return vectors.dot(preference)

# 更新用户偏好
def update_preference(preference, vector, feedback, alpha=0.1, beta=0.1):
    if feedback == 'like':
        delta = alpha * (1 - preference)
        preference += vector * delta
    elif feedback == 'dislike':
        delta = beta * preference
        preference -= vector * delta
    preference = np.clip(preference, 0, None)
    preference /= np.sum(preference)
    return preference

# 示例使用
scores = calculate_scores(user_preference, song_vectors)
print("推荐得分:", scores)
