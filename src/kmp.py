from typing import List


def kmp_search(source: List[str], target: List[str]) -> List[tuple]:
    print(f'source:{source}, target:{target}')
    partial_match_tabel = [-1]
    for i in range(len(target)):
        match_len = partial_match(target[:i+1])
        partial_match_tabel.append(match_len)
    print(partial_match_tabel)
    
    i = 0
    while i < len(source) - len(target):
        print(i)
        for j in range(len(target)):
            print(f'\tj:{j} s:{source[i+j]} t:{target[0+j]}')
            if target[0+j] == source[i+j]:
                if j == len(target) - 1:
                    print('gotya', target)
                    i += len(target)
            else:
                i += j - partial_match_tabel[j]
                break
        




def partial_match(sequence: List[str]) -> int:
    prefixes = []
    postfixes = []
    for i in range(len(sequence) - 1):
        prefix = sequence[:i+1]
        postfix = sequence[i+1:]
        prefixes.append(prefix)
        postfixes.insert(0, postfix)
    max_match_len = 0
    for prefix, postfix in zip(prefixes, postfixes):
        if (prefix == postfix) & (len(prefix) > max_match_len):
            max_match_len = len(prefix)
    return max_match_len


if __name__ == "__main__":
    keywords = []
    kmp_search('000124123123456789000', '123123')