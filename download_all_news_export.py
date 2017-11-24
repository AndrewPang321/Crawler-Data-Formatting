import newspaper
import json

# Get all news from a website with crawler

def getPaperInfo(url):
    paper = newspaper.build(url, memoize_articles=False)

    # print the number of news extracted from the website
    print("No. of news extracted from", paper.brand, ":", paper.size())

    # get all the category urls and save it in all_sub_urls array
    all_sub_urls = []
    for category in paper.category_urls():
        all_sub_urls.append(category)

    # Originally every string in the array used single quote which is not compatible in JSON format
    # use json.dumps to convert the array into JSON compatible string format before formatting it into JSON
    all_sub_urls = json.dumps(all_sub_urls)

    # Construct JSON format string for the paper
    paper_info = '{{"brand": "{paper_brand}", "description": "{paper_description}", "size": {paper_size}, "category_urls": {paper_category_urls}, "articles": {paper_articles}}}'
    return paper, all_sub_urls, paper_info

def getAllNewsExport(paper, all_sub_urls, paper_info):
    print(paper_info)
    # paper_info_json = json.loads(paper_info)
    # print(paper_info_json['category_urls'])
    # articles_paper = {{"articles": {paper_article_array}}}
    all_articles_details = []
    print(len(paper.articles))
    index = 0
    for article in paper.articles:
        if index == 10:
            break
        try:
            index += 1
            print('Running ', index, ' out of ', len(paper.articles))
            # download the article
            article.download()
            # parse to get different type of information
            article.parse()
            # nlp to get keywords and summary   
            article.nlp()

            # create a dictionary to store the news data ('images' attribute is in wrong format in the parsing process)
            news = {}
            news['url'] = article.url
            news['title'] = article.title
            news['authors'] = article.authors
            news['text'] = article.text
            news['top_image'] = article.top_image
            # news['images'] = article.images
            news['movies'] = article.movies
            news['keywords'] = article.keywords
            news['summary'] = article.summary
            # append the dict object into the list
            all_articles_details.append(news)
            # TIPS: use json.dumps(WHOLE_LIST) to change all single quotes of dict to double quotes of JSON format
            # print(json.dumps(all_articles_details))
        except newspaper.article.ArticleException:
            print('Broken URL at index', index-1, ':', article.url)
    # articles_paper_json = articles_paper.format(paper_article_array=json.dumps(all_articles_details))
    # Add new 'articles' field in the JSON
    # paper_info_json.append(articles_paper_json)
    # paper_info_json['articles'] = all_articles_details
    # print(paper_info_json)
    # paper_info.format(paper_brand=paper.brand, paper_description=paper.description, paper_size=paper.size(), paper_category_urls=all_sub_urls, paper_articles=all_articles_details)
    # paper_info.format(paper_articles=all_articles_details)
    paper_info_formatted = paper_info.format(paper_brand=paper.brand, paper_description=paper.description, paper_size=paper.size(), paper_category_urls=all_sub_urls, paper_articles=json.dumps(all_articles_details))
    print(paper_info.format(paper_brand=paper.brand, paper_description=paper.description, paper_size=paper.size(), paper_category_urls=all_sub_urls, paper_articles=json.dumps(all_articles_details)))

    # print(articles_paper_json)
    # Export to another file with JSON format only
    # Open a file
    fo = open("single_article.json", "w")
    fo.write(paper_info_formatted)
    # Close opened file
    fo.close()

# url = "http://edition.cnn.com/"
url = "http://www.scmp.com/frontpage/hk"
paper, all_sub_urls, paper_info = getPaperInfo(url)
getAllNewsExport(paper, all_sub_urls, paper_info)

# # download the article
# single_article.download()
# # parse to get different type of information
# single_article.parse()
# # nlp to get keywords and summary   
# single_article.nlp()

# # Construct JSON format string for news
# news_in_json = {{"title": "{news_title}", "authors": {news_authors}, "text": "{news_text}", "top_image": "{news_top_image}", "images": "{news_images}", "movies": {news_movies}, "keywords": {news_keywords}, "summary": "{news_summary}"}}

# # Export to another file with text format only
# # fo_test = open("single_article_content.json", "w")
# # fo_test.write(single_article.text)
# # fo_test.close()

# # Export to another file with JSON format only
# # Open a file
# fo = open("single_article.json", "w")
# fo.write(news_in_json.format(news_title=single_article.title, news_authors=single_article.authors, news_text=single_article.text, news_top_image=single_article.top_image, news_images=single_article.images, news_movies=single_article.movies, news_keywords=single_article.keywords, news_summary=single_article.summary))
# # Close opened file
# fo.close()
