import queue

_q = queue.Queue(maxsize=10000)

def enqueue(item):
    _q.put(item)

def dequeue():
    if _q.empty():
        return None
    return _q.get()
