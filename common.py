import heapq


# Common functions, used in several of the solutions
def get_input(path):
    file = open(path, "r")
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\n", "")
    file.close()
    return lines


def dijkstra(nodes, edges, start_node):
    dist = {}
    prev = {}
    queue = PriorityQueue()
    for node in nodes:
        dist[node] = float("inf")
        prev[node] = []
        queue.add(node, priority=float("inf"))
    dist[start_node] = 0
    queue.add(start_node, priority=0)

    while len(queue) > 0:
        selected_node = queue.pop()

        for neighbor, edge_cost in edges[selected_node].items():
            alt_dist = dist[selected_node] + edge_cost
            if alt_dist < dist[neighbor]:
                dist[neighbor] = alt_dist
                prev[neighbor].append(selected_node)
                queue.add(neighbor, priority=alt_dist)

    return dist, prev


class PriorityQueue:
    def __init__(self):
        self.queue = []  # Queue entries arranged in a heap
        self.entry_finder = {}  # Mapping of items to entries
        self.REMOVED = None  # Placeholder for removed task

    def add(self, item, priority=0):
        if item in self.entry_finder:
            self.remove(item)
        entry = Entry(item, priority)
        self.entry_finder[item] = entry
        heapq.heappush(self.queue, entry)

    def remove(self, item):
        entry = self.entry_finder.pop(item)
        entry.item = self.REMOVED

    def pop(self):
        while self.queue:
            item = heapq.heappop(self.queue).item
            if not item == self.REMOVED:
                del self.entry_finder[item]
                return item

    def __len__(self):
        return len(self.entry_finder)


class Entry:
    def __init__(self, item, priority):
        self.item = item
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority
