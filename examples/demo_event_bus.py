"""
Demo: Event Bus in Action

This script demonstrates practical usage of both synchronous and asynchronous
event buses with real-world scenarios.
"""

import asyncio
import time

from core import get_logger, setup_logging
from lessons.lab_0001_event_bus.event_bus import AsyncEventBus, EventBus

# Set up logging
setup_logging(level="INFO")
logger = get_logger(__name__)


def demo_synchronous_bus():
    """Demonstrate synchronous event bus usage."""
    logger.info("=" * 60)
    logger.info("SYNCHRONOUS EVENT BUS DEMO")
    logger.info("=" * 60)

    bus = EventBus()

    # Scenario: E-commerce order processing
    def send_confirmation_email(_event, payload):
        logger.info(
            f"Sending confirmation email for order #{payload['order_id']}"
        )

    def update_inventory(_event, payload):
        logger.info(f"Updating inventory: -{payload['quantity']} items")

    def track_analytics(_event, payload):
        logger.info(f"Analytics: Order value ${payload['amount']:.2f}")

    def notify_warehouse(_event, payload):
        logger.info(
            f"Warehouse notified: Prepare order #{payload['order_id']}"
        )

    # Subscribe all handlers
    bus.subscribe("order.created", send_confirmation_email)
    bus.subscribe("order.created", update_inventory)
    bus.subscribe("order.created", track_analytics)
    bus.subscribe("order.created", notify_warehouse)

    logger.info("\nCustomer places an order...\n")

    # Publish the event
    order_data = {
        "order_id": 12345,
        "user_id": 789,
        "quantity": 3,
        "amount": 99.99,
    }

    start = time.time()
    count = bus.publish("order.created", order_data)
    elapsed = time.time() - start

    logger.info(f"\n{count} handlers executed in {elapsed * 1000:.2f}ms")
    logger.info(f"Total subscribers: {bus.count_subscribers()}")


async def demo_asynchronous_bus():
    """Demonstrate asynchronous event bus usage."""
    logger.info("\n\n" + "=" * 60)
    logger.info("ASYNCHRONOUS EVENT BUS DEMO")
    logger.info("=" * 60)

    bus = AsyncEventBus()

    # Scenario: User login with async operations
    async def fetch_user_profile(_event, payload):
        logger.info(f"Fetching profile for user {payload['user_id']}...")
        await asyncio.sleep(0.3)  # Simulate database query
        logger.info(f"Profile loaded for user {payload['user_id']}")

    async def log_login_attempt(_event, payload):
        logger.info(f"Logging login attempt from {payload['ip_address']}...")
        await asyncio.sleep(0.1)  # Simulate log write
        logger.info("Login logged")

    async def send_login_notification(_event, _payload):
        logger.info("Sending login notification...")
        await asyncio.sleep(0.2)  # Simulate push notification
        logger.info("Notification sent")

    async def update_last_seen(_event, _payload):
        logger.info("Updating last seen timestamp...")
        await asyncio.sleep(0.15)  # Simulate database update
        logger.info("Timestamp updated")

    # Subscribe all handlers
    bus.subscribe("user.login", fetch_user_profile)
    bus.subscribe("user.login", log_login_attempt)
    bus.subscribe("user.login", send_login_notification)
    bus.subscribe("user.login", update_last_seen)

    logger.info("\nUser logs in...\n")

    # Publish the event
    login_data = {
        "user_id": 42,
        "ip_address": "192.168.1.100",
        "timestamp": "2025-10-11",
    }

    start = time.time()
    count = await bus.publish("user.login", login_data)
    elapsed = time.time() - start

    msec = elapsed * 1000
    logger.info(f"\n{count} handlers executed concurrently in {msec:.2f}ms")
    logger.info("Note: Async handlers ran in parallel, not sequentially!")
    logger.info(f"Total subscribers: {bus.count_subscribers()}")


def demo_multiple_events():
    """Demonstrate multiple events and selective subscription."""
    logger.info("\n\n" + "=" * 60)
    logger.info("MULTIPLE EVENTS DEMO")
    logger.info("=" * 60)

    bus = EventBus()

    # Different handlers for different events
    def on_user_registered(_event, payload):
        logger.info(f"Welcome {payload['username']}! Account created.")

    def on_user_login(_event, payload):
        logger.info(f"Welcome back, {payload['username']}!")

    def on_user_logout(_event, payload):
        logger.info(f"Goodbye, {payload['username']}!")

    def universal_logger(event, payload):
        logger.info(f"[LOG] Event: {event} | Data: {payload}")

    # Subscribe to specific events
    bus.subscribe("user.registered", on_user_registered)
    bus.subscribe("user.login", on_user_login)
    bus.subscribe("user.logout", on_user_logout)

    # This handler listens to ALL events
    bus.subscribe("user.registered", universal_logger)
    bus.subscribe("user.login", universal_logger)
    bus.subscribe("user.logout", universal_logger)

    logger.info("\nSimulating user lifecycle events...\n")

    # Simulate user lifecycle
    bus.publish("user.registered", {"user_id": 1, "username": "alice"})
    logger.info("")
    bus.publish("user.login", {"user_id": 1, "username": "alice"})
    logger.info("")
    bus.publish("user.logout", {"user_id": 1, "username": "alice"})

    logger.info("\nEvent statistics:")
    reg_count = bus.count_subscribers("user.registered")
    login_count = bus.count_subscribers("user.login")
    logout_count = bus.count_subscribers("user.logout")
    total_count = bus.count_subscribers()
    logger.info(f"  - user.registered: {reg_count} subscribers")
    logger.info(f"  - user.login: {login_count} subscribers")
    logger.info(f"  - user.logout: {logout_count} subscribers")
    logger.info(f"  - Total: {total_count} subscribers")


def demo_dynamic_subscriptions():
    """Demonstrate dynamic subscribe/unsubscribe."""
    logger.info("\n\n" + "=" * 60)
    logger.info("DYNAMIC SUBSCRIPTIONS DEMO")
    logger.info("=" * 60)

    bus = EventBus()

    def temporary_handler(_event, _payload):
        logger.info("This handler will be removed soon!")

    def permanent_handler(_event, _payload):
        logger.info("This handler stays forever!")

    # Subscribe both handlers
    temp_sub = bus.subscribe("notification", temporary_handler)
    bus.subscribe("notification", permanent_handler)

    logger.info("\nPublishing with both handlers active:\n")
    bus.publish("notification", "First message")

    logger.info("\nRemoving temporary handler...\n")
    bus.unsubscribe(temp_sub)

    logger.info("Publishing again with only permanent handler:\n")
    bus.publish("notification", "Second message")

    logger.info("\nDemonstration complete!")


def main():
    """Run all demonstrations."""
    # Synchronous demos
    demo_synchronous_bus()
    demo_multiple_events()
    demo_dynamic_subscriptions()

    # Asynchronous demo
    asyncio.run(demo_asynchronous_bus())

    logger.info("\n\n" + "=" * 60)
    logger.info("DEMO COMPLETE")
    logger.info("=" * 60)
    logger.info("\nKey Takeaways:")
    logger.info("  1. Event buses decouple publishers from subscribers")
    logger.info("  2. Multiple handlers can react to the same event")
    logger.info("  3. Async buses enable concurrent execution")
    logger.info("  4. Subscriptions can be added/removed dynamically")
    logger.info("\nNext steps: Check out the tests and try the exercises!")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
