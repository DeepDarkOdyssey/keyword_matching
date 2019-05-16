from typing import List


class TrieNode(object):
    def __init__(self, word, depth=0):
        self.word = word
        self.children = {}
        self.is_leaf = False
        self.depth = depth

    def insert(self, words: List[str]):
        current_node = self
        for word in words:
            if word not in current_node.children:
                current_node.children[word] = TrieNode(word, current_node.depth+1)
            current_node = current_node.children[word]
        current_node.is_leaf = True

    def search(self, words: List[str]) -> bool:
        current_node = self
        for word in words:
            if word not in current_node.children:
                return False
            else:
                current_node = current_node.children[word]
        return current_node.is_leaf
    
    def layer_traversal(self):
        result = []
        queue = []
        queue.append(self)
        while len(queue) > 0:
            node = queue.pop(0)
            for child in node.children.values():
                queue.append(child)
                print(child.word, child.depth, child.is_leaf)

    def df_traversal(self):
        stack = []
        stack.append(self)
        discovered = set()
        while len(stack)>0:
            node = stack.pop()
            if node not in discovered:
                discovered.add(node)
                for child in node.children.values():
                    stack.append(child)
        return stack
    
    def list_words(self, node, words='', words_list=[]):
        if node.is_leaf:
            words_list.append(words)
        for word, child in node.children.items():
            if len(child.children) == 0:
                words_list.append(words+word)
            else:
                self.list_words(child, words+word, words_list)
        return words_list

    def to_dict(self):
        result = {}
        for word, child in self.children.items():
            result[word] = child.to_dict()
        return result


if __name__ == "__main__":
    import json
    trie_tree = TrieNode('#ROOT#')
    # words_list = ['1', '12', '123', '12345', '14', '145', '6', '67', '8']
    # for word in words_list:
    #     trie_tree.insert(word)
    # trie_tree.layer_traversal()
    keywords = []
    with open('data/keywords.tsv', encoding='utf8') as f:
        for line in f:
            keyword = line.strip()
            keywords.append(keyword)
            trie_tree.insert(list(keyword))
    # with open('data/trie_tree.json', 'w', encoding='utf8') as f:
    #     json.dump(trie_tree.to_dict(), f, ensure_ascii=False, indent=2)
    # print(trie_tree.search(list('医院陪护')))
    words_list = []
    words_list = trie_tree.list_words(trie_tree)
    print(set(words_list) == set(keywords))
