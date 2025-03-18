from flask import Flask, render_template, jsonify, request, Response
from event_system import EventSystem
import threading
import time
import json
import queue

app = Flask(__name__)
event_system = EventSystem()
event_logs = queue.Queue()

# Simulate subscribers with logging functions
def create_subscriber(subscriber_id, event_type):
    def subscriber(data):
        timestamp = time.strftime('%H:%M:%S')
        log_message = f"Subscriber {subscriber_id} of {event_type} executed at {timestamp}"
        print(log_message)
        
        # Add to event logs queue for SSE
        event_logs.put({
            'event_type': event_type,
            'message': log_message,
            'timestamp': timestamp,
            'subscriber_id': subscriber_id
        })
    return subscriber

# Register subscribers
for i in range(10):  # 10 subscribers for event1
    event_system.subscribe("event1", create_subscriber(i, "event1"))

for i in range(1000):  # 1000 subscribers for event2
    event_system.subscribe("event2", create_subscriber(i, "event2"))

def simulation_thread():
    # Initial event2 emission
    print("\nEmitting event2 at start")
    event_logs.put({
        'event_type': 'event2',
        'message': 'Event2 emitted with 1000 subscribers',
        'timestamp': time.strftime('%H:%M:%S'),
        'is_emission': True
    })
    event_system.emit("event2", {"message": "Initial event2"})
    
    # Emit event1 after 10 seconds
    time.sleep(10)
    print("\nEmitting event1 after 10 seconds")
    event_logs.put({
        'event_type': 'event1',
        'message': 'First Event1 emitted with 10 subscribers',
        'timestamp': time.strftime('%H:%M:%S'),
        'is_emission': True
    })
    event_system.emit("event1", {"message": "First event1"})
    
    # Emit event1 after 20 seconds from start
    time.sleep(10)
    print("\nEmitting event1 after 20 seconds")
    event_logs.put({
        'event_type': 'event1',
        'message': 'Second Event1 emitted with 10 subscribers',
        'timestamp': time.strftime('%H:%M:%S'),
        'is_emission': True
    })
    event_system.emit("event1", {"message": "Second event1"})
    
    # Emit event1 after 50 seconds from start
    time.sleep(30)
    print("\nEmitting event1 after 50 seconds")
    event_logs.put({
        'event_type': 'event1',
        'message': 'Third Event1 emitted with 10 subscribers',
        'timestamp': time.strftime('%H:%M:%S'),
        'is_emission': True
    })
    event_system.emit("event1", {"message": "Third event1"})
    
    # Add completion event
    time.sleep(20)  # Wait for processing to complete
    event_logs.put({
        'event_type': 'system',
        'message': 'Simulation completed',
        'timestamp': time.strftime('%H:%M:%S'),
        'is_emission': True
    })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-simulation')
def start_simulation():
    threading.Thread(target=simulation_thread).start()
    return jsonify({"status": "success", "message": "Simulation started"})

@app.route('/events')
def events():
    def generate():
        while True:
            try:
                # Get event from queue with timeout
                event = event_logs.get(timeout=1)
                yield f"data: {json.dumps(event)}\n\n"
            except queue.Empty:
                # Send a heartbeat to keep the connection alive
                yield f"data: {json.dumps({'event_type': 'heartbeat'})}\n\n"
            time.sleep(0.1)  # Small delay to prevent CPU overuse
    
    return Response(generate(), mimetype="text/event-stream")

@app.route('/status')
def status():
    # Return current status of event processing
    event1_subscribers = len(event_system.subscribers.get("event1", []))
    event2_subscribers = len(event_system.subscribers.get("event2", []))
    
    return jsonify({
        "event1_subscribers": event1_subscribers,
        "event2_subscribers": event2_subscribers,
        "is_processing_low_priority": event_system.is_processing_low_priority
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
