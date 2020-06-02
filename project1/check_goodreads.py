import requests

key = "m4Op1odc9VVDWVL0UOC9A"
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": "0743234413"})
print(res)
print(res.json())
print(res.json()['books'][0]['average_rating'])
print(res.json()['books'][0]['work_reviews_count'])
