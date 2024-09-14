from trywebscraping import Fetch

# Basic usage: Single query without extraction
print("1. Basic usage: Single query without extraction")
hn = Fetch("https://news.ycombinator.com")
titles = hn.query("tr.athing td.title a")
print(titles)

# Custom Extraction: Single query with specified fields
print("\n2. Custom Extraction: Single query with specified fields")
articles = hn.query("tr.athing").extract({
    "rank": "td span.rank",
    "title": "td.title a",
    "link": "td.title a@href"
})
print(articles)

# Multiple Queries: Chained queries with separate extractions
print("\n3. Multiple Queries: Chained queries with separate extractions")
full_articles = hn.query("tr.athing").extract({
    "rank": "td span.rank",
    "title": "td.title a",
    "link": "td.title a@href"
}).query("tr.athing + tr").extract({
    "score": "span.score",
    "user": "a.hnuser",
    "comments": "a[href^='item?id=']:last-child"
})
print(full_articles)

# Limit Results: Using the limit method
print("\n4. Limit Results: Using the limit method")
limited_articles = hn.query("tr.athing").extract({
    "rank": "td span.rank",
    "title": "td.title a",
    "link": "td.title a@href"
}).limit(5)
print(limited_articles)

# Iteration: Using the Fetch object as an iterator
print("\n5. Iteration: Using the Fetch object as an iterator")
for article in hn.query("tr.athing").extract({
    "rank": "td span.rank",
    "title": "td.title a",
    "link": "td.title a@href"
}).limit(3):
    print(f"Rank: {article['rank']}")
    print(f"Title: {article['title']}")
    print(f"Link: {article['link']}")
    print()

# Indexing: Accessing specific results
print("\n6. Indexing: Accessing specific results")
indexed_articles = hn.query("tr.athing").extract({
    "rank": "td span.rank",
    "title": "td.title a",
    "link": "td.title a@href"
})
print("First article:")
print([indexed_articles[0]])
print("Last article:")
print([indexed_articles[-1]])
print("Articles 2-4:")
print(indexed_articles[1:4])