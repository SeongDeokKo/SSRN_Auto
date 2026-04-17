from ssrn_autobot.models import Paper
from ssrn_autobot.processing.scoring import score_paper


def test_scoring_rewards_relevant_keywords() -> None:
    p = Paper(
        source="test",
        external_id="1",
        title="Hansen-Jagannathan Bounds and SDF Identification",
        abstract="Stochastic discount factor and no-arbitrage implications for factor pricing.",
    )
    assert score_paper(p) >= 20


def test_scoring_penalizes_irrelevant_keywords() -> None:
    p = Paper(
        source="test",
        external_id="2",
        title="Clinical Trial and Neuroscience Evidence",
        abstract="A placebo-controlled clinical trial in oncology and neuroscience.",
    )
    assert score_paper(p) < 0
