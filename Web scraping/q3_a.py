from bs4 import BeautifulSoup
from wordcloud import WordCloud
import pymysql
import pymysql.cursors
import requests
import matplotlib.pyplot as plt
import json

def starting_idx(name):
    length = len(name)
    for i in range(length):
        if name[i].isalpha():
            return i 

mydb = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "M@ni1234",
    database = "top_250_shows"
)

if (mydb.open):
    print("Connected")
    cur = mydb.cursor()

def barGraph():
    if (mydb.open):
        xAxis = []
        yAxis = []
        dictionary = {}

        query = 'SELECT Genre FROM Top_shows'
        cur.execute(query)
        allGenres = cur.fetchall()
        for itr in allGenres:
            splitGenres = itr[0].split()
            for genress in splitGenres:
                dictionary[genress] = 0
                
        for itr in allGenres:
            splitGenres = itr[0].split()
            for genress in splitGenres:
                dictionary[genress] =dictionary[genress] + 1 

        for keys in dictionary:
            xAxis.append(keys)
            yAxis.append(dictionary[keys])
            
        plt.bar(xAxis, yAxis)
        plt.show()

    
headers = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
html_file = requests.get('https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250', headers = headers).text
soup = BeautifulSoup(html_file, 'html5lib')
lists = soup.find_all('div', class_="sc-be6f1408-0 gVGktK cli-children")
show_names = []
durations = []
num_episodes = []
ratings = []
genres = []
types = []
for div in lists:
    intermedite1 = div.find('div', class_="ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-be6f1408-9 srahg cli-title")
    show_name = intermedite1.a.h3.text
    show_name = show_name[starting_idx(show_name):]
    show_names.append(show_name)
    intermedite2 = div.find('div', class_="sc-be6f1408-7 iUtHEN cli-title-metadata")
    ninja = intermedite2.find_all('span')
    one = ninja[1].text
    zero = ninja[0].text
    one = one.split(' ')[0]
    zero = zero.split(' ')[0]
    if len(zero) == 5:
        zero = zero + "present"
    durations.append(zero)
    num_episodes.append(one)
    intermedite3 = div.find('span', class_="sc-be6f1408-1 dbnleL")
    rating = intermedite3.div.span.text
    rating = rating.split()[0]
    ratings.append(float(rating))
    Genre = 'Crime'
    show_type = intermedite3.find('span', class_='sc-be6f1408-3 bpSATy cli-title-type-data').text
    types.append(show_type)
    # query = f'INSERT INTO Top_shows (NameOfTheShow, Timeline, NumberOfEpisodes, Rating, Genre) VALUES ("{show_name}", "{zero}", {one}, {rating}, "{Genre}")'
    # cur.execute(query)

genre_script = soup.find('script', id='__NEXT_DATA__')
genre_content = genre_script.string
json_object = json.loads(genre_content)
iterator = json_object['props']['pageProps']['pageData']['chartTitles']['edges']
index = 1
for edge in iterator:
    genre_temp = edge['node']['titleGenres']['genres']
    temp_list = []
    for items in genre_temp:
        # print(items['genre']['text'])
        temp_list.append(items['genre']['text'])
    # print(temp_list)
    upload_string = ' '.join(temp_list)
    # query = f'UPDATE Top_shows SET Genre = "{upload_string}" WHERE S_no = {index}'
    # cur.execute(query)
    # print(query)
    index = index + 1
    # print(genre_temp)
    
freq_num_ep = {}
for i in num_episodes:
    freq_num_ep[i] = 0
    
for i in num_episodes:
    freq_num_ep[i] = freq_num_ep[i] + 1
    
xAxis = []
yAxis = []
    
for keys, values in freq_num_ep.items():
    xAxis.append(keys)
    yAxis.append(values)

plt.plot(xAxis, yAxis, marker='s')
plt.show()

barGraph()

# mydb.commit()
cur.close()
mydb.close()