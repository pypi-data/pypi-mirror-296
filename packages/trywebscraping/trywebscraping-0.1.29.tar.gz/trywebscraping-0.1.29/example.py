from trywebscraping import Fetch
google = Fetch("https://www.google.com/search?q=web+scraping")
results = google.query("div.g", key="search_result").extract({
    "title": "h3",
    "link": "a@href",
    "snippet": "div.VwiC3b"
}).limit(10)
print(results)