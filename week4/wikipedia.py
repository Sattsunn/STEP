from collections import deque
import sys
import collections
import numpy as np

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # idとtitleを逆にした辞書
        self.inverse_titles = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)

        # 逆の辞書を作成 
        self.inverse_titles = {v: k for k, v in self.titles.items()}
        print("Finished creating inverse_title")
        print()

    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        start_id = self.inverse_titles[start]
        goal_id = self.inverse_titles[goal]
        queue = deque()
        visited = {}
        path = {}
        visited[start_id] = True
        queue.append(start_id)
        while len(queue)!=0:
            node = queue.popleft()
            if node == goal_id:
                shortest_path = []
                while node is not None:
                    shortest_path.append(self.titles[node])
                    node = path.get(node)
                print("The shortest path is:")
                print(list(reversed(shortest_path)))
                return 
            for child in self.links[node]:
                if child not in visited:
                    visited[child] = True
                    path[child] = node
                    queue.append(child)
        print("There is no path between %s and %s" % (start, goal))
        return "Not found"
    
    # 辞書の中身をコメントで残す



        # Calculate the page ranks and print the most popular pages.

        # 辞書より配列を使う
        # 

    def find_most_popular_pages(self, damping_factor=0.85, epsilon=1e-6, max_iterations=100):
        num_nodes = len(self.titles)

        # ノードIDの範囲を1から始める
        incoming_links = {node_id: [] for node_id in range(1, num_nodes+1)}

        # 各ノードへの入力リンクを記録
        for src_node, dst_nodes in self.links.items():
            if src_node in incoming_links:
                for dst_node in dst_nodes:
                    if dst_node in incoming_links:
                        incoming_links[dst_node].append(src_node)

        # 初期ページランクを1に設定
        page_ranks = np.full(num_nodes, 1)

        # ページランクの計算（最大100回まで）
        count = 0
        for _ in range(max_iterations):
            count += 1
            print(count)
            new_page_ranks = np.zeros(num_nodes)

            # 各ノードのページランクを更新
            for node in range(1, num_nodes+1):
                if node in self.links and node in self.titles:
                
                    incoming_pr = 0

                    # 隣接ノードからの寄与を計算
                    for incoming_node in incoming_links[node]:
                        if incoming_node in self.titles:
                            incoming_pr += damping_factor * page_ranks[incoming_node-1] / len(self.links[incoming_node])

                    # 残りの確率を均等に分配
                    incoming_pr = (1 - damping_factor) / num_nodes + damping_factor * incoming_pr
                    new_page_ranks[node-1] = incoming_pr

            # 収束判定
            if np.linalg.norm(new_page_ranks - page_ranks, ord=np.inf) < epsilon:
                break
            
            page_ranks = new_page_ranks

        # 上位10件のページランクを出力
        print("The top 10 most popular pages are:")
        sorted_indices = [index for index in range(1, num_nodes+1) if index in self.titles]
        sorted_indices = sorted(sorted_indices, key=lambda x: page_ranks[x-1], reverse=True)
        for index in sorted_indices[:10]:
            print(f"{self.titles[index]}: {page_ranks[index-1]:.6f}")
        print()


    # Do something more interesting!!
    def find_something_more_interesting(self):
        # リンクが一つしかないのを探す予定だったがあまり面白くなかったので没
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The least linked pages are:")
        link_count_min = 1
        for dst in link_count.keys():
            if link_count[dst] == link_count_min:
                print(self.titles[dst], link_count_min)
        print()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    wikipedia.find_longest_titles()
    wikipedia.find_most_linked_pages()
    wikipedia.find_shortest_path("ヨーロッパ", "生物")
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    wikipedia.find_shortest_path("渋谷", "小野妹子")
    wikipedia.find_shortest_path("男らしさ", "女装")
    wikipedia.find_shortest_path("シェラトン・タワーズ・シンガポール", "CONCONJUMP")
    wikipedia.find_most_popular_pages()
    # wikipedia.find_something_more_interesting()