"""
Tests for the asynchronous AsyncEventBus implementation.
"""

import asyncio

import pytest

from lessons.lab_0001_event_bus.event_bus import AsyncEventBus


class TestAsyncEventBusBasics:
    """Test basic AsyncEventBus functionality."""

    def test_initialization(self):
        """Test that a new AsyncEventBus starts empty."""
        bus = AsyncEventBus()
        assert bus.count_subscribers() == 0

    def test_subscribe_returns_id(self):
        """Test that subscribe returns a subscription ID."""
        bus = AsyncEventBus()

        async def handler(_e, _p):
            pass

        sub_id = bus.subscribe("test.event", handler)

        assert isinstance(sub_id, str)
        assert len(sub_id) > 0

    def test_subscribe_increments_count(self):
        """Test that subscribing increases the subscriber count."""
        bus = AsyncEventBus()

        async def handler(_e, _p):
            pass

        assert bus.count_subscribers() == 0
        bus.subscribe("test.event", handler)
        assert bus.count_subscribers() == 1
        bus.subscribe("test.event", handler)
        assert bus.count_subscribers() == 2

    def test_count_subscribers_by_event(self):
        """Test counting subscribers for specific events."""
        bus = AsyncEventBus()

        async def handler(_e, _p):
            pass

        bus.subscribe("event1", handler)
        bus.subscribe("event1", handler)
        bus.subscribe("event2", handler)

        assert bus.count_subscribers("event1") == 2
        assert bus.count_subscribers("event2") == 1
        assert bus.count_subscribers("event3") == 0
        assert bus.count_subscribers() == 3


class TestAsyncEventBusPublish:
    """Test publishing events asynchronously."""

    @pytest.mark.asyncio
    async def test_publish_to_single_handler(self):
        """Test publishing an event to a single async handler."""
        bus = AsyncEventBus()
        results = []

        async def handler(event, payload):
            results.append((event, payload))

        bus.subscribe("test.event", handler)
        count = await bus.publish("test.event", {"data": 123})

        assert count == 1
        assert len(results) == 1
        assert results[0] == ("test.event", {"data": 123})

    @pytest.mark.asyncio
    async def test_publish_to_multiple_handlers(self):
        """Test publishing to multiple async handlers."""
        bus = AsyncEventBus()
        results = []

        async def handler1(_event, payload):
            results.append(f"h1:{payload}")

        async def handler2(_event, payload):
            results.append(f"h2:{payload}")

        bus.subscribe("test.event", handler1)
        bus.subscribe("test.event", handler2)
        count = await bus.publish("test.event", "data")

        assert count == 2
        assert len(results) == 2
        assert "h1:data" in results
        assert "h2:data" in results

    @pytest.mark.asyncio
    async def test_publish_with_no_subscribers(self):
        """Test publishing to an event with no subscribers."""
        bus = AsyncEventBus()
        count = await bus.publish("no.subscribers")

        assert count == 0

    @pytest.mark.asyncio
    async def test_publish_without_payload(self):
        """Test publishing without a payload."""
        bus = AsyncEventBus()
        results = []

        async def handler(_event, payload):
            results.append(payload)

        bus.subscribe("test.event", handler)
        await bus.publish("test.event")

        assert len(results) == 1
        assert results[0] is None

    @pytest.mark.asyncio
    async def test_publish_only_notifies_correct_event(self):
        """Test that publishing only notifies handlers for specific event."""
        bus = AsyncEventBus()
        event1_called = []
        event2_called = []

        async def handler1(_e, p):
            event1_called.append(p)

        async def handler2(_e, p):
            event2_called.append(p)

        bus.subscribe("event1", handler1)
        bus.subscribe("event2", handler2)

        await bus.publish("event1", "data1")

        assert len(event1_called) == 1
        assert len(event2_called) == 0

        await bus.publish("event2", "data2")

        assert len(event1_called) == 1
        assert len(event2_called) == 1

    @pytest.mark.asyncio
    async def test_handlers_run_concurrently(self):
        """Test that multiple handlers run concurrently."""
        bus = AsyncEventBus()
        execution_order = []

        async def slow_handler(_event, _payload):
            execution_order.append("slow_start")
            await asyncio.sleep(0.1)
            execution_order.append("slow_end")

        async def fast_handler(_event, _payload):
            execution_order.append("fast_start")
            await asyncio.sleep(0.01)
            execution_order.append("fast_end")

        bus.subscribe("test.event", slow_handler)
        bus.subscribe("test.event", fast_handler)

        await bus.publish("test.event")

        # If concurrent, fast should finish before slow
        # Both should start before either finishes
        assert execution_order[0] in ["slow_start", "fast_start"]
        assert execution_order[1] in ["slow_start", "fast_start"]
        assert "fast_end" in execution_order
        assert "slow_end" in execution_order


class TestAsyncEventBusUnsubscribe:
    """Test unsubscribing from events."""

    @pytest.mark.asyncio
    async def test_unsubscribe_removes_handler(self):
        """Test that unsubscribe removes a handler."""
        bus = AsyncEventBus()
        results = []

        async def handler(_e, p):
            results.append(p)

        sub_id = bus.subscribe("test.event", handler)
        await bus.publish("test.event", "before")

        assert bus.unsubscribe(sub_id) is True
        await bus.publish("test.event", "after")

        assert len(results) == 1
        assert results[0] == "before"

    def test_unsubscribe_decrements_count(self):
        """Test that unsubscribe decreases the subscriber count."""
        bus = AsyncEventBus()

        async def handler(_e, _p):
            pass

        sub_id = bus.subscribe("test.event", handler)
        assert bus.count_subscribers() == 1

        bus.unsubscribe(sub_id)
        assert bus.count_subscribers() == 0

    def test_unsubscribe_nonexistent_id(self):
        """Test unsubscribing with an invalid ID."""
        bus = AsyncEventBus()
        result = bus.unsubscribe("nonexistent-id")

        assert result is False

    def test_unsubscribe_same_id_twice(self):
        """Test unsubscribing the same ID twice."""
        bus = AsyncEventBus()

        async def handler(_e, _p):
            pass

        sub_id = bus.subscribe("test.event", handler)
        assert bus.unsubscribe(sub_id) is True
        assert bus.unsubscribe(sub_id) is False

    @pytest.mark.asyncio
    async def test_unsubscribe_one_of_multiple_handlers(self):
        """Test unsubscribing one handler when multiple are registered."""
        bus = AsyncEventBus()
        results = []

        async def handler1(_e, _p):
            results.append("h1")

        async def handler2(_e, _p):
            results.append("h2")

        sub_id1 = bus.subscribe("test.event", handler1)
        bus.subscribe("test.event", handler2)

        bus.unsubscribe(sub_id1)
        await bus.publish("test.event")

        assert len(results) == 1
        assert results[0] == "h2"


class TestAsyncEventBusClear:
    """Test clearing all subscriptions."""

    def test_clear_removes_all_handlers(self):
        """Test that clear removes all subscriptions."""
        bus = AsyncEventBus()

        async def handler(_e, _p):
            pass

        bus.subscribe("event1", handler)
        bus.subscribe("event2", handler)
        bus.subscribe("event3", handler)

        assert bus.count_subscribers() == 3

        bus.clear()

        assert bus.count_subscribers() == 0

    def test_clear_on_empty_bus(self):
        """Test that clearing an empty bus doesn't cause errors."""
        bus = AsyncEventBus()
        bus.clear()
        assert bus.count_subscribers() == 0

    @pytest.mark.asyncio
    async def test_publish_after_clear(self):
        """Test that publishing after clear doesn't call any handlers."""
        bus = AsyncEventBus()
        results = []

        async def handler(_e, p):
            results.append(p)

        bus.subscribe("test.event", handler)
        bus.clear()
        await bus.publish("test.event", "data")

        assert len(results) == 0


class TestAsyncEventBusValidation:
    """Test input validation and assertions."""

    def test_subscribe_with_invalid_event_type(self):
        """Test that subscribe raises assertion for non-string event."""
        bus = AsyncEventBus()

        async def handler(_e, _p):
            pass

        with pytest.raises(AssertionError, match="Event must be a string"):
            bus.subscribe(123, handler)

    def test_subscribe_with_empty_event(self):
        """Test that subscribe raises assertion for empty event name."""
        bus = AsyncEventBus()

        async def handler(_e, _p):
            pass

        with pytest.raises(AssertionError, match="Event name cannot be empty"):
            bus.subscribe("", handler)

    def test_subscribe_with_non_callable_handler(self):
        """Test subscribe raises assertion for non-callable handler."""
        bus = AsyncEventBus()
        with pytest.raises(AssertionError, match="Handler must be callable"):
            bus.subscribe("test.event", "not a function")

    @pytest.mark.asyncio
    async def test_publish_with_invalid_event_type(self):
        """Test publish raises assertion for non-string event."""
        bus = AsyncEventBus()
        with pytest.raises(AssertionError, match="Event must be a string"):
            await bus.publish(123, "payload")

    @pytest.mark.asyncio
    async def test_publish_with_empty_event(self):
        """Test publish raises assertion for empty event name."""
        bus = AsyncEventBus()
        msg = "Event name cannot be empty"
        with pytest.raises(AssertionError, match=msg):
            await bus.publish("", "payload")

    def test_unsubscribe_with_invalid_id_type(self):
        """Test that unsubscribe raises assertion for non-string ID."""
        bus = AsyncEventBus()
        with pytest.raises(
            AssertionError, match="Subscription ID must be a string"
        ):
            bus.unsubscribe(123)

    def test_unsubscribe_with_empty_id(self):
        """Test that unsubscribe raises assertion for empty ID."""
        bus = AsyncEventBus()
        with pytest.raises(
            AssertionError, match="Subscription ID cannot be empty"
        ):
            bus.unsubscribe("")

    def test_count_subscribers_with_invalid_event_type(self):
        """Test that count_subscribers raises assertion for non-string event."""
        bus = AsyncEventBus()
        with pytest.raises(AssertionError, match="Event must be a string"):
            bus.count_subscribers(123)


class TestAsyncEventBusEdgeCases:
    """Test edge cases and unusual scenarios."""

    @pytest.mark.asyncio
    async def test_handler_receives_correct_event_name(self):
        """Test that handlers receive the correct event name."""
        bus = AsyncEventBus()
        received_events = []

        async def handler(event, _payload):
            received_events.append(event)

        bus.subscribe("my.event", handler)
        await bus.publish("my.event", {})

        assert len(received_events) == 1
        assert received_events[0] == "my.event"

    @pytest.mark.asyncio
    async def test_multiple_events_multiple_handlers(self):
        """Test complex scenario with multiple events and handlers."""
        bus = AsyncEventBus()
        calls = []

        async def handler_a(_e, p):
            calls.append(("a", _e, p))

        async def handler_b(_e, p):
            calls.append(("b", _e, p))

        bus.subscribe("event1", handler_a)
        bus.subscribe("event1", handler_b)
        bus.subscribe("event2", handler_a)

        await bus.publish("event1", "data1")
        await bus.publish("event2", "data2")

        assert len(calls) == 3
        assert ("a", "event1", "data1") in calls
        assert ("b", "event1", "data1") in calls
        assert ("a", "event2", "data2") in calls

    @pytest.mark.asyncio
    async def test_handler_can_modify_mutable_payload(self):
        """Test that handlers can modify mutable payloads."""
        bus = AsyncEventBus()

        async def handler(_event, payload):
            if isinstance(payload, dict):
                payload["modified"] = True

        payload = {"data": 123}
        bus.subscribe("test.event", handler)
        await bus.publish("test.event", payload)

        assert payload["modified"] is True

    @pytest.mark.asyncio
    async def test_exception_in_handler_propagates(self):
        """Test that exceptions in handlers propagate to the caller."""
        bus = AsyncEventBus()

        async def faulty_handler(_event, _payload):
            raise ValueError("Handler error")

        bus.subscribe("test.event", faulty_handler)

        with pytest.raises(ValueError, match="Handler error"):
            await bus.publish("test.event")

    @pytest.mark.asyncio
    async def test_async_handler_with_delay(self):
        """Test that async handlers with delays work correctly."""
        bus = AsyncEventBus()
        start_time = asyncio.get_event_loop().time()
        results = []

        async def delayed_handler(_event, payload):
            await asyncio.sleep(0.05)
            results.append(payload)

        bus.subscribe("test.event", delayed_handler)
        await bus.publish("test.event", "data")

        end_time = asyncio.get_event_loop().time()

        assert len(results) == 1
        assert results[0] == "data"
        assert (end_time - start_time) >= 0.05
