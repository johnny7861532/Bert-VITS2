# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import List
from typing import Tuple

try:
    import jieba_fast as jieba
except:
    import jieba
from pypinyin import lazy_pinyin
from pypinyin import Style


class ToneSandhi:
    def __init__(self):
        self.must_neural_tone_words = {
            "麻煩", "高粱", "骨頭", "饅頭", "風箏", "力氣", "學生", 
            "什麼", "那個", "大夫", "太陽", "爺爺", "奶奶", "媽媽",
            "爸爸", "哥哥", "姐姐", "弟弟", "妹妹", "叔叔", "阿姨",
            "老師", "同學", "朋友", "醫生", "先生", "小姐", "東西",
            "水餃", "餃子", "包子", "衛生", "大姊", "大哥", "女兒",
            "兒子", "眼睛", "鼻子", "耳朵", "肚子", "肚臍", "大人",
            "小孩", "指甲", "嘴巴", "生氣", "熱鬧", "便宜", "漂亮",
            "舒服", "糊塗", "快樂", "聰明", "自在", "知識",
        }
        self.must_not_neural_tone_words = {
            "男子", "女子", "分子", "原子", "量子", "蓮子",
            "石子", "瓜子", "電子", "人人", "個個", "處處",
        }
        self.punc = "：，；。？！「」『』、"

        # 載入台灣常用詞字典
        jieba.load_userdict("path_to_taiwan_words.txt")  # 請確保此檔案存在

    def _neural_sandhi(self, word: str, pos: str, finals: List[str]) -> List[str]:
        for j, item in enumerate(word):
            if (
                j - 1 >= 0
                and item == word[j - 1]
                and pos[0] in {"n", "v", "a"}
                and word not in self.must_not_neural_tone_words
            ):
                finals[j] = finals[j][:-1] + "5"
        
        if len(word) >= 1 and word[-1] in "吧呢啊喔耶欸":
            finals[-1] = finals[-1][:-1] + "5"
        elif len(word) >= 1 and word[-1] in "的":  # 只有「的」通常讀輕聲
            finals[-1] = finals[-1][:-1] + "5"
        elif (
            len(word) > 1
            and word[-1] in "們"
            and pos in {"r", "n"}
            and word not in self.must_not_neural_tone_words
        ):
            finals[-1] = finals[-1][:-1] + "5"
        elif len(word) > 1 and word[-1] in "子":
            if word in self.must_neural_tone_words:
                finals[-1] = finals[-1][:-1] + "5"
        else:
            if word in self.must_neural_tone_words:
                finals[-1] = finals[-1][:-1] + "5"

        return finals

    def _bu_sandhi(self, word: str, finals: List[str]) -> List[str]:
        if len(word) == 3 and word[1] == "不":
            finals[1] = finals[1][:-1] + "5"
        else:
            for i, char in enumerate(word):
                if char == "不" and i + 1 < len(word) and finals[i + 1][-1] == "4":
                    finals[i] = finals[i][:-1] + "2"
        return finals

    def _yi_sandhi(self, word: str, finals: List[str]) -> List[str]:
        if word.find("一") != -1 and all(
            [item.isnumeric() for item in word if item != "一"]
        ):
            return finals
        elif len(word) == 3 and word[1] == "一" and word[0] == word[-1]:
            finals[1] = finals[1][:-1] + "5"
        elif word.startswith("第一"):
            finals[1] = finals[1][:-1] + "1"
        else:
            for i, char in enumerate(word):
                if char == "一" and i + 1 < len(word):
                    if finals[i + 1][-1] == "4":
                        finals[i] = finals[i][:-1] + "2"
                    else:
                        if word[i + 1] not in self.punc:
                            finals[i] = finals[i][:-1] + "4"
        return finals

    def _split_word(self, word: str) -> List[str]:
        word_list = jieba.cut_for_search(word)
        word_list = sorted(word_list, key=lambda i: len(i), reverse=False)
        first_subword = word_list[0]
        first_begin_idx = word.find(first_subword)
        if first_begin_idx == 0:
            second_subword = word[len(first_subword):]
            new_word_list = [first_subword, second_subword]
        else:
            second_subword = word[:-len(first_subword)]
            new_word_list = [second_subword, first_subword]
        return new_word_list

    def _three_sandhi(self, word: str, finals: List[str]) -> List[str]:
        if len(word) == 2 and self._all_tone_three(finals):
            finals[0] = finals[0][:-1] + "2"
        elif len(word) == 3:
            if self._all_tone_three(finals):
                finals[0] = finals[0][:-1] + "2"
                finals[1] = finals[1][:-1] + "2"
            else:
                word_list = self._split_word(word)
                finals_list = [finals[:len(word_list[0])], finals[len(word_list[0]):]]
                if len(finals_list) == 2:
                    for i, sub in enumerate(finals_list):
                        if self._all_tone_three(sub) and len(sub) == 2:
                            finals_list[i][0] = finals_list[i][0][:-1] + "2"
                    finals = sum(finals_list, [])
        elif len(word) == 4:
            finals_list = [finals[:2], finals[2:]]
            finals = []
            for sub in finals_list:
                if self._all_tone_three(sub):
                    sub[0] = sub[0][:-1] + "2"
                finals += sub

        return finals

    def _all_tone_three(self, finals: List[str]) -> bool:
        return all(x[-1] == "3" for x in finals)

    def _merge_bu(self, seg: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        new_seg = []
        last_word = ""
        for word, pos in seg:
            if last_word == "不":
                word = last_word + word
            if word != "不":
                new_seg.append((word, pos))
            last_word = word[:]
        if last_word == "不":
            new_seg.append((last_word, "d"))
            last_word = ""
        return new_seg

    def _merge_yi(self, seg: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        new_seg = []
        i = 0
        while i < len(seg):
            word, pos = seg[i]
            if (
                i - 1 >= 0
                and word == "一"
                and i + 1 < len(seg)
                and seg[i - 1][0] == seg[i + 1][0]
                and seg[i - 1][1] == "v"
            ):
                new_seg.append([seg[i - 1][0] + "一" + seg[i - 1][0], "v"])
                i += 3
            else:
                new_seg.append([word, pos])
                i += 1
        return new_seg

    def _merge_reduplication(self, seg: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        new_seg = []
        for i, (word, pos) in enumerate(seg):
            if new_seg and word == new_seg[-1][0]:
                new_seg[-1][0] = new_seg[-1][0] + seg[i][0]
            else:
                new_seg.append([word, pos])
        return new_seg

    def pre_merge_for_modify(self, seg: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        seg = self._merge_bu(seg)
        try:
            seg = self._merge_yi(seg)
        except:
            print("_merge_yi failed")
        seg = self._merge_reduplication(seg)
        return seg

    def _taiwan_particle_sandhi(self, word: str, finals: List[str]) -> List[str]:
        if word in ["啦", "喔", "耶", "啊", "欸", "呢", "嘛", "吧"]:
            finals[-1] = finals[-1][:-1] + "5"
        return finals

    def modified_tone(self, word: str, pos: str, finals: List[str]) -> List[str]:
        finals = self._bu_sandhi(word, finals)
        finals = self._yi_sandhi(word, finals)
        finals = self._neural_sandhi(word, pos, finals)
        finals = self._three_sandhi(word, finals)
        finals = self._taiwan_particle_sandhi(word, finals)
        return finals
