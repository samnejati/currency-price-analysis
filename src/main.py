#imports:
from locale import currency
import pandas as pd
import plotly
import plotly.graph_objects as go
import requests
import seaborn as sns
from bs4 import BeautifulSoup

def get_table(url):
    """ Gets a url, scrapes the url, and returns the data frame """
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    
    table = soup.find('table') #finding html tags in soup which are = 'table'
    table_header = table.find_all('th') # finding table header in the table tags
    header = [th.text for th in table_header]   #list comprehention / 
    
    df = pd.DataFrame(columns=header)
    table_rows = table.find_all('tr')    
    for x in table_rows[1:]:
        data = x.find_all('td')
        my_row = [td.text for td in data]
        length = len(df)
        df.loc[length] = my_row
        
    return df
    

def create_plot(df):
    fig = go.Figure(data=[go.Candlestick(x=df['تاریخ / میلادی'],
                        open=df['بازگشایی؟'],
                        high=df['بیشترین؟'],
                        low=df['کمترین؟'],
                        close=df['پایانی؟'])])
    plotly.offline.plot(fig, filename='Candlestick.html')
    fig.write_image("Candlestick.png")


if __name__ == "__main__":
    url = 'https://www.tgju.org/profile/price_dollar_rl/history'
    currency_table = get_table(url)
    create_plot(currency_table)
