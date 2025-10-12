# Lab 0001: Event Bus

**Status**: ✅ Complete  
**Difficulty**: Beginner to Intermediate  
**Concepts**: Observer Pattern, Pub/Sub, Async/Await, Defensive Programming

## 🎯 Learning Objectives

By the end of this lab, you will understand:

- ✅ The Observer Pattern and publish/subscribe (pub/sub) architecture
- ✅ How to decouple components using event-driven communication
- ✅ Synchronous vs. asynchronous event handling
- ✅ Defensive programming with assertions
- ✅ Test-driven development with pytest
- ✅ Working with `asyncio` and concurrent execution

## 📚 What is an Event Bus?

An **Event Bus** is a design pattern that enables decoupled communication between components:

- **Publishers** emit events (e.g., `order.created`, `user.logged_in`)
- **Subscribers** register handlers to react to those events
- **The Event Bus** routes messages from publishers to subscribers

This pattern is used in many frameworks and systems:
- Django signals
- Node.js EventEmitter
- Enterprise message brokers (Kafka, RabbitMQ)
- GUI frameworks (Qt signals/slots)

### Why Use an Event Bus?

**Without an Event Bus:**
```python
def create_order(user_id, items):
    order = Order.create(user_id, items)
    
    # Tightly coupled dependencies
    email_service.send_confirmation(order)
    analytics.track_order(order)
    inventory.update_stock(order)
    # What if we need to add more actions?
```

**With an Event Bus:**
```python
def create_order(user_id, items):
    order = Order.create(user_id, items)
    
    # Loose coupling - just publish the event
    bus.publish("order.created", order)
    # Other components subscribe independently
```

## 🏗️ Architecture

This lab includes two implementations:

### 1. `EventBus` (Synchronous)
- Handlers execute one at a time
- Simple and predictable execution order
- Best for quick operations

### 2. `AsyncEventBus` (Asynchronous)
- Handlers execute concurrently with `asyncio`
- Better performance for I/O-bound operations
- Modern async/await syntax

## 🚀 Quick Start

### Installation

```bash
# From the repository root
cd lessons/lab_0001_event_bus
```

### Basic Usage - Synchronous

```python
from event_bus import EventBus

# Create a bus
bus = EventBus()

# Define handlers
def log_handler(event, payload):
    print(f"[LOG] {event}: {payload}")

def analytics_handler(event, payload):
    print(f"[ANALYTICS] Tracking: {event}")

# Subscribe handlers to events
sub1 = bus.subscribe("user.login", log_handler)
sub2 = bus.subscribe("user.login", analytics_handler)

# Publish an event
bus.publish("user.login", {"user_id": 123, "timestamp": "2025-10-11"})

# Output:
# [LOG] user.login: {'user_id': 123, 'timestamp': '2025-10-11'}
# [ANALYTICS] Tracking: user.login

# Unsubscribe when done
bus.unsubscribe(sub1)
```

### Basic Usage - Asynchronous

```python
import asyncio
from event_bus import AsyncEventBus

# Create an async bus
bus = AsyncEventBus()

# Define async handlers
async def fetch_user_data(event, payload):
    # Simulate async I/O operation
    await asyncio.sleep(0.1)
    print(f"Fetched data for user {payload['user_id']}")

async def send_notification(event, payload):
    # Simulate async I/O operation
    await asyncio.sleep(0.1)
    print(f"Sent notification to user {payload['user_id']}")

# Subscribe handlers
bus.subscribe("user.login", fetch_user_data)
bus.subscribe("user.login", send_notification)

# Publish an event (must await)
await bus.publish("user.login", {"user_id": 123})

# Both handlers run concurrently!
```

## 🔍 Key Features

### 1. Subscribe and Unsubscribe
```python
# Subscribe returns a unique ID
sub_id = bus.subscribe("event.name", handler_function)

# Use the ID to unsubscribe
bus.unsubscribe(sub_id)
```

### 2. Multiple Subscribers
```python
# Multiple handlers can listen to the same event
bus.subscribe("order.created", send_email)
bus.subscribe("order.created", update_inventory)
bus.subscribe("order.created", track_analytics)

# All three handlers will be called when the event is published
bus.publish("order.created", order_data)
```

### 3. Event Isolation
```python
# Handlers only receive events they subscribe to
bus.subscribe("user.login", login_handler)
bus.subscribe("user.logout", logout_handler)

bus.publish("user.login", data)  # Only login_handler is called
```

### 4. Count Subscribers
```python
# Total subscribers across all events
total = bus.count_subscribers()

# Subscribers for a specific event
count = bus.count_subscribers("user.login")
```

### 5. Clear All Subscriptions
```python
# Remove all handlers at once
bus.clear()
```

## 🛡️ Defensive Programming

This implementation uses **assertions** to catch bugs early:

```python
# Event name must be a string
bus.subscribe(123, handler)  # AssertionError!

# Handler must be callable
bus.subscribe("event", "not a function")  # AssertionError!

# Subscription ID must be valid
bus.unsubscribe("")  # AssertionError!
```

Every method includes multiple assertions to validate:
- Input types (strings, callables)
- State invariants (counts, registrations)
- Postconditions (handlers added/removed correctly)

## 🧪 Running Tests

This lab includes comprehensive test coverage:

```bash
# Run all tests
pytest

# Run only sync bus tests
pytest tests/test_sync_bus.py

# Run only async bus tests
pytest tests/test_async_bus.py

# Run with coverage
pytest --cov=event_bus --cov-report=term-missing

# Run with verbose output
pytest -v
```

Test coverage includes:
- ✅ Basic functionality (subscribe, publish, unsubscribe)
- ✅ Multiple handlers and events
- ✅ Edge cases (empty events, no subscribers)
- ✅ Input validation and assertions
- ✅ Async concurrency behavior
- ✅ Error propagation

## 💡 Exercises

Try these challenges to deepen your understanding:

### Exercise 1: Priority Handlers
Modify the EventBus to support priority levels. High-priority handlers should execute first.

### Exercise 2: Event Filtering
Add support for wildcard subscriptions (e.g., `user.*` matches `user.login` and `user.logout`).

### Exercise 3: Event History
Implement a method to retrieve the last N events published to the bus.

### Exercise 4: Middleware
Add support for middleware functions that can intercept and transform events before handlers receive them.

### Exercise 5: Error Handling
Modify the async bus to continue executing other handlers even if one raises an exception.

## 🌟 Real-World Applications

Event buses are used in:

1. **Web Applications**: Handle user actions (clicks, form submissions) without tightly coupling UI to business logic
2. **Microservices**: Services communicate via events rather than direct API calls
3. **Plugin Systems**: Plugins subscribe to application events to extend functionality
4. **Game Development**: Game entities react to events (collision, state changes) independently
5. **IoT Systems**: Devices publish sensor data; services subscribe to process it

## 📖 Further Reading

- [Observer Pattern - Refactoring Guru](https://refactoring.guru/design-patterns/observer)
- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html)
- [Defensive Programming Best Practices](https://en.wikipedia.org/wiki/Defensive_programming)

## 🎓 Teaching Notes

This lab is ideal for:
- **Blog post**: "Building a Pub/Sub System from Scratch in Python"
- **Video tutorial**: Live coding session with TDD approach
- **Course module**: Design patterns or async programming course
- **Interview prep**: Common system design question

**Estimated time**: 2-3 hours for implementation and testing

---

[← Back to Main README](../../README.md) | [View Examples →](../../examples/demo_event_bus.py) | [Open Notebook →](../../notebooks/Lab_0001_EventBus.ipynb)

