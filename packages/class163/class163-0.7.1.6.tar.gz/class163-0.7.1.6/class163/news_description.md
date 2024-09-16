# class163

网易云音乐部分常用开放信息类 API 调用和部分需要用户凭证的 API 调用, 包括音乐/歌单/搜索结果的获取, 以及音乐的获取及信息写入.

长描述文件目前记录从 `0.7.0` 版本开始的大版本更新的更新文档.

## 0.7.0

### 新增

- `class163.search.Search.search_result_sorted`: 搜索结果自识别歌单/歌曲后, 存储为包含 `Playlist` 或 `Music` 的列表;

- `class163.music.music_from_detail`: 从搜索结果导入音乐;

- `class163.playlist.playlist_from_detail`: 从搜索结果导入歌单;

- `class163.playlist.Playlist.extract_detail`: 新增可选参数 `id_keys` 用于导入歌单 id;

- `class163.playlist.Playlist.update_encode_data`: 更新解码参数的函数, 无需参数.

### 修订

- `class163.playlist.Playlist.extract_detail`: 为满足搜索结果导入的歌单需求:

  1. 在 97 行加入 `try-except` 语句排除可能的没有歌单内歌曲的 id;

  2. 修改 `create_time` 和 `last_update_time` 的载入方式, 使得在没有创建时间的时间戳和最后更新时间的时间戳的时候能正常导入;

- `class163.music.update_encode_data`: 从 `encode_data_update` 更名为 `update_encode_data`.

### 修复

  本次更新没有修复的 bugs.
