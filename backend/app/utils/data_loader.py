import pandas as pd

def load_movie_metadata():
    #A faire
    def load_a_modifier():
    url = "https://api.themoviedb.org/3/authentication"
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlNjEzZjcwYTM5NTZlNTQ5NThiODhlNjM1MjY2NzM0MSIsIm5iZiI6MTc0Mjk4NDAyOC4wNDcwMDAyLCJzdWIiOiI2N2UzZDM1YzQ0MGYzMTFhY2U3NjI2MjAiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.1ElkJXIgfMwtTG3QrkYLGHacvInVXrXkkjuv7cJ05mY"
    }
    response = requests.get(url, headers=headers)
    print(response.text)