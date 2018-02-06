import argparse
import io
import os

from google.cloud import language
import google
import numpy
import six

import newspaper
import json
import datetime

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
    # print(paper_info)
    all_articles_details = []
    # print(len(paper.articles))
    index = 0
    for article in paper.articles:
        # if index == 10:
        #     break
        try:
            index += 1
            print('Running ', index, ' out of ', len(paper.articles))
            # download the article
            article.download()
            # parse to get different type of information
            article.parse()
            # nlp to get keywords and summary   
            article.nlp()

            # Ignore article which is not a news (with text < 500) crawled from the web
            if len(article.text) < 500:
                print(article.title, "is skipped as not enough content.")
                continue

            # create a dictionary to store the news data ('images' attribute may be in wrong format in the parsing process)
            news = {}
            news['url'] = article.url
            news['title'] = article.title
            news['authors'] = article.authors
            news['text'] = article.text
            news['top_image'] = article.top_image
            # The parsing result of images attribute sometimes is type set not list(array)
            # By checking the type, convert it to list using list(set) to match the JSON format
            if type(article.images) is set:
                news['images'] = list(article.images)
            else:
                news['images'] = article.images
            news['movies'] = article.movies
            news['keywords'] = article.keywords
            news['summary'] = article.summary

            # Category Classification using Google Cloud NLP API
            categories = classify(article.text, False)
            for category in categories:
                categories[category.replace("/", "_")] = categories.pop(category)

            news['all_categories'] = categories
            # print("MAIN CATEGORY: ", max(categories, key=categories.get))
            if len(categories) != 0:
                news['main_category'] = max(categories, key=categories.get)

            # append the dict object into the list
            all_articles_details.append(news)
            # TIPS: use json.dumps(WHOLE_LIST) to change all single quotes of dict to double quotes of JSON format
            # print(json.dumps(all_articles_details))
        except newspaper.article.ArticleException:
            print('Broken URL at index', index-1, ':', article.url)
        except google.api_core.exceptions.InvalidArgument:
            print('Language is not support for Google Cloud ClassifyText')

    paper_info_formatted = paper_info.format(paper_brand=paper.brand, paper_description=paper.description, paper_size=paper.size(), paper_category_urls=all_sub_urls, paper_articles=json.dumps(all_articles_details))
    # print(paper_info.format(paper_brand=paper.brand, paper_description=paper.description, paper_size=paper.size(), paper_category_urls=all_sub_urls, paper_articles=json.dumps(all_articles_details)))

    # Export to another file with JSON format only
    # Open a file
    fo = open("all_articles_" + str(datetime.datetime.now()).replace(" ", "_") + ".json", "w")
    fo.write(paper_info_formatted)
    # Close opened file
    fo.close()

def classify(text, verbose=True):
    """Classify the input text into categories. """

    language_client = language.LanguageServiceClient()

    document = language.types.Document(
        content=text,
        type=language.enums.Document.Type.PLAIN_TEXT)
    response = language_client.classify_text(document)
    categories = response.categories

    result = {}

    for category in categories:
        # Turn the categories into a dictionary of the form:
        # {category.name: category.confidence}, so that they can
        # be treated as a sparse vector.
        result[category.name] = category.confidence

    if verbose:
        print(text)
        for category in categories:
            print(u'=' * 20)
            print(u'{:<16}: {}'.format('category', category.name))
            print(u'{:<16}: {}'.format('confidence', category.confidence))

    return result

### Main Program ###
# url = "http://edition.cnn.com/"
url = "http://www.bbc.com/"
# url = "http://www.scmp.com/frontpage/hk"
paper, all_sub_urls, paper_info = getPaperInfo(url)
getAllNewsExport(paper, all_sub_urls, paper_info)
