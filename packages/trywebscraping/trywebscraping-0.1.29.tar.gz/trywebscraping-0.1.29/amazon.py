from trywebscraping import Fetch

amazon = Fetch("https://www.amazon.com/s?k=cracking+the+coding+interview")
product_listings = amazon.query("div.s-card-container").extract({
    "title": "h2 a span.a-text-normal",
    "price": "span.a-price-whole",
    "rating": "span.a-icon-alt",
    "num_reviews": "a-size-base",
    "product_link": "h2 a.a-link-normal@href",
    "product_image": "img.s-image@src"
})

# Print the results
print(product_listings)

# If you want to pretty print the results, you can use:
# import json
# print(json.dumps(top_offers, indent=2))