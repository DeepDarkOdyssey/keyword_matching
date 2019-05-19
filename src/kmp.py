from typing import List, Tuple


class KMP(object):
    def build_partial_match_table(self, target: List[str]):
        partial_match_table = [0]
        for i in range(1, len(target)):
            j = partial_match_table[i - 1]
            while j > 0 and target[j] != target[i]:
                j = partial_match_table[j - 1]
            if target[i] == target[j]:
                partial_match_table.append(j + 1)
            else:
                partial_match_table.append(0)
        return partial_match_table

    def search(self,
               source: List[str],
               target: List[str],
               verbose: bool = False) -> List[Tuple[int]]:
        partial_match_table = self.build_partial_match_table(target)
        result = []
        t_pointer = 0
        for s_pointer in range(len(source)):
            if verbose:
                show_progress(source, s_pointer, target, t_pointer,
                              partial_match_table)
            while t_pointer > 0 and source[s_pointer] != target[t_pointer]:
                t_pointer = partial_match_table[t_pointer - 1]
                if verbose:
                    show_progress(source, s_pointer, target, t_pointer,
                                  partial_match_table)

            if source[s_pointer] == target[t_pointer]:
                t_pointer += 1
            if t_pointer == len(target):
                result.append((s_pointer - t_pointer + 1, s_pointer))
                # t_pointer = partial_match_table[t_pointer - 1]
                t_pointer = 0
        return result


def show_progress(source, s_pointer, target, t_pointer, partial_match_table):
    print(source)
    s_prefix = s_pointer - t_pointer
    print(' ' * s_pointer + '^')
    print(' ' * s_prefix + target)
    print(' ' * s_prefix + ''.join([str(p) for p in partial_match_table]))
    print(' ' * s_prefix + '*' * t_pointer + '^')


def kmp_search(source: List[str],
               target: List[str],
               partial_match_table: List[int],
               verbose: bool = False) -> List[int]:
    result = []
    t_pointer = 0
    for s_pointer in range(len(source)):
        if verbose:
            show_progress(source, s_pointer, target, t_pointer,
                          partial_match_table)
        while t_pointer > 0 and source[s_pointer] != target[t_pointer]:
            t_pointer = partial_match_table[t_pointer - 1]
            if verbose:
                show_progress(source, s_pointer, target, t_pointer,
                              partial_match_table)

        if source[s_pointer] == target[t_pointer]:
            t_pointer += 1
        if t_pointer == len(target):
            result.append(s_pointer - t_pointer + 1)
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
    # kmp = KMP()
    # print(kmp.search(list(source), list(target)))

    import time
    import pandas as pd
    df = pd.read_csv('./data/dev.tsv', sep='\t', encoding='utf8')
    keywords = []
    tick = time.time()
    with open('data/keywords.tsv', encoding='utf8') as f:
        for i, keyword in enumerate(f):
            keyword = keyword.strip()
            keywords.append(keyword)
    desc = df['描述'].values[0]
    for i, keyword in enumerate(keywords):
        kmp = KMP()
        result = kmp.search(list(desc), list(keyword))
        print(f'\r{i} {keyword}', end='')
    tock = time.time()
    kmp_run_time = tock - tick
    for i, keyword in enumerate(keywords):
        print(f'\r{i}', end='')
        if keyword in desc:
            print(f' {keyword}')
    tick = time.time()
    in_run_time = tick - tock
    print()
    print(kmp_run_time, in_run_time)
