<img src="https://www.trywebscraping.com/_next/image?url=%2Fassets%2Flogo.png&w=128&q=75" alt="Try Web Scraping Logo">

# Try Web Scraping

To get started, run: `pip install trywebscraping`

Here's some example code to help you begin:

```python
from trywebscraping import Fetch

hn = Fetch("https://news.ycombinator.com")
articles = hn.query("tr.athing").extract({
    "rank": "span.rank",
    "title": "td.title a",
    "link": "td.title a@href"
}).limit(10)
print(articles)
```

If you're interested in this project, please connect with me:

- Schedule a call: https://cal.com/lukelucas/30min
- Email: luke.lucas@trywebscraping.com

For issues, feedback, or general discussion about the library, you can use our GitHub repository: https://github.com/webscrape/trywebscraping-python

I appreciate any communications, regardless of how you choose to reach out!
