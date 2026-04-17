from ssrn_autobot.models import Paper
from ssrn_autobot.processing.dedup import deduplicate_papers


def test_dedup_by_external_id() -> None:
    a = Paper(source="mock", external_id="X1", title="T1")
    b = Paper(source="mock", external_id="X1", title="T1 changed")
    assert len(deduplicate_papers([a, b])) == 1


def test_dedup_by_normalized_title() -> None:
    a = Paper(source="mock", external_id=None, title="Term Structure of Equity")
    b = Paper(source="other", external_id=None, title="term  structure of equity!!")
    assert len(deduplicate_papers([a, b])) == 1
