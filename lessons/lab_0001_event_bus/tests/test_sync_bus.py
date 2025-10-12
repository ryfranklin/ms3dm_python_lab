"""
Tests for the synchronous EventBus implementation.
"""

import pytest

from lessons.lab_0001_event_bus.event_bus import EventBus


class TestEventBusBasics:
    """Test basic EventBus functionality."""

    def test_initialization(self):
        """Test that a new EventBus starts empty."""
        bus = EventBus()
        assert bus.count_subscribers() == 0

    def test_subscribe_returns_id(self):
        """Test that subscribe returns a subscription ID."""
        bus = EventBus()

        def handler(_e, _p):
            pass

        sub_id = bus.subscribe("test.event", handler)

        assert isinstance(sub_id, str)
        assert len(sub_id) > 0

    def test_subscribe_increments_count(self):
        """Test that subscribing increases the subscriber count."""
        bus = EventBus()

        def handler(_e, _p):
            pass

        assert bus.count_subscribers() == 0
        bus.subscribe("test.event", handler)
        assert bus.count_subscribers() == 1
        bus.subscribe("test.event", handler)
        assert bus.count_subscribers() == 2

    def test_count_subscribers_by_event(self):
        """Test counting subscribers for specific events."""
        bus = EventBus()

        def handler(_e, _p):
            pass

        bus.subscribe("event1", handler)
        bus.subscribe("event1", handler)
        bus.subscribe("event2", handler)

        assert bus.count_subscribers("event1") == 2
        assert bus.count_subscribers("event2") == 1
        assert bus.count_subscribers("event3") == 0
        assert bus.count_subscribers() == 3


class TestEventBusPublish:
    """Test publishing events."""

    def test_publish_to_single_handler(self):
        """Test publishing an event to a single handler."""
        bus = EventBus()
        results = []

        def handler(event, payload):
            results.append((event, payload))

        bus.subscribe("test.event", handler)
        count = bus.publish("test.event", {"data": 123})

        assert count == 1
        assert len(results) == 1
        assert results[0] == ("test.event", {"data": 123})

    def test_publish_to_multiple_handlers(self):
        """Test publishing to multiple handlers for the same event."""
        bus = EventBus()
        results = []

        def handler1(_event, payload):
            results.append(f"h1:{payload}")

        def handler2(_event, payload):
            results.append(f"h2:{payload}")

        bus.subscribe("test.event", handler1)
        bus.subscribe("test.event", handler2)
        count = bus.publish("test.event", "data")

        assert count == 2
        assert len(results) == 2
        assert "h1:data" in results
        assert "h2:data" in results

    def test_publish_with_no_subscribers(self):
        """Test publishing to an event with no subscribers."""
        bus = EventBus()
        count = bus.publish("no.subscribers")

        assert count == 0

    def test_publish_without_payload(self):
        """Test publishing without a payload."""
        bus = EventBus()
        results = []

        def handler(_event, payload):
            results.append(payload)

        bus.subscribe("test.event", handler)
        bus.publish("test.event")

        assert len(results) == 1
        assert results[0] is None

    def test_publish_only_notifies_correct_event(self):
        """Test that publishing only notifies handlers for specific event."""
        bus = EventBus()
        event1_called = []
        event2_called = []

        def handler1(_e, p):
            event1_called.append(p)

        def handler2(_e, p):
            event2_called.append(p)

        bus.subscribe("event1", handler1)
        bus.subscribe("event2", handler2)

        bus.publish("event1", "data1")

        assert len(event1_called) == 1
        assert len(event2_called) == 0

        bus.publish("event2", "data2")

        assert len(event1_called) == 1
        assert len(event2_called) == 1


class TestEventBusUnsubscribe:
    """Test unsubscribing from events."""

    def test_unsubscribe_removes_handler(self):
        """Test that unsubscribe removes a handler."""
        bus = EventBus()
        results = []

        def handler(_e, p):
            results.append(p)

        sub_id = bus.subscribe("test.event", handler)
        bus.publish("test.event", "before")

        assert bus.unsubscribe(sub_id) is True
        bus.publish("test.event", "after")

        assert len(results) == 1
        assert results[0] == "before"

    def test_unsubscribe_decrements_count(self):
        """Test that unsubscribe decreases the subscriber count."""
        bus = EventBus()

        def handler(_e, _p):
            pass

        sub_id = bus.subscribe("test.event", handler)
        assert bus.count_subscribers() == 1

        bus.unsubscribe(sub_id)
        assert bus.count_subscribers() == 0

    def test_unsubscribe_nonexistent_id(self):
        """Test unsubscribing with an invalid ID."""
        bus = EventBus()
        result = bus.unsubscribe("nonexistent-id")

        assert result is False

    def test_unsubscribe_same_id_twice(self):
        """Test unsubscribing the same ID twice."""
        bus = EventBus()

        def handler(_e, _p):
            pass

        sub_id = bus.subscribe("test.event", handler)
        assert bus.unsubscribe(sub_id) is True
        assert bus.unsubscribe(sub_id) is False

    def test_unsubscribe_one_of_multiple_handlers(self):
        """Test unsubscribing one handler when multiple are registered."""
        bus = EventBus()
        results = []

        def handler1(_e, _p):
            results.append("h1")

        def handler2(_e, _p):
            results.append("h2")

        sub_id1 = bus.subscribe("test.event", handler1)
        bus.subscribe("test.event", handler2)

        bus.unsubscribe(sub_id1)
        bus.publish("test.event")

        assert len(results) == 1
        assert results[0] == "h2"


class TestEventBusClear:
    """Test clearing all subscriptions."""

    def test_clear_removes_all_handlers(self):
        """Test that clear removes all subscriptions."""
        bus = EventBus()

        def handler(_e, _p):
            pass

        bus.subscribe("event1", handler)
        bus.subscribe("event2", handler)
        bus.subscribe("event3", handler)

        assert bus.count_subscribers() == 3

        bus.clear()

        assert bus.count_subscribers() == 0

    def test_clear_on_empty_bus(self):
        """Test that clearing an empty bus doesn't cause errors."""
        bus = EventBus()
        bus.clear()
        assert bus.count_subscribers() == 0

    def test_publish_after_clear(self):
        """Test that publishing after clear doesn't call any handlers."""
        bus = EventBus()
        results = []

        def handler(_e, p):
            results.append(p)

        bus.subscribe("test.event", handler)
        bus.clear()
        bus.publish("test.event", "data")

        assert len(results) == 0


class TestEventBusValidation:
    """Test input validation and assertions."""

    def test_subscribe_with_invalid_event_type(self):
        """Test that subscribe raises assertion for non-string event."""
        bus = EventBus()

        def handler(_e, _p):
            pass

        with pytest.raises(AssertionError, match="Event must be a string"):
            bus.subscribe(123, handler)

    def test_subscribe_with_empty_event(self):
        """Test that subscribe raises assertion for empty event name."""
        bus = EventBus()

        def handler(_e, _p):
            pass

        with pytest.raises(AssertionError, match="Event name cannot be empty"):
            bus.subscribe("", handler)

    def test_subscribe_with_non_callable_handler(self):
        """Test subscribe raises assertion for non-callable handler."""
        bus = EventBus()
        with pytest.raises(AssertionError, match="Handler must be callable"):
            bus.subscribe("test.event", "not a function")

    def test_publish_with_invalid_event_type(self):
        """Test publish raises assertion for non-string event."""
        bus = EventBus()
        with pytest.raises(AssertionError, match="Event must be a string"):
            bus.publish(123, "payload")

    def test_publish_with_empty_event(self):
        """Test publish raises assertion for empty event name."""
        bus = EventBus()
        msg = "Event name cannot be empty"
        with pytest.raises(AssertionError, match=msg):
            bus.publish("", "payload")

    def test_unsubscribe_with_invalid_id_type(self):
        """Test that unsubscribe raises assertion for non-string ID."""
        bus = EventBus()
        with pytest.raises(
            AssertionError, match="Subscription ID must be a string"
        ):
            bus.unsubscribe(123)

    def test_unsubscribe_with_empty_id(self):
        """Test that unsubscribe raises assertion for empty ID."""
        bus = EventBus()
        with pytest.raises(
            AssertionError, match="Subscription ID cannot be empty"
        ):
            bus.unsubscribe("")

    def test_count_subscribers_with_invalid_event_type(self):
        """Test that count_subscribers raises assertion for non-string event."""
        bus = EventBus()
        with pytest.raises(AssertionError, match="Event must be a string"):
            bus.count_subscribers(123)


class TestEventBusEdgeCases:
    """Test edge cases and unusual scenarios."""

    def test_handler_receives_correct_event_name(self):
        """Test that handlers receive the correct event name."""
        bus = EventBus()
        received_events = []

        def handler(event, _payload):
            received_events.append(event)

        bus.subscribe("my.event", handler)
        bus.publish("my.event", {})

        assert len(received_events) == 1
        assert received_events[0] == "my.event"

    def test_multiple_events_multiple_handlers(self):
        """Test complex scenario with multiple events and handlers."""
        bus = EventBus()
        calls = []

        def handler_a(e, p):
            calls.append(("a", e, p))

        def handler_b(e, p):
            calls.append(("b", e, p))

        bus.subscribe("event1", handler_a)
        bus.subscribe("event1", handler_b)
        bus.subscribe("event2", handler_a)

        bus.publish("event1", "data1")
        bus.publish("event2", "data2")

        assert len(calls) == 3
        assert ("a", "event1", "data1") in calls
        assert ("b", "event1", "data1") in calls
        assert ("a", "event2", "data2") in calls

    def test_handler_can_modify_mutable_payload(self):
        """Test that handlers can modify mutable payloads."""
        bus = EventBus()

        def handler(_event, payload):
            if isinstance(payload, dict):
                payload["modified"] = True

        payload = {"data": 123}
        bus.subscribe("test.event", handler)
        bus.publish("test.event", payload)

        assert payload["modified"] is True

    def test_exception_in_handler_propagates(self):
        """Test that exceptions in handlers propagate to the caller."""
        bus = EventBus()

        def faulty_handler(_event, _payload):
            raise ValueError("Handler error")

        bus.subscribe("test.event", faulty_handler)

        with pytest.raises(ValueError, match="Handler error"):
            bus.publish("test.event")
