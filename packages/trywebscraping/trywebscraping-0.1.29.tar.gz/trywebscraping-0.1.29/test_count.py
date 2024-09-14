import pytest
from trywebscraping import Fetch

@pytest.fixture
def hn():
    return Fetch("https://news.ycombinator.com")

def test_single_query_count(hn):
    articles = hn.query("tr.athing").extract({
        "rank": "span.rank",
        "title": "td.title a",
        "link": "td.title a@href"
    })
    assert articles.count() > 0, "Should return a positive count of articles"

def test_merged_query_count(hn):
    merged_articles = hn.query("tr.athing", key="article_info").extract({
        "rank": "span.rank",
        "title": "td.title a",
        "link": "td.title a@href"
    }).query("tr.athing + tr", key="article_info").extract({
        "score": "span.score",
        "user": "a.hnuser" 
    })
    assert merged_articles.count() > 0, "Should return a positive count of merged articles"

def test_limited_query_count(hn):
    limited_articles = hn.query("tr.athing").extract({
        "rank": "span.rank",
        "title": "td.title a",
        "link": "td.title a@href"
    }).limit(5)
    assert limited_articles.count() == 5, "Should return exactly 5 articles"

def test_multiple_queries_different_keys_count(hn):
    multiple_queries = hn.query("tr.athing", key="article_info").extract({
        "rank": "span.rank",
        "title": "td.title a",
        "link": "td.title a@href"
    }).query("tr.athing + tr", key="article_info").extract({
        "score": "span.score",
        "user": "a.hnuser" 
    }).limit(10).query("tr.athing + tr", key="metadata").extract({
        "score": "span.score",
        "user": "a.hnuser"
    }).limit(10)
    assert multiple_queries.count() == 20, "Should return 20 items (10 articles + 10 metadata)"

def test_empty_result_count(hn):
    empty_result = hn.query("non_existent_element").extract({
        "data": "some_selector"
    })
    assert empty_result.count() == 0, "Should return 0 for queries with no results"

def test_count_consistency(hn):
    articles = hn.query("tr.athing").extract({
        "rank": "span.rank",
        "title": "td.title a",
        "link": "td.title a@href"
    })
    count = articles.count()
    data = articles.get_data()
    assert count == len(data), "Count should match the length of get_data() result"