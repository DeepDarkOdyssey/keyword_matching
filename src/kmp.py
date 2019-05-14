from typing import List


def kmp_search(source: List[str], target: List[str]) -> List[tuple]:
    partial_match_tabel = []
    print(target)
    for i in range(len(target)):
        match_len = partial_match(target[:i+1])
        partial_match_tabel.append(match_len)
    for i in range(len(source)):
        for j in range(len(target)):
            if target[0+j] == source[i+j]:
                if j == len(target) - 1:
                    print(j)
            else:
                i += j - partial_match_tabel[j]


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
    with open('data/keywords.tsv', encoding='utf8') as f:
        for keyword in f:
            keywords.append(keyword.strip())
    
    kmp_search(None, '123123')