from collections import deque, defaultdict

class AhoCorasick:
    def __init__(self):
        self.trie = defaultdict(dict)
        self.fail = defaultdict(int)
        self.output = defaultdict(list)
        self.state_count = 0
    
    def add_pattern(self, pattern, index):
        state = 0
        for char in pattern:
            if char not in self.trie[state]:
                self.state_count += 1
                self.trie[state][char] = self.state_count
            state = self.trie[state][char]
        self.output[state].append(index)
    
    def build_automaton(self):
        queue = deque()
        for char in self.trie[0]:
            state = self.trie[0][char]
            self.fail[state] = 0
            queue.append(state)
        
        while queue:
            r = queue.popleft()
            
            for char, u in self.trie[r].items():
                queue.append(u)
                
                state = self.fail[r]
                while state != 0 and char not in self.trie[state]:
                    state = self.fail[state]
                if char in self.trie[state]:
                    self.fail[u] = self.trie[state][char]
                else:
                    self.fail[u] = 0
                
                self.output[u].extend(self.output[self.fail[u]])
    
    def search(self, text):
        state = 0
        results = []
        for i, char in enumerate(text):
            while state != 0 and char not in self.trie[state]:
                state = self.fail[state]
            if char in self.trie[state]:
                state = self.trie[state][char]
            else:
                state = 0
            
            if self.output[state]:
                for pattern_index in self.output[state]:
                    results.append((i, pattern_index))
        
        return results

if __name__ == "__main__":
    # Example usage
    ac = AhoCorasick()
    patterns = ["he", "she", "his", "hers"]
    for i, pattern in enumerate(patterns):
        ac.add_pattern(pattern, i)

    ac.build_automaton()

    text = "ushers"
    matches = ac.search(text)

    print("Matches found:")
    for position, pattern_index in matches:
        print(f"Pattern '{patterns[pattern_index]}' found ending at position {position}")

