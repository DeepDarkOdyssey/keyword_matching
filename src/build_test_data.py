from typing import List, Tuple, Iterable, Callable
from collections import Counter
import random


START_CODE = ord('\u4e00')
END_CODE = ord('\u9fa5')
random.seed(20190516)


def rand_char(start_code=START_CODE, end_code=END_CODE) -> str:
    return chr(random.randint(start_code, end_code))


def fake_passage(min_len=50, max_len=2000) -> str:
    passage_len = random.randint(min_len, max_len)
    passage = ''
    for _ in range(passage_len):
        passage += rand_char()
    return passage


def fake_label(passage: str) -> List[Tuple[int]]:
    start_points = sorted(
        random.sample(range(len(passage)), random.randint(1, 10)))
    end_points = [
        start_point + random.randint(1, 20) for start_point in start_points
    ]
    return list(zip(start_points, end_points))


def build_keywords(text_iterator: Iterable, segmentor: Callable=list, top_n: int=1000):
    word_counter = Counter()
    for text in text_iterator:
        word_counter.update(segmentor(text))
    words = [word for word, count in word_counter.most_common() if len(word)>1]
    return words[:top_n]


if __name__ == "__main__":
    import re
    import jieba
    import time
    from collections import defaultdict
    from brute_force import bf_search
    from kmp import KMP
    from ac_automation import ACAutomation

    def text_iterator():
        with open('data/166893.txt') as f:
            for line in f:
                line = line.strip()
                if line and not re.match('-+', line):
                    yield line
    
    keywords = build_keywords(text_iterator(), jieba.lcut)
    ac_automation = ACAutomation(keywords)
    
    tick = time.time()
    for text in text_iterator():
        for keyword in keywords:
            result = re.findall(keyword, text)
    tock = time.time()
    print('re search time:', tock - tick)

    tick = time.time()
    for text in text_iterator():
        for keyword in keywords:
            result = bf_search(text.strip(), keyword)
            # if result:
            #     print(keyword, result)
        tock = time.time()
    print('bf search time:', tock - tick)
    
    tick = time.time()
    for text in text_iterator():
        for keyword in keywords:
            result = KMP().search(text.strip(), keyword)
            # if result:
            #     print(keyword, result)
    tock = time.time()
    print('kmp search time:', tock - tick)

    tick = time.time()
    for text in text_iterator():
        result = ac_automation.search(text.strip())
    tock = time.time()
    # word2pos = defaultdict(list)
    # for start, end in result:
    #     word2pos[line[start: end+1]].append((start, end))
    # for word, pos in word2pos.items():
    #     print(word, pos)
    print('ac search time:', tock - tick)
    