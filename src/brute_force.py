from typing import List


def bf_search(source: List[str], target: List[str]) -> List[tuple]:
    result = []
    for i in range(len(source) - len(target) + 1):
        for j in range(len(target)):
            if target[0+j] == source[i+j]:
                if j == len(target) - 1:
                    result.append((i, i+j))
            else:
                break
    return result


if __name__ == "__main__":
    import time
    import pandas as pd
    df = pd.read_csv('./data/dev.tsv', sep='\t', encoding='utf8')
    keywords = []
    with open('data/keywords.tsv', encoding='utf8') as f:
        for keyword in f:
            keyword = keyword.strip()
            keywords.append(keyword)
    desc = df['描述'].values[0]
    tick = time.time()
    for i, keyword in enumerate(keywords):
        result = bf_search(list(desc), list(keyword))
        print(f'\r{i}', end='')
        if result:
            print(f' {keyword}')
    tock = time.time()
    bf_run_time = tock - tick
    for i, keyword in enumerate(keywords):
        print(f'\r{i}', end='')
        if keyword in desc:
            print(f' {keyword}')
    tick = time.time()
    in_run_time = tick - tock
    print()
    print(bf_run_time, in_run_time)
