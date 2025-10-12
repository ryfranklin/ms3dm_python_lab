"""
Asynchronous Event Bus Implementation

An async/await compatible publish/subscribe system for asynchronous event handling.
Handlers are called concurrently using asyncio.
"""

import asyncio
from collections.abc import Callable, Coroutine
from typing import Any
from uuid import uuid4


class AsyncEventBus:
    """
    An asynchronous event bus for publish/subscribe communication.

    Similar to EventBus, but handlers can be async functions and are
    executed concurrently.

    Examples:
        >>> import asyncio
        >>> bus = AsyncEventBus()
        >>> async def handler(event: str, payload: dict):
        ...     print(f"Received {event}: {payload}")
        >>> sub_id = bus.subscribe("user.login", handler)
        >>> asyncio.run(bus.publish("user.login", {"user_id": 123}))
        Received user.login: {'user_id': 123}
        1
    """

    def __init__(self):
        """Initialize an empty async event bus."""
        self._subscribers: dict[str, dict[str, Callable]] = {}
        assert isinstance(
            self._subscribers, dict
        ), "Subscribers must be a dictionary"
        assert (
            len(self._subscribers) == 0
        ), "New bus should have no subscribers"

    def subscribe(
        self,
        event: str,
        handler: Callable[[str, Any], Coroutine[Any, Any, None]],
    ) -> str:
        """
        Subscribe an async handler to an event.

        Args:
            event: The event name to subscribe to
            handler: An async callable that accepts (event: str, payload: Any)

        Returns:
            A subscription ID that can be used to unsubscribe

        Raises:
            AssertionError: If event is not a string or handler is not callable

        Examples:
            >>> bus = AsyncEventBus()
            >>> async def my_handler(event, payload):
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
            >>> bus = AsyncEventBus()
            >>> async def handler(e, p):
            ...     pass
            >>> sub_id = bus.subscribe("test", handler)
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

        return False

    async def publish(self, event: str, payload: Any = None) -> int:
        """
        Publish an event to all subscribers asynchronously.

        All handlers are called concurrently using asyncio.gather().

        Args:
            event: The event name to publish
            payload: Optional data to pass to handlers

        Returns:
            The number of handlers that were called

        Raises:
            AssertionError: If event is not a string

        Examples:
            >>> import asyncio
            >>> bus = AsyncEventBus()
            >>> results = []
            >>> async def handler(e, p):
            ...     results.append(p)
            >>> bus.subscribe("test", handler)
            '...'
            >>> asyncio.run(bus.publish("test", {"data": 123}))
            1
        """
        assert isinstance(event, str), "Event must be a string"
        assert len(event) > 0, "Event name cannot be empty"

        # Get handlers for this event
        handlers = self._subscribers.get(event, {})
        handler_count = len(handlers)

        # Call all handlers concurrently
        if handler_count > 0:
            tasks = [handler(event, payload) for handler in handlers.values()]
            await asyncio.gather(*tasks)

        assert handler_count >= 0, "Handler count must be non-negative"

        return handler_count

    def clear(self) -> None:
        """
        Remove all subscriptions from the bus.

        Examples:
            >>> bus = AsyncEventBus()
            >>> async def handler(e, p):
            ...     pass
            >>> bus.subscribe("test", handler)
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
            >>> bus = AsyncEventBus()
            >>> async def handler(e, p):
            ...     pass
            >>> bus.subscribe("event1", handler)
            '...'
            >>> bus.subscribe("event1", handler)
            '...'
            >>> bus.subscribe("event2", handler)
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
