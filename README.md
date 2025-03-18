# Event System with Priority Handling

This application demonstrates an event system with priority handling for different types of events and subscribers. It showcases how to implement a system where high-priority events can interrupt low-priority event processing.

## System Features

- **Two Event Types**:
  - **Event1**: High priority with 10 subscribers
  - **Event2**: Low priority with 1000 subscribers

- **Priority Handling**:
  - High priority events (event1) are processed immediately
  - Low priority events (event2) are processed in batches of 20 subscribers
  - High priority events can interrupt low priority processing

- **Token System Integration**:
  - Displays token values based on the configured exchange rate (1 TKN = £520.00)
  - Shows both token and fiat currency values
  - Implements minimum bid increment of 5%

## Requirements

- Python 3.7+
- Flask

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:

```bash
python app.py
```

2. Open your browser and navigate to:

```
http://localhost:5000
```

3. Click the "Start Simulation" button to begin the demonstration

## Simulation Timeline

The simulation follows this timeline:
- T+0s: Event2 is emitted (1000 subscribers)
- T+10s: First Event1 is emitted (10 subscribers)
- T+20s: Second Event1 is emitted (10 subscribers)
- T+50s: Third Event1 is emitted (10 subscribers)

## Implementation Details

The application consists of:

1. **Event System**: Core implementation of the priority-based event system
2. **Flask Backend**: Handles HTTP requests and manages the simulation
3. **Interactive Frontend**: Visualizes the events and their processing in real-time

## Architecture

- **event_system.py**: Contains the EventSystem class that manages subscribers and event processing
- **app.py**: Flask application that provides API endpoints and runs the simulation
- **templates/index.html**: Frontend interface with real-time visualization

## How It Works

1. When a high-priority event is emitted, it pauses any ongoing low-priority processing
2. High-priority subscribers are notified immediately
3. After high-priority processing completes, low-priority processing resumes
4. Low-priority events are processed in batches to allow for interruption

This demonstrates how to implement a system that can handle different priority levels while ensuring that high-priority events are processed promptly.
#   E r i c - E v e n t C h a l l e n g e  
 