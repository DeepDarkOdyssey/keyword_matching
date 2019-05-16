from trie_tree import TrieNode
from typing import List, Tuple, Any

class ACNode(TrieNode):
    def __init__(self, word, depth=0):
        super().__init__(word, depth=depth)
        self.fail = None

class ACAutomation(object):
    def __init__(self, words_list: List[List[str]]):
        self.root = ACNode('%ROOT%')
        for words in words_list:
            self.root.insert(words)
        for node in self.root.children.values():
            node.fail = self.root
        self.add_fails()

    def add_fails(self):
        # TODO: use the recursive way to optimize this method
        queue = []
        queue.extend(self.root.children.values())
        while len(queue) > 0:
            node = queue.pop(0)
            for word, child in node.children.items():
                fail_to = node.fail
                while True:
                    if word in fail_to.children:
                        child.fail = fail_to.children[word]
                        break
                    elif fail_to is self.root:
                        child.fail = self.root
                        break
                    else:
                        fail_to = fail_to.fail
                queue.append(child)

    def search(self, source: List[str]) -> List[Tuple[Any, int]]:
        result = []
        t_pointer = self.root
        for s_pointer in range(len(source)):
            word = source[s_pointer]
            while (t_pointer.fail is not None) and (word not in t_pointer.children):
                t_pointer = t_pointer.fail
            if word in t_pointer.children:
                t_pointer = t_pointer.children[word]
            if t_pointer.is_leaf:
                result.append((s_pointer-t_pointer.depth + 1, s_pointer))
                t_pointer = self.root
        return result


if __name__ == "__main__":
    # keywords = ["nihao","hao","hs","hsr"]
    # target = "sdmfhsgnshejfgnihaofhsrnihao"
    # ac_automation = ACAutomation(keywords)

    import time
    import pandas as pd
    df = pd.read_csv('./data/dev.tsv', sep='\t', encoding='utf8')
    keywords = []
    with open('data/keywords.tsv', encoding='utf8') as f:
        for i, keyword in enumerate(f):
            keyword = keyword.strip()
            keywords.append(keyword)
    tick = time.time()
    print('深' in keywords)
    # ac_automation = ACAutomation(keywords)
    # tock = time.time()
    # print(tock - tick)
    # stack = []
    # stack.append(ac_automation.root)
    # char_list = []
    # while len(stack) > 0:
    #     node = stack.pop()
    #     for child in node.children.values():
    #         char_list.append(child.word)
    #         stack.append(child)
    #         if child.is_leaf:
    #             print(''.join(char_list))
    #             char_list = []
    # queue = []
    # queue.append(ac_automation.root)
    # while len(queue) > 0:
    #     node = queue.pop(0)
    #     for child in node.children.values():
    #         queue.append(child)
    #         print(child.word, child.depth, child.fail.word)

    desc = df['描述'].values[0]
    # result = ac_automation.search(desc)
    # for start, end in result:
    #     print(start, end, desc[start: end+1])
    # tick = time.time()
    # ac_run_time = tick - tock
    # for i, keyword in enumerate(keywords):
    #     print(f'\r{i}', end='')
    #     if keyword in desc:
    #         print(f' {keyword}')
    # tock = time.time()
    # in_run_time = tock - tick
    # print()
    # print(ac_run_time, in_run_time)