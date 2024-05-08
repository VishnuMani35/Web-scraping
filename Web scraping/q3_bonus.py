import pymysql
import pymysql.cursors
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from q3_b import toBePrinted

mydb = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "M@ni1234",
    database = "top_250_shows"
)

if (mydb.open):
    print("Connected")
    cur = mydb.cursor()
    
# query = 'SELECT Rating FROM Top_shows'
# cur.execute(query)
# ratings = cur.fetchall()
    
# query = 'SELECT NameOfTheShow FROM Top_shows'
# cur.execute(query)
# show_names = cur.fetchall()
# wc_list = []
# for i in range(250):
#     freq = ratings[i][0] * 10
#     for j in range(int(freq)):
#         wc_list.append(show_names[i][0])
wc_list = []
print(toBePrinted)
for i in toBePrinted:
    query = f'SELECT Rating, NameOfTheShow FROM Top_shows WHERE S_no = {i}'
    cur.execute(query)
    wc = cur.fetchone()
    print(wc, type(wc))
    freq = int(wc[0] * 10)
    for j in range(freq):
        temp1 = wc[1].replace(' ', '-')
        wc_list.append(temp1)
        
wc_string = " ".join(wc_list)
print(wc_string)
wc_obj = WordCloud(background_color='white', height = 600, width = 400).generate(wc_string)
plt.imshow(wc_obj, interpolation='bilinear')
plt.axis('off')
plt.show()

cur.close()
mydb.close()