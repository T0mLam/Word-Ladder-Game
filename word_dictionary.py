'''
Trie is a tree data structure.
Each node except the leaf node has 0 to 26 children, storing each alphabet of a word.

e.g.
['app', 'apps', 'apple', 'bed', 'bee'] can be stored as ...   
('*' indicates end of word)

              ROOT
              / \
            a     b
           /       \
          p         e
        /          /  \
      *p         *d    *e     
     / \
   *s   l
       /
      *e

'''
class TrieNode:
    def __init__(self):
        self.children = {}
        self.end_of_word = False


class WordDictionary:
    def __init__(self):
        self.root = TrieNode()
        self.__file_input()

    def find(self, word):
        if not word:
            return
        
        node = self.root

        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return node.end_of_word

    def find_neighbors(self, word):
        if not word:
            return []
        
        original_word = word
        n = len(word)
        res = set()
        # Create permutations of the word
        # e.g. 'cow' -> ['*ow', 'c*w', 'co*'], 
        # (* indicates any alphabets)
        permutations = [word[:i] + '*' + word[i + 1:] for i in range(n)]

        cache = []
        def dfs(i, node):
            # Enable dfs() to access the outer variable res
            nonlocal res

            # 1. Check i == n (whether the search reaches the end of the word)
            # 2. Check node.end_of_word (whether the word exists in the Trie)
            # 3. Add the found word to res
            if i == n and node.end_of_word:
                res.add(''.join(cache))
                return
            
            # Stop the recursion if ...
            # 1. The search reaches the end of the word but no valid words are found
            # 2. The character is not a child of the node nor is it a '*'
            if (i == n or
                word[i] != '*' and 
                word[i] not in node.children):
                return 
        
            for child in node.children:
                # Continue the recursion only on the subtree of the current character
                # or all children if the character is a '*'
                if word[i] == '*' or word[i] == child:
                    # Backtracking 
                    # Using a cache variable to store the combinations of the word
                    # Add char -> dfs -> remove char when dfs returns
                    # Instead of passing combination as parameter, dfs(i, node, combination)
                    # Reusing the variable to reduce memory usage 
                    cache.append(child)
                    # Move pointer i to the next character and set the child node to be the new root
                    dfs(i + 1, node.children[child])
                    cache.pop()
        
        for word in permutations:
            dfs(0, self.root)

        res.discard(original_word)
        return list(res)

    def __file_input(self):
        with open('words_alpha.txt', 'r') as f:
            for word in f.read().split():
                self.__insert(word)

    def __insert(self, word):
        # Create a pointer to the root
        node = self.root

        # Check if the character is a child of the root
        for char in word:
            # Create a new branch if the character is not found
            if char not in node.children:
                node.children[char] = TrieNode()
            # Traverse to the node storing the character 
            node = node.children[char]
            
        # Set the node storing the last character of the word to be the end_of_word
        node.end_of_word = True

# Testing
if __name__ == '__main__':
    wd = WordDictionary()
    print(wd.find_neighbors('!'))
    print(wd.find_neighbors('cow'))
    print(wd.find_neighbors('life'))
    print(wd.find('wife'))

    
        
