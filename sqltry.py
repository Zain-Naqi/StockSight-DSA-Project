import sqlite3
import requests


# conn = sqlite3.connect('IBM_daily.db')
# try:
#       conn.execute('''CREATE TABLE data
#          (ID INT PRIMARY KEY     NOT NULL,
#          Date      CHAR(50)    NOT NULL,
#          Open            CHAR(50)     NOT NULL,
#          High        CHAR(50)  NOT NULL,
#         Low        CHAR(50)  NOT NULL,
#         Close         CHAR(50) NOT NULL,
#         Volume     CHAR(50)   NOT NULL);''')
# except:
#       pass



# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol=IBM&apikey=MXHD1U8YQ3F3Z5EK'
# r = requests.get(url)
# print("request got")
# data = r.json()["Time Series (Daily)"]
# print(len(data))
# for index,dat in enumerate(data):
#     conn.execute(f"INSERT INTO data (ID,Date,Open,High,Low,Close,Volume) \
#       VALUES ({index},'{str(dat)}', '{str(data[dat]['1. open'])}','{str(data[dat]['2. high'])}', '{str(data[dat]['3. low'])}', '{str(data[dat]['4. close'])}','{str(data[dat]['5. volume'])}' )")
# conn.execute("COMMIT;")
# conn.close()

def create_database(url, db_name):
      
      conn = sqlite3.connect(db_name)
      
      try:
            conn.execute('''CREATE TABLE data
            (ID INT PRIMARY KEY     NOT NULL,
            Date      CHAR(50)    NOT NULL,
            Open            CHAR(50)     NOT NULL,
            High        CHAR(50)  NOT NULL,
            Low        CHAR(50)  NOT NULL,
            Close         CHAR(50) NOT NULL,
            Volume     CHAR(50)   NOT NULL);''')
            
      except:
            pass

      r = requests.get(url)
      data = r.json()["Time Series (Daily)"]
      for index,dat in enumerate(data):
            conn.execute(f"INSERT INTO data (ID,Date,Open,High,Low,Close,Volume) \
                  VALUES ({index},'{str(dat)}', '{str(data[dat]['1. open'])}','{str(data[dat]['2. high'])}', '{str(data[dat]['3. low'])}', '{str(data[dat]['4. close'])}','{str(data[dat]['5. volume'])}' )")
      conn.execute("COMMIT;")
      conn.close()

ibm_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol=IBM&apikey=MXHD1U8YQ3F3Z5EK'
create_database(ibm_url, "IBM_Daily.db")


microsoft_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol=MSFT&apikey=MXHD1U8YQ3F3Z5EK'
create_database(microsoft_url, "Microsoft_Daily.db")


walmart_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol=WMT&apikey=MXHD1U8YQ3F3Z5EK'
create_database(walmart_url, "Walmart_Daily.db")


netflix_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol=NFLX&apikey=MXHD1U8YQ3F3Z5EK'
create_database(netflix_url, "Netflix_Daily.db")

nvidia_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol=NVDA&apikey=MXHD1U8YQ3F3Z5EK'
create_database(nvidia_url, "NVIDIA_Daily.db")
