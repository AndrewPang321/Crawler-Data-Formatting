import io
import datetime
import time
import json
import csv
import http.client

conn = http.client.HTTPSConnection("api.themoviedb.org")

payload = "{}"

fo = csv.writer(open("all_movies_" + str(datetime.datetime.now()).replace(" ", "_") + ".txt", "a"))

for i in range(1000):
    ### 20 movies for each page ###
    print("Running page " + str(i+1) + " ...")
    conn.request("GET", "/3/discover/movie?page=" + str(i+1) + "&include_video=false&include_adult=false&sort_by=popularity.desc&language=en-US&api_key=a6ffbc3c2a4dd66577851418f32b6da0", payload)
    res = conn.getresponse()
    data = res.read()
    data_json = json.loads(data)

    # write to csv file
    for item in data_json["results"]:
        fo.writerow([item["id"], item["title"], item["vote_average"], "https://image.tmdb.org/t/p/w500"+item["poster_path"]])

    time.sleep(1)