from typing import List


def show_progress(source, s_pointer, target, t_pointer):
    print(source)
    s_prefix = s_pointer - t_pointer
    print(' ' * s_pointer + '^')
    print(' ' * s_prefix + target)
    print(' ' * s_prefix + ''.join([str(p) for p in partial_match_table]))
    print(' ' * s_prefix + '*' * t_pointer + '^')


def kmp_search(source: List[str],
               target: List[str],
               partial_match_table: List[int],
               verbose=False) -> List[tuple]:
    result = []
    t_pointer = 0
    for s_pointer in range(len(source)):
        if verbose:
            show_progress(source, s_pointer, target, t_pointer)
        while t_pointer > 0 and source[s_pointer] != target[t_pointer]:
            t_pointer = partial_match_table[t_pointer - 1]
            if verbose:
                show_progress(source, s_pointer, target, t_pointer)

        if source[s_pointer] == target[t_pointer]:
            t_pointer += 1
        if t_pointer == len(target):
            result.append((s_pointer - t_pointer + 1, target,
                           source[s_pointer - t_pointer + 1:s_pointer + 1]))
            # t_pointer = partial_match_table[t_pointer - 1]
            t_pointer = 0

    return result


def partial_match(sequence: List[str]) -> int:
    prefixes = []
    postfixes = []
    for i in range(len(sequence) - 1):
        prefix = sequence[:i + 1]
        postfix = sequence[i + 1:]
        prefixes.append(prefix)
        postfixes.insert(0, postfix)
    max_match_len = 0
    for prefix, postfix in zip(prefixes, postfixes):
        if (prefix == postfix) & (len(prefix) > max_match_len):
            max_match_len = len(prefix)
    return max_match_len


def build_partial_match_table(sequence: List[str]) -> List[int]:
    partial_match_table = []
    for i in range(len(sequence)):
        match_len = partial_match(sequence[:i + 1])
        partial_match_table.append(match_len)
    return partial_match_table


if __name__ == "__main__":
    # source = '00012456712312389000'
    # target = '123123'
    # partial_match_table = build_partial_match_table(target)
    # print(partial_match_table)
    # print(kmp_search(source, target, partial_match_table, verbose=True))

    import time
    import pandas as pd
    df = pd.read_csv('./data/dev.tsv', sep='\t', encoding='utf8')
    keywords = []
    partial_match_tables = {}
    print('building partial match tables...')
    tick = time.time()
    with open('data/keywords.tsv', encoding='utf8') as f:
        for i, keyword in enumerate(f):
            keyword = keyword.strip()
            partial_match_table = build_partial_match_table(keyword)
            partial_match_tables[keyword] = partial_match_table
            keywords.append(keyword)
            print(f'\r{i} {keyword}', end='')
    tock = time.time()
    building_time = tock - tick
    desc = df['描述'].values[0]
    for i, keyword in enumerate(keywords):
        result = kmp_search(list(desc), list(keyword),
                            partial_match_tables[keyword])
        print(f'\r{i}', end='')
    tick = time.time()
    kmp_run_time = tick - tock
    for i, keyword in enumerate(keywords):
        print(f'\r{i}', end='')
        if keyword in desc:
            print(f' {keyword}')
    tick = time.time()
    in_run_time = tick - tock
    print()
    print(building_time, kmp_run_time, in_run_time)
