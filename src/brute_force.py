from typing import List


def bf_search(source: List[str], target: List[str]) -> List[tuple]:
    result = []
    for i in range(len(source) - len(target) + 1):
        for j in range(len(target)):
            if target[0 + j] == source[i + j]:
                if j == len(target) - 1:
                    result.append((i, i + j))
            else:
                break
    return result


def show_progress(source, s_pointer, target, t_pointer):
    print(source)
    print(' ' * s_pointer + '^')
    print(' ' * (s_pointer - t_pointer) + target)
    print(' ' * (s_pointer - t_pointer) + '*' * t_pointer + '^')


def bf_search_new(source: List[str], target: List[str],
                  verbose=False) -> List[tuple]:
    result = []

    s_pointer, t_pointer = 0, 0
    if verbose:
        show_progress(source, s_pointer, target, t_pointer)
    while s_pointer < len(source):
        if target[t_pointer] == source[s_pointer]:
            s_pointer += 1
            t_pointer += 1
            if verbose:
                show_progress(source, s_pointer, target, t_pointer)
            if t_pointer >= len(target):
                t_pointer = 0
                result.append(s_pointer - len(target))
                if verbose:
                    show_progress(source, s_pointer, target, t_pointer)
        else:
            s_pointer += 1
            t_pointer = 0
            if verbose:
                show_progress(source, s_pointer, target, t_pointer)
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
