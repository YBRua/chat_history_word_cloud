# Word Cloud Generator for QQ Chat History

## Requirements

- `jieba`
- `numpy`
- `word_cloud`
- `matplotlib`

## Quick Start

### 0. Setting up the Environment

A few Python packages are required for the script to properly run, which are listed above.

### 1. Preparing Data

1. *(Required)* **Export chat history in `.txt` format**
   - Follow the instructions [here](https://kf.qq.com/faq/161230MfMfqy161230q2ENVr.html) to export history from `消息管理器`
   - For Windows PC, `消息管理器` can be found in the settings panel ([ref](https://jingyan.baidu.com/article/495ba841bea61a79b30ede9a.html))
2. *(Optional)* **Prepare an image mask**
   - The default shape of the word cloud is a rectangle.
   - A mask can be used to change the shape of the cloud.
   - Current implementation only supports binary mask (0 for background and 255 for foreground)
   - For more usages of masks and colors, refer to the [official documentation of wordcloud](https://amueller.github.io/word_cloud/index.html)

### 2. Running the Script

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

The main script `word_cloud_plot.py` accepts several arguments

- `--chat_history_path`, `-i`: path to the input `.txt` file containing exported chat history
- `--stop_word_path`, `-sw`: *Optional*. path to a txt file containing a list of stopwords
- `--mask_path`, `-m`: *Optional*. path to an image file to be used as the mask
- `--mask_crop_size`: *Optional, deafult: 960*. integer value for cropping the image
- `--output_path`: *Optional, default: 'output.png'*. path for saving the word cloud
- `--show`: *Optional*. if enabled, the script will display the word cloud in an interactive window
- `--dump_json`: *Optional*. if enabled, the processed messages will be serialized and stored to `json_output_path`
- `--json_output_path`: *Optional, default: dump.json*. path to save processed chat messages, used only when `--dump_json` is enabled
