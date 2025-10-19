"""
Synchronous Event Bus Implementation

A publish/subscribe system that allows components to communicate without tight coupling.
Handlers are called synchronously in the order they were registered.
"""

import logging
from collections.abc import Callable
from typing import Any
from uuid import uuid4

logger = logging.getLogger(__name__)


class EventBus:
    """
    A synchronous event bus for publish/subscribe communication.

    The EventBus allows components to subscribe to events and publish messages
    to those subscribers without direct coupling between components.

    Examples:
        >>> bus = EventBus()
        >>> def handler(event: str, payload: dict):
        ...     logger.info(f"Received {event}: {payload}")
        >>> sub_id = bus.subscribe("user.login", handler)
        >>> bus.publish("user.login", {"user_id": 123})
        >>> bus.unsubscribe(sub_id)
        >>> bus.publish("user.login", {"user_id": 456})  # No output
    """

    def __init__(self):
        """Initialize an empty event bus."""
        self._subscribers: dict[str, dict[str, Callable]] = {}
        assert isinstance(
            self._subscribers, dict
        ), "Subscribers must be a dictionary"
        assert (
            len(self._subscribers) == 0
        ), "New bus should have no subscribers"

    def subscribe(
        self, event: str, handler: Callable[[str, Any], None]
    ) -> str:
        """
        Subscribe a handler to an event.

        Args:
            event: The event name to subscribe to (e.g., "user.login")
            handler: A callable that accepts (event: str, payload: Any)

        Returns:
            A subscription ID that can be used to unsubscribe

        Raises:
            AssertionError: If event is not a string or handler is not callable

        Examples:
            >>> bus = EventBus()
            >>> def my_handler(event, payload):
            ...     pass
            >>> sub_id = bus.subscribe("order.created", my_handler)
            >>> isinstance(sub_id, str)
            True
        """
        assert isinstance(event, str), "Event must be a string"
        assert len(event) > 0, "Event name cannot be empty"
        assert callable(handler), "Handler must be callable"

        # Create subscription ID
        sub_id = str(uuid4())

        # Initialize event list if needed
        if event not in self._subscribers:
            self._subscribers[event] = {}

        # Store the handler
        self._subscribers[event][sub_id] = handler

        assert sub_id in self._subscribers[event], "Handler must be registered"
        assert (
            self._subscribers[event][sub_id] is handler
        ), "Handler must match"

        return sub_id

    def unsubscribe(self, subscription_id: str) -> bool:
        """
        Unsubscribe a handler using its subscription ID.

        Args:
            subscription_id: The ID returned by subscribe()

        Returns:
            True if a handler was removed, False if ID not found

        Raises:
            AssertionError: If subscription_id is not a string

        Examples:
            >>> bus = EventBus()
            >>> sub_id = bus.subscribe("test", lambda e, p: None)
            >>> bus.unsubscribe(sub_id)
            True
            >>> bus.unsubscribe(sub_id)
            False
        """
        assert isinstance(
            subscription_id, str
        ), "Subscription ID must be a string"
        assert len(subscription_id) > 0, "Subscription ID cannot be empty"

        # Search all events for this subscription
        for event, handlers in self._subscribers.items():
            if subscription_id in handlers:
                del handlers[subscription_id]

                # Clean up empty event entries
                if len(handlers) == 0:
                    del self._subscribers[event]

                assert (
                    subscription_id not in handlers
                ), "Handler must be removed"
                return True

        assert subscription_id not in [
            sub_id
            for handlers in self._subscribers.values()
            for sub_id in handlers.keys()
        ], "Subscription ID must not exist after failed removal"

        return False

    def publish(self, event: str, payload: Any = None) -> int:
        """
        Publish an event to all subscribers.

        Handlers are called synchronously in an undefined order.

        Args:
            event: The event name to publish
            payload: Optional data to pass to handlers

        Returns:
            The number of handlers that were called

        Raises:
            AssertionError: If event is not a string

        Examples:
            >>> bus = EventBus()
            >>> count = 0
            >>> def increment(e, p):
            ...     global count
            ...     count += 1
            >>> bus.subscribe("test", increment)
            '...'
            >>> bus.publish("test")
            1
            >>> count
            1
        """
        assert isinstance(event, str), "Event must be a string"
        assert len(event) > 0, "Event name cannot be empty"

        # Get handlers for this event
        handlers = self._subscribers.get(event, {})
        handler_count = len(handlers)

        # Call each handler
        for handler in handlers.values():
            handler(event, payload)

        assert handler_count >= 0, "Handler count must be non-negative"

        return handler_count

    def clear(self) -> None:
        """
        Remove all subscriptions from the bus.

        Examples:
            >>> bus = EventBus()
            >>> bus.subscribe("test", lambda e, p: None)
            '...'
            >>> bus.clear()
            >>> bus.count_subscribers()
            0
        """
        self._subscribers.clear()

        assert len(self._subscribers) == 0, "All subscribers must be removed"
        assert self.count_subscribers() == 0, "Count must be zero after clear"

    def count_subscribers(self, event: str | None = None) -> int:
        """
        Count the number of subscribers.

        Args:
            event: Optional event name to count subscribers for.
                   If None, returns total count across all events.

        Returns:
            The number of subscribers

        Raises:
            AssertionError: If event is provided but not a string

        Examples:
            >>> bus = EventBus()
            >>> bus.subscribe("event1", lambda e, p: None)
            '...'
            >>> bus.subscribe("event1", lambda e, p: None)
            '...'
            >>> bus.subscribe("event2", lambda e, p: None)
            '...'
            >>> bus.count_subscribers()
            3
            >>> bus.count_subscribers("event1")
            2
        """
        if event is not None:
            assert isinstance(event, str), "Event must be a string"
            count = len(self._subscribers.get(event, {}))
        else:
            count = sum(
                len(handlers) for handlers in self._subscribers.values()
            )

        assert count >= 0, "Count must be non-negative"
        return count
