import re
import json
import jieba
import random
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from collections import Counter
from wordcloud import WordCloud
from argparse import ArgumentParser
from chat_history_reader import TxtChatHistoryReader, ChatMessage

from typing import List, Set, Optional


def parse_args():
    parser = ArgumentParser('word cloud plotter for QQ chat history')
    parser.add_argument(
        '--chat_history_path',
        '-i',
        type=str,
        required=True,
        help='path to the chat history file, expected to be in txt format')
    parser.add_argument('--stopword_path',
                        '-sw',
                        type=str,
                        default='',
                        help='path to a txt file containing stop words')
    parser.add_argument('--mask_path',
                        '-m',
                        type=str,
                        default='',
                        help='path to an image mask')
    parser.add_argument('--mask_crop_size',
                        type=int,
                        default=960,
                        help='crop size for mask image')
    parser.add_argument('--output_path',
                        '-o',
                        type=str,
                        default='output.png',
                        help='path for image output')
    parser.add_argument('--show',
                        action='store_true',
                        help='whether to show the plot with plt.show()')
    parser.add_argument('--dump_json',
                        action='store_true',
                        help='whether to save processed chat history to a json file')
    parser.add_argument('--json_output_path',
                        type=str,
                        default='dump.json',
                        help='path for json output')
    return parser.parse_args()


def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return f"hsl(0, 0%, {random.randint(60, 100):d}%)"


def load_stopwords(fpath: str):
    with open(fpath, 'r', encoding='utf-8') as f:
        return set([line.strip() for line in f.readlines()])


def cleanse_sentence(msg: str):
    msg_str = msg.replace('[图片]', '').replace('[表情]', '')
    msg_str = re.sub(r'@[^\s]+', '', msg_str)
    if '请使用最新版手机QQ体验新功能' in msg_str:
        # remove unsupported emoji or functions on PC
        msg_str = msg_str.replace('请使用最新版手机QQ体验新功能', '')
        # strip '[', ']'
        msg_str = msg_str[1:-1]
    return msg_str


def filter_strings(messages: List[ChatMessage]):
    msg_strings = []
    for msg in messages:
        if msg.sender_id == '10000':
            # skip system messages
            continue

        msg_str = cleanse_sentence(msg.message)
        if msg_str:
            msg_strings.append(msg_str)
    return msg_strings


def tokenize_message_strings(msg_strings: List[str], stopwords: Optional[Set[str]]):
    # tokenize
    tokens = []
    for msg_str in msg_strings:
        tokens.extend(jieba.cut(msg_str))

    if stopwords is not None:
        # the stopwords in wordcloud seems broken on Chinese input
        # so we do it manually here
        tokens = [token for token in tokens if token not in stopwords]

    return tokens


def load_mask(fpath: str, crop_size: int):
    img = Image.open(fpath)
    width, height = img.size  # Get dimensions

    if crop_size > width or crop_size > height:
        print('crop size must be smaller than image size')
        print('ignoring crop size and using original image size')
        mask = np.array(img)
        return mask

    # center crop
    left = (width - crop_size) / 2
    top = (height - crop_size) / 2
    right = (width + crop_size) / 2
    bottom = (height + crop_size) / 2
    img = img.crop((left, top, right, bottom))

    # invert mask to match implementation of wordcloud
    # 0: foreground, 255: background
    mask = np.array(img)
    mask[mask > 0] = 255
    mask = 255 - mask
    return mask


def main(args):
    # load data
    reader = TxtChatHistoryReader()
    msgs = reader.read(args.chat_history_path)

    if args.dump_json:
        # dump json
        json_msgs = [msg.serialize() for msg in msgs]
        print(f'number of messages: {len(json_msgs)}')
        with open(args.json_output_path, 'w', encoding='utf-8') as f:
            json.dump(json_msgs, f, ensure_ascii=False, indent=4)
        print(f'json file saved to {args.json_output_path}')

    # get all non-empty strings
    msg_strings = filter_strings(msgs)

    # load mask and stopwords
    if args.mask_path != '':
        mask = load_mask(args.mask_path, args.mask_crop_size)
    else:
        mask = None
    if args.stopword_path != '':
        stopwords = load_stopwords(args.stopword_path)
    else:
        stopwords = None

    # tokenize strings
    tokens = tokenize_message_strings(msg_strings, stopwords)

    # plot word cloud
    wordcloud = WordCloud(font_path='C:/Windows/Fonts/Deng.ttf',
                          mask=mask,
                          stopwords=stopwords,
                          margin=10,
                          scale=2,
                          max_words=648).generate_from_frequencies(Counter(tokens))
    plt.imshow(wordcloud.recolor(color_func=grey_color_func, random_state=42),
               interpolation='bilinear')
    plt.axis("off")
    plt.margins(x=0, y=0)

    if args.show:
        plt.show()

    wordcloud.to_file(args.output_path)
    print(f'word cloud saved to {args.output_path}')


if __name__ == '__main__':
    # default stopwords are from https://github.com/goto456/stopwords
    args = parse_args()
    main(args)
