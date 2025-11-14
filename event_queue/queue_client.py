from queue import Queue

# global shared queue
event_queue = Queue()

def push(event):
    """Put an event into the in-memory queue."""
    event_queue.put(event)

def pop():
    """Try to pop an event without blocking. Return None if empty."""
    try:
        return event_queue.get(block=False)
    except Exception:
        return None
