import http.client

conn = http.client.HTTPSConnection("api.themoviedb.org")

payload = "{}"

conn.request("GET", "/3/discover/movie?page=1&include_video=false&include_adult=false&sort_by=popularity.desc&language=en-US&api_key=a6ffbc3c2a4dd66577851418f32b6da0", payload)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
