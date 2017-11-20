from newspaper import Article

# Get the news with crawler
# Another test link: http://www.scmp.com/news/hong-kong/health-environment/article/2119669/hong-kongs-food-safety-checks-imported-fruits-and
# url = "http://edition.cnn.com/2017/11/12/europe/poland-warsaw-nationalist-march/index.html"
url = "http://www.scmp.com/news/hong-kong/health-environment/article/2119669/hong-kongs-food-safety-checks-imported-fruits-and"
single_article = Article(url)

single_article.download()
single_article.parse()

# Construct JSON format string for news
news_in_json = '{{"title": "{news_title}", "authors": "{news_authors}", "text": "{news_text}", "images": "{news_images}", "movies": "{news_movies}"}}'

# Export to another file with text format only
fo_test = open("single_article_content.json", "w")
fo_test.write(single_article.text)
fo_test.close()

# Export to another file with JSON format only
# Open a file
fo = open("single_article.json", "w")
fo.write(news_in_json.format(news_title=single_article.title, news_authors=single_article.authors, news_text=single_article.text, news_images=single_article.images, news_movies=single_article.movies))

# Close opened file
fo.close()
