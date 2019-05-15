from typing import List


class TrieNode(object):
    def __init__(self, word):
        self.word = word
        self.children = {}
        self.is_leaf = False

    def insert(self, words: List[str]):
        current_node = self
        for word in words:
            if word not in current_node.children:
                current_node.children[word] = TrieNode(word)
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

    def to_dict(self):
        result = {}
        for word, child in self.children.items():
            result[word] = child.to_dict()
        return result


if __name__ == "__main__":
    import json
    trie_tree = TrieNode('#ROOT#')
    with open('data/keywords.tsv', encoding='utf8') as f:
        for line in f:
            keyword = line.strip()
            trie_tree.insert(keyword)
    with open('data/trie_tree.json', 'w', encoding='utf8') as f:
        json.dump(trie_tree.to_dict(), f, ensure_ascii=False, indent=2)
