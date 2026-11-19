"""EXAMPLE ONLY: a tiny stateful stand-in for Canvas with fault injection.

Shows the idea: remember what was created, behave like Canvas when asked twice,
and fail on demand. A real fake models many more quirks.
"""
import pytest


class FakeCanvas:
    def __init__(self):
        self.courses = {}                    # sis_id -> course
        self.fail_next = None                # e.g. "server_error"
        self.calls = []

    def create_course(self, sis_id):
        self.calls.append(("create_course", sis_id))
        if self.fail_next == "server_error":
            self.fail_next = None
            raise ConnectionError("simulated 500")
        if sis_id in self.courses:           # Canvas refuses duplicate SIS ids
            raise ValueError("sis id already in use")
        self.courses[sis_id] = {"id": len(self.courses) + 1, "sis_id": sis_id}
        return self.courses[sis_id]


def apply_create(canvas, sis_id):
    """Safe to repeat: read first, write only what is missing."""
    if sis_id in canvas.courses:
        return "already done"
    canvas.create_course(sis_id)
    return "changed"


def test_applying_twice_changes_nothing_the_second_time():
    canvas = FakeCanvas()
    assert apply_create(canvas, "TERM-12345-A") == "changed"
    assert apply_create(canvas, "TERM-12345-A") == "already done"
    assert len(canvas.courses) == 1


def test_a_server_error_is_not_blindly_retried():
    canvas = FakeCanvas()
    canvas.fail_next = "server_error"
    with pytest.raises(ConnectionError):
        apply_create(canvas, "TERM-12345-A")
    assert [c for c in canvas.calls if c[0] == "create_course"] == [
        ("create_course", "TERM-12345-A")
    ]                                        # exactly one attempt; the caller reads back before deciding
