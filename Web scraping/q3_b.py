import pymysql
import pymysql.cursors

mydb = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "M@ni1234",
    database = "top_250_shows"
)

if (mydb.open):
    print("Connected")
    cur = mydb.cursor()
    
Genres = input("What genres whould you like: ")
IMDBRange = input("Enter the range of ratings: ")
Num_ep_pref = input("Enter preferred number of episodes: ")

genreList = Genres.split()
IMDBLow, IMDBhigh = IMDBRange.split()
Num_ep_prefMin, Num_ep_prefMax = Num_ep_pref.split()

IMDBLow = float(IMDBLow)
IMDBhigh = float(IMDBhigh)
Num_ep_prefMin = int(Num_ep_prefMin)
Num_ep_prefMax = int(Num_ep_prefMax)
    
query = f"SELECT S_no, Genre FROM Top_shows WHERE Rating >= {IMDBLow} AND Rating <= {IMDBhigh} AND NumberOfEpisodes < {Num_ep_prefMax} AND NumberOfEpisodes > {Num_ep_prefMin} ORDER BY Rating DESC"
cur.execute(query)
rows = cur.fetchall()
toBePrinted = []

list1 = genreList  # required
for tuples in rows:
    # print(tuples)
    list2 = tuples[1].split()   # available
    # print(list1, list2)
    if all(num in list2 for num in list1):
        toBePrinted.append(tuples[0])
# print(toBePrinted)
if __name__ == "__main__":
    print()
    if len(toBePrinted) != 0:
        print("Name of the show" + 60 * " " + "Number of episodes           Rating                     Genres")
        print("-" * 155)
        
    for i in toBePrinted:
        query = f'SELECT NameOfTheShow, NumberOfEpisodes, Rating, Genre FROM Top_shows WHERE S_no = {i}'
        cur.execute(query)
        it = cur.fetchall()
        print(it[0][0], end = ' ')
        print((82 - len(it[0][0])) * " ", it[0][1], end = ' ')
        print((20 - len(str(it[0][1]))) * " ", it[0][2], end = ' ')
        print((15 - len(str(it[0][2]))) * " ", it[0][3], end = ' ')
        print()
    
cur.close()
mydb.close()