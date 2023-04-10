# Word Cloud Generator for QQ Chat History

> 逃避现实的摸鱼项目。~~我的毕业设计好像要完蛋了~~。
> 从导出的聊天记录生成词云，看看看群友平时都在说些什么~~怪话~~。

## Requirements

- `jieba`
- `numpy`
- `word_cloud`
- `matplotlib`

## 快速开始

> ゴゴゴ・ゴーゴー☆

### 0. 配环境

需要一些 Python 包，都写在 [上面](#requirements) 了。

### 1. 准备数据

1. *(Required)* **从 QQ 导出 `txt` 格式的聊天记录**
   - 可以从 `消息管理器` 里导出聊天记录，可以参考[这里](https://kf.qq.com/faq/161230MfMfqy161230q2ENVr.html)
   - Windows PC 端的 QQ 的 `消息管理器` 可以从 `设置` -> `安全设置` 里打开 ([ref](https://jingyan.baidu.com/article/495ba841bea61a79b30ede9a.html))
2. *(Optional)* **准备一张图片作为 mask**
   - 默认的词云是长方形的，但是可以额外提供一张图片作为 mask 来限定词云的形状
   - 这张图片或许最好是灰度图？~~测试用的图片是灰度图所以不保证 RGB 也能工作。~~
   - ~~没搞清楚是 0 的地方做背景还是 255 的地方做背景，可以试试~~
   - 关于 mask 和 color 的更多用法，可以看 [wordcloud 的官方文档](https://amueller.github.io/word_cloud/index.html)

### 2. Just Rush

```sh
# TL;DR
python word_cloud_plot.py \
  -i data/some_chat_history.txt \
  -sw data/cn_stopwords.txt \
  -m data/some_fancy_mask.png \
  -o outputs/an_output.png \
  --show \
  --dump_json \
  --json_output_path outputs/serialized_messages.json
```

`word_cloud_plot.py` 接受一些参数

- `--chat_history_path`, `-i`: 聊天记录的 `.txt` 文件，作为输入。
- `--stop_word_path`, `-sw`: *Optional*. 停用词列表。停用词表里的词不会被统计词频，也不会出现在词云里。
  - 需要停用词的话可以看看 [这个仓库](https://github.com/goto456/stopwords)。
- `--mask_path`, `-m`: *Optional*. 作为 mask 的图片的路径。
- `--mask_crop_size`: *Optional, deafult: 960*. 如果需要裁切 mask 的图片的话可以用这个，但是只支持裁成正方形（宽度和高度一样）
  - ~~因为这是一个摸鱼项目而且我懒了~~
- `--output_path`: *Optional, default: 'output.png'*. 保存词云图片的路径。
- `--show`: *Optional*. 如果开启，会用 `matplotlib.pyplot.show()` 方法弹一个对话框展示词云。否则会直接保存。
- `--dump_json`: *Optional*. 如果开启，会把处理好的聊天记录序列化成 JSON，保存到 `json_output_path`
- `--json_output_path`: *Optional, default: dump.json*. 保存 JSON 的路径
