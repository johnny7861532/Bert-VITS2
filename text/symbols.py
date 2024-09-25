punctuation = ["!", "?", "…", ",", "。", "、", "「", "」", "'", "-"]
pu_symbols = punctuation + ["SP", "UNK"]
pad = "_"

# 台灣中文（擴展自原中文符號集）
zh_tw_symbols = [
    "E",
    "En",
    "a",
    "ai",
    "an",
    "ang",
    "ao",
    "b",
    "c",
    "ch",
    "d",
    "e",
    "ei",
    "en",
    "eng",
    "er",
    "f",
    "g",
    "h",
    "i",
    "i0",
    "ia",
    "ian",
    "iang",
    "iao",
    "ie",
    "in",
    "ing",
    "iong",
    "ir",
    "iu",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "ong",
    "ou",
    "p",
    "q",
    "r",
    "s",
    "sh",
    "t",
    "u",
    "ua",
    "uai",
    "uan",
    "uang",
    "ui",
    "un",
    "uo",
    "v",
    "van",
    "ve",
    "vn",
    "w",
    "x",
    "y",
    "z",
    "zh",
    "AA",
    "EE",
    "OO",
    # 可能的台灣特有音素，需要根據實際需求添加
    "er0",  # 去掉捲舌音的 "er"
    "tsi",  # 台語音 "chi"
    "si0",  # 台語音 "si"
]

# 保留原有的日文和英文符號
ja_symbols = [
    "N",
    "a",
    "a:",
    "b",
    "by",
    "ch",
    "d",
    "dy",
    "e",
    "e:",
    "f",
    "g",
    "gy",
    "h",
    "hy",
    "i",
    "i:",
    "j",
    "k",
    "ky",
    "m",
    "my",
    "n",
    "ny",
    "o",
    "o:",
    "p",
    "py",
    "q",
    "r",
    "ry",
    "s",
    "sh",
    "t",
    "ts",
    "ty",
    "u",
    "u:",
    "w",
    "y",
    "z",
    "zy",
]

en_symbols = [
    "aa",
    "ae",
    "ah",
    "ao",
    "aw",
    "ay",
    "b",
    "ch",
    "d",
    "dh",
    "eh",
    "er",
    "ey",
    "f",
    "g",
    "hh",
    "ih",
    "iy",
    "jh",
    "k",
    "l",
    "m",
    "n",
    "ng",
    "ow",
    "oy",
    "p",
    "r",
    "s",
    "sh",
    "t",
    "th",
    "uh",
    "uw",
    "V",
    "w",
    "y",
    "z",
    "zh",
]

# 調整聲調數量
num_zh_tw_tones = 5  # 包括輕聲
num_ja_tones = 2
num_en_tones = 4

# 合併所有符號
normal_symbols = sorted(set(zh_tw_symbols + ja_symbols + en_symbols))
symbols = [pad] + normal_symbols + pu_symbols
sil_phonemes_ids = [symbols.index(i) for i in pu_symbols]

# 合併所有聲調
num_tones = num_zh_tw_tones + num_ja_tones + num_en_tones

# 語言映射
language_id_map = {"ZH-TW": 0, "JP": 1, "EN": 2}
num_languages = len(language_id_map.keys())
language_tone_start_map = {
    "ZH-TW": 0,
    "JP": num_zh_tw_tones,
    "EN": num_zh_tw_tones + num_ja_tones,
}

if __name__ == "__main__":
    a = set(zh_tw_symbols)
    b = set(en_symbols)
    print("共同音素：", sorted(a & b))
    print("台灣中文特有音素：", sorted(a - b))
