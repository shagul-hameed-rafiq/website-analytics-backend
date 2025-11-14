# processor/worker.py
import time
import sys
from pathlib import Path

# ensure project root on path (helps when running as script)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from event_queue.queue_client import pop
from database.db import init_db, insert_event

def process_event(event):
    # write to sqlite
    try:
        event_id = insert_event(event)
        print(f"Processed and stored event id={event_id}")
    except Exception as e:
        print("Error storing event:", e)

def main_loop():
    while True:
        event = pop()
        if event:
            try:
                process_event(event)
            except Exception as e:
                print("Error processing event:", e)
        else:
            time.sleep(0.1)

if __name__ == "__main__":
    # create DB / tables if they don't exist
    init_db()
    print("Worker started. Waiting for events...")
    main_loop()
