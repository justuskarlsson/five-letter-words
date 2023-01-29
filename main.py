from collections import defaultdict, deque
from pathlib import Path

def word_to_num(word):
    num = 0
    for char in word:
        idx = ord(char) - ord('a')
        num |= (1 << idx)
    return num

def num_to_chars(num):
    chars = []
    for idx in range(26):
        if num & (1 << idx):
            chars.append(chr(ord('a') + idx))
    return chars


num_to_word = defaultdict(list)
# Appeared in solution, don't like it
banned_words = {"fldxt", "crwth", "fdubs", "vejoz"}
def load_words():
    repo = Path(__file__).parent
    with open(repo / 'words_alpha.txt') as word_file:
        valid_words = word_file.read().split()
    
    filtered = set()
    first = True

    for word in valid_words:
        if len(word) == 5 and len(set(word)) == 5:
            if word in banned_words:
                continue
            # 0b000000010000100010100 (length 26, 5 bits on)
            num = word_to_num(word.lower())
            if first:
                print("--- Sanity check ---")
                print(f"{word} -> {num} = 0b{num:0b} = {num_to_chars(num)}")
                first = False
            num_to_word[num].append(word)
            filtered.add(num)

    return filtered

def graph(nodes):
    # Time complexity: 640k * 1000 = 640M

    # nodes: Set of vertices.
    
    # Edge E between vertices(u, v) if u & v == 0
    # V = 5 K
    # E = 25 M, worst case

    adj = defaultdict(list)
    for v in nodes:
        for u in nodes:
            if u & v == 0:
                adj[v].append(u)

    # Average number of edges per node: E(V) = 1075.35 
    # s = sum([len(l) for l in adj.values()])
    # print("Average neighbors per node:" s / len(nodes)) 
    
    q = deque([])
    for v in nodes:
        q.append((v, v, 1))
    
    # Max 2^26 insertions, but for this data 640k
    visited = set()
    
    # For tracability of solution
    trace = dict()
    best = 1
    best_aggr = -1
    last_num = -1
    while q:
        v, aggr, cnt = q.popleft()
        if cnt > best:
            best = cnt
            best_aggr = aggr
            last_num = v
        for u in adj[v]:
            if aggr & u:
                continue

            new_aggr = u | aggr
            if new_aggr in visited:
                continue
            visited.add(new_aggr)
            q.append((u, new_aggr, cnt + 1))
            trace[new_aggr] = (aggr, v)

    words = [num_to_word[last_num]]
    aggr = best_aggr
    while aggr in trace:
        aggr, v = trace[aggr]
        words.append(num_to_word[v])

    print("Solution (pick any word you want for each row):")
    for word_list in words:
        print(" ".join(word_list))
    return words

if __name__ == '__main__':
    from time import time
    start = time()
    nums = load_words()
    print("Num words:", len(nums))
    graph(nums)
    elapsed = time() - start
    print(f"Took {elapsed} seconds")