import io
import decimal
import requests
from forex_python.bitcoin import BtcConverter
from tkinter import *
from urllib.request import Request, urlopen
from PIL import Image, ImageTk
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class WebImage:
    def __init__(self, url):
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        raw_data = urlopen(req).read()
        image = Image.open(io.BytesIO(raw_data))
        self.image = ImageTk.PhotoImage(image)
    def get(self):
        return self.image


window = Tk()
window.title("Trending Coin")
window.geometry("450x450")
window.configure(background='white')

api_test = requests.get("https://api.coingecko.com/api/v3/search/trending")

api_all_coin = requests.get("https://api.coingecko.com/api/v3/coins/list")
btcconv = BtcConverter()
#diraddress = r"E:\python project\coin_tracker\bitcoin_data.csv"
diraddress = r"C:\bitcoin_data.csv"
def coin_market_graph(coin_name, days):
    print(coin_name)
    coin_prices_url = fr"https://api.coingecko.com/api/v3/coins/{coin_name}/market_chart?vs_currency=usd&days={days}"
    coin_market_data = requests.get(coin_prices_url)
    i = 0
    

    # if os.path.exists(diraddress):
    #     os.remove(diraddress)

    while i < len(coin_market_data.json()["prices"]):
        #print(API_RESPONSE.json()["prices"][i][1])
        csv_exist = os.path.exists(diraddress) 
        print(len(coin_market_data.json()["prices"]))
        listdata = pd.DataFrame(data=[{"Prices": decimal.Decimal(coin_market_data.json()["prices"][i][1]), "Market Cap": coin_market_data.json()["market_caps"][i][1], "Total Volume": coin_market_data.json()["total_volumes"][i][1]}])
        
        if csv_exist == True:
            headers = None
        else:
            headers = True
        i += 1
        listdata.to_csv(diraddress, mode='a', index=False, sep=',', encoding='utf-8', header=headers)


def trending_coin(x, y):
    api_trending_coin = api_test.json()["coins"][y]["item"]

    img_link = api_trending_coin["small"]

    img = WebImage(img_link).get()

    coin_img = Label(window, image=img, bg="white")
    coin_img.image = img
    coin_symbol = Label(window, text=str(api_trending_coin["symbol"]).upper(), padx=30, bg="white")
    coin_name = Label(window, text=api_trending_coin["name"], padx=50, bg="white")
    coin_usd = Label(window, text="$" + str(round(btcconv.convert_btc_to_cur(decimal.Decimal(api_trending_coin["price_btc"]), 'USD'), 5)), padx=60, bg="white")
    coin_rank = Label(window, text="Rank Market : " + str(api_trending_coin["market_cap_rank"]), padx=10, bg="white")

    coin_img.grid(row=x, column=0, rowspan= 2)
    coin_symbol.grid(row=x, column=1)
    coin_name.grid(row=x+1, column=1)
    coin_usd.grid(row=x, column=2)
    coin_rank.grid(row=x+1, column=2)


def trend_coin():
    x = 0
    y = 0
    while x <= len(api_test.json()["coins"]) * 2 - 1:
        trending_coin(x, y)
        x = x + 2
        y = y + 1
        

trend_coin()
window.mainloop()