import datetime as dt

from backend.visitor_counter import VisitorCounter, client_ip_from_headers


def test_visitor_counter_counts_one_ip_once_per_day(tmp_path):
    counter = VisitorCounter(tmp_path / "visitor_count.json")
    day = dt.date(2026, 6, 12)

    assert counter.record("127.0.0.1", day=day) == 1
    assert counter.record("127.0.0.1", day=day) == 1
    assert counter.record("127.0.0.2", day=day) == 2
    assert counter.total() == 2


def test_visitor_counter_prunes_seen_window(tmp_path):
    counter = VisitorCounter(tmp_path / "visitor_count.json")

    counter.record("old", day=dt.date(2026, 6, 1))
    counter.record("new", day=dt.date(2026, 6, 12))

    data = counter.load()
    assert data["total"] == 2
    assert len(data["seen"]) == 1


def test_client_ip_prefers_first_forwarded_for():
    assert client_ip_from_headers({"x-forwarded-for": "1.1.1.1, 2.2.2.2"}, fallback="3.3.3.3") == "1.1.1.1"
    assert client_ip_from_headers({}, fallback="3.3.3.3") == "3.3.3.3"
