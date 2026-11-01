
from app.agents.research_agent import research_topic


def test_research_shivaji_maharaj():

    result = research_topic("Chhatrapati Shivaji Maharaj")

    assert result["topic"] == "Chhatrapati Shivaji Maharaj"
    assert result["total_sources"] > 0
    assert len(result["research_results"]) > 0

    for source in result["research_results"]:
        assert source["title"]
        assert source["url"]
        assert source["content"]
