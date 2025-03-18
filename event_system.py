import time
import threading
import queue
from typing import Callable, Dict, List, Any
from collections import defaultdict

class EventSystem:
    def __init__(self):
        self.subscribers = defaultdict(list)
        self.low_priority_queue = queue.Queue()
        self.is_processing_low_priority = False
        self.batch_size = 20
        self.current_batch = []
        self.lock = threading.Lock()
        self.processed_subscribers = {
            "event1": 0,
            "event2": 0
        }
        self.total_subscribers = {
            "event1": 0,
            "event2": 0
        }
        self.pause_low_priority = threading.Event()
        self.pause_low_priority.set()  # Initially not paused
        
    def subscribe(self, event_type: str, callback: Callable):
        """Subscribe a callback function to an event type"""
        self.subscribers[event_type].append(callback)
        self.total_subscribers[event_type] = len(self.subscribers[event_type])
        
    def emit(self, event_type: str, data: Any = None):
        """Emit an event with optional data"""
        if event_type == "event1":  # High priority
            # Pause low priority processing if it's running
            self.pause_low_priority.clear()
            # Process high priority event
            self._process_high_priority(event_type, data)
            # Resume low priority processing
            self.pause_low_priority.set()
        else:  # Low priority
            self.low_priority_queue.put((event_type, data))
            if not self.is_processing_low_priority:
                threading.Thread(target=self._process_low_priority_queue, daemon=True).start()
                
    def _process_high_priority(self, event_type: str, data: Any = None):
        """Process high priority events immediately"""
        with self.lock:
            print(f"\n[HIGH PRIORITY] Processing event: {event_type} with {len(self.subscribers[event_type])} subscribers")
            for i, subscriber in enumerate(self.subscribers[event_type]):
                start_time = time.time()
                subscriber(data)
                self.processed_subscribers[event_type] += 1
                processing_time = time.time() - start_time
                print(f"  - Subscriber {i} processed in {processing_time:.2f}s")
                time.sleep(max(0, 1 - processing_time))  # Ensure 1 second total processing time
                
    def _process_low_priority_queue(self):
        """Process low priority events in batches"""
        self.is_processing_low_priority = True
        
        while not self.low_priority_queue.empty():
            event_type, data = self.low_priority_queue.get()
            batch_subscribers = self.subscribers[event_type]
            
            for i in range(0, len(batch_subscribers), self.batch_size):
                # Wait if high priority event is being processed
                self.pause_low_priority.wait()
                
                with self.lock:
                    batch = batch_subscribers[i:i + self.batch_size]
                    batch_end = min(i + self.batch_size, len(batch_subscribers))
                    print(f"\n[LOW PRIORITY] Processing batch for {event_type} (subscribers {i}-{batch_end-1})")
                    
                    for j, subscriber in enumerate(batch):
                        start_time = time.time()
                        subscriber(data)
                        self.processed_subscribers[event_type] += 1
                        processing_time = time.time() - start_time
                        print(f"  - Subscriber {i+j} processed in {processing_time:.2f}s")
                        time.sleep(max(0, 1 - processing_time))  # Ensure 1 second total processing time
        
        self.is_processing_low_priority = False
    
    def get_status(self):
        """Get the current status of event processing"""
        return {
            "processed": self.processed_subscribers,
            "total": self.total_subscribers,
            "is_processing_low_priority": self.is_processing_low_priority
        }
