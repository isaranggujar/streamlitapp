import random
import time
import warnings
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import squarify
import streamlit as st

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 5000)

st.set_page_config(page_title='iNSIGHTS', page_icon=':bar_chart', layout='wide')
st.sidebar.header('iNSIGHTS')

indices_list = ['NIFTY', 'FINNIFTY', 'BANKNIFTY', 'MIDCPNIFTY']

warnings.filterwarnings('ignore')

pre_market_categories = ["NIFTY", "BANKNIFTY", "FO", "SME"]
equity_market_categories = ['NIFTY 50', 'NIFTY BANK', 'NIFTY AUTO', 'NIFTY ENERGY',
                            'NIFTY FINANCIAL SERVICES',
                            'NIFTY FMCG', 'NIFTY IT', 'NIFTY MEDIA', 'NIFTY METAL', 'NIFTY PHARMA',
                            'NIFTY PSU BANK', 'NIFTY REALTY', 'NIFTY PRIVATE BANK', 'NIFTY MIDCAP SELECT']


class NSE:
    def __init__(self):
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/121.0.0.0 Safari/537.36'}

        self.session = requests.Session()
        self.session.get("https://www.nseindia.com", headers=self.headers)

    def pre_market_data(self, category):

        category = category.upper()
        # Introduce random delay before displaying the chart
        delay_before_display = random.uniform(1, 6)  # Random delay between 1 and 4 seconds
        time.sleep(delay_before_display)

        data = self.session.get(f"https://www.nseindia.com/api/market-data-pre-open?key="
                                f"{category}", headers=self.headers).json()["data"]
        new_data = []
        for i in data:
            new_data.append(i["metadata"])
        pre_market_data = pd.DataFrame(new_data)
        pre_market_data = pre_market_data.drop(
            ["identifier", "purpose", "identifier", "yearHigh", "yearLow", "marketCap", "iep", "chartTodayPath"],
            axis=1)
        pre_market_data = pre_market_data.drop(0)
        pre_market_data = pre_market_data.sort_values(by="finalQuantity", ascending=False)
        pd.set_option('display.float_format', lambda x: '%.2f' % x)
        return pre_market_data

    def equity_market_data(self, category, symbol_list=False):
        category = category.upper().replace(' ', '%20').replace('&', '%26')
        # Introduce random delay before displaying the chart
        delay_before_display = random.uniform(1, 6)  # Random delay between 1 and 4 seconds
        time.sleep(delay_before_display)
        data = self.session.get(f"https://www.nseindia.com/api/equity-stockIndices?index={category}",
                                headers=self.headers).json()["data"]
        equity_market_data = pd.DataFrame(data)
        equity_market_data = equity_market_data.drop(
            ["meta", "priority", "identifier", "yearHigh", "yearLow", "ffmc", "nearWKH", "nearWKL", "perChange365d",
             "date365dAgo", "chart365dPath", "date30dAgo", "perChange30d", "chart30dPath", "series", "chartTodayPath"],
            axis=1)
        equity_market_data = equity_market_data.drop(0)
        equity_market_data = equity_market_data.sort_values(by="totalTradedVolume", ascending=False)
        pd.set_option('display.float_format', lambda x: '%.2f' % x)
        if symbol_list:
            return list(equity_market_data.index)
        else:
            return equity_market_data

    def indices_data(self):
        # Introduce random delay before displaying the chart
        delay_before_display = random.uniform(1, 6)  # Random delay between 1 and 4 seconds
        time.sleep(delay_before_display)

        data = self.session.get(f"https://www.nseindia.com/api/allIndices",
                                headers=self.headers).json()["data"]
        ndices_data = pd.DataFrame(data)
        ndices_data = ndices_data.drop(
            ["key", "index", "variation", "yearHigh", "yearLow", "pe", "pb", "dy", "perChange365d", "date365dAgo",
             "chart365dPath", "date30dAgo", "perChange30d", "chart30dPath", "oneWeekAgo", "oneMonthAgo", "oneYearAgo",
             "chartTodayPath"], axis=1)
        indicestodrop = [54, 17, 42, 6, 11, 52, 12, 21, 51, 9, 39, 40, 7, 32, 13, 14, 44, 10, 1, 66, 67, 69, 70,
                         1, 41, 68, 4, 5, 48, 3, 49, 47, 57, 50, 2, 64, 62, 43, 36, 46, 45, 33, 58, 35, 65, 38, 37, 30,
                         63, 31, 53, 34, 8, 59, 16, 56, 61, 59, 61, 16, 56]
        ndices_data = ndices_data.drop(indicestodrop)
        # df = df.set_index("indexSymbol", drop=True)
        ndices_data = ndices_data.sort_values(by="percentChange", ascending=False)
        pd.set_option('display.float_format', lambda x: '%.2f' % x)
        return ndices_data

    def about_holidays(self, category):
        # Introduce random delay before displaying the chart
        delay_before_display = random.uniform(1, 6)  # Random delay between 1 and 4 seconds
        time.sleep(delay_before_display)
        data = self.session.get(f'https://www.nseindia.com/api/holiday-master?type={category.lower()}',
                                headers=self.headers).json()
        about_holidays = pd.DataFrame(list(data.values())[0])
        return about_holidays

    def equity_info(self, symbol, trade_info=False):
        # Introduce random delay before displaying the chart
        delay_before_display = random.uniform(1, 6)  # Random delay between 1 and 4 seconds
        time.sleep(delay_before_display)
        symbol = symbol.replace(' ', '%20').replace('&', '%26')
        url = ('https://www.nseindia.com/api/quote-equity?symbol=' + symbol +
               ("&section=trade_info" if trade_info else ""))
        data = self.session.get(url, headers=self.headers).json()
        return data

    def get_nse_option_chain(self, symbol):
        if any(x in symbol for x in indices_list):
            data = self.session.get(f"https://www.nseindia.com/api/option-chain-indices?symbol="
                                    f"{symbol}", headers=self.headers)
        else:
            data = self.session.get(f"https://www.nseindia.com/api/option-chain-equities?symbol=" + f"{symbol}",
                                    headers=self.headers)
        return data

    @staticmethod
    def nse_live_option_chain(symbol: str, expiry_date: str = None, oi_mode: str = "compact"):
        """
        get live nse option chain.
        :param symbol: eg:SBIN/BANKNIFTY
        :param expiry_date: '01-06-2023'
        :param oi_mode: eg: full/compact
        :return: pands dataframe
        """
        # Introduce random delay before making the request
        delay = random.uniform(1, 6)  # Random delay between 2 tando 6 seconds
        time.sleep(delay)
        payload = nse.get_nse_option_chain(symbol).json()
        if expiry_date:
            exp_date = pd.to_datetime(expiry_date, format='%d-%m-%Y')
            expiry_date = exp_date.strftime('%d-%b-%Y')

        if oi_mode == 'compact':
            col_names = ['Fetch_Time', 'Symbol', 'Expiry_Date', 'CALLS_OI', 'CALLS_Chng_in_OI', 'CALLS_Volume',
                         'CALLS_IV',
                         'CALLS_LTP', 'CALLS_Net_Chng', 'Strike_Price', 'PUTS_OI', 'PUTS_Chng_in_OI', 'PUTS_Volume',
                         'PUTS_IV', 'PUTS_LTP', 'PUTS_Net_Chng']
        else:
            col_names = ['Fetch_Time', 'Symbol', 'Expiry_Date', 'CALLS_OI', 'CALLS_Chng_in_OI', 'CALLS_Volume',
                         'CALLS_IV',
                         'CALLS_LTP', 'CALLS_Net_Chng', 'CALLS_Bid_Qty', 'CALLS_Bid_Price', 'CALLS_Ask_Price',
                         'CALLS_Ask_Qty', 'Strike_Price', 'PUTS_Bid_Qty', 'PUTS_Bid_Price', 'PUTS_Ask_Price',
                         'PUTS_Ask_Qty',
                         'PUTS_Net_Chng', 'PUTS_LTP', 'PUTS_IV', 'PUTS_Volume', 'PUTS_Chng_in_OI', 'PUTS_OI']

        oi_data = pd.DataFrame(columns=col_names)

        oi_row = {'Fetch_Time': None, 'Symbol': None, 'Expiry_Date': None, 'CALLS_OI': 0, 'CALLS_Chng_in_OI': 0,
                  'CALLS_Volume': 0,
                  'CALLS_IV': 0, 'CALLS_LTP': 0, 'CALLS_Net_Chng': 0, 'CALLS_Bid_Qty': 0, 'CALLS_Bid_Price': 0,
                  'CALLS_Ask_Price': 0, 'CALLS_Ask_Qty': 0, 'Strike_Price': 0, 'PUTS_OI': 0, 'PUTS_Chng_in_OI': 0,
                  'PUTS_Volume': 0, 'PUTS_IV': 0, 'PUTS_LTP': 0, 'PUTS_Net_Chng': 0, 'PUTS_Bid_Qty': 0,
                  'PUTS_Bid_Price': 0, 'PUTS_Ask_Price': 0, 'PUTS_Ask_Qty': 0}

        # print(expiry_date)
        for m in range(len(payload['records']['data'])):
            if not expiry_date or (payload['records']['data'][m]['expiryDate'] == expiry_date):
                try:
                    oi_row['Expiry_Date'] = payload['records']['data'][m]['expiryDate']
                    oi_row['CALLS_OI'] = payload['records']['data'][m]['CE']['openInterest']
                    oi_row['CALLS_Chng_in_OI'] = payload['records']['data'][m]['CE']['changeinOpenInterest']
                    oi_row['CALLS_Volume'] = payload['records']['data'][m]['CE']['totalTradedVolume']
                    oi_row['CALLS_IV'] = payload['records']['data'][m]['CE']['impliedVolatility']
                    oi_row['CALLS_LTP'] = payload['records']['data'][m]['CE']['lastPrice']
                    oi_row['CALLS_Net_Chng'] = payload['records']['data'][m]['CE']['change']
                    if oi_mode == 'full':
                        oi_row['CALLS_Bid_Qty'] = payload['records']['data'][m]['CE']['bidQty']
                        oi_row['CALLS_Bid_Price'] = payload['records']['data'][m]['CE']['bidprice']
                        oi_row['CALLS_Ask_Price'] = payload['records']['data'][m]['CE']['askPrice']
                        oi_row['CALLS_Ask_Qty'] = payload['records']['data'][m]['CE']['askQty']
                except KeyError:
                    oi_row['CALLS_OI'], oi_row['CALLS_Chng_in_OI'], oi_row['CALLS_Volume'], oi_row['CALLS_IV'], \
                        oi_row[
                            'CALLS_LTP'], oi_row['CALLS_Net_Chng'] = 0, 0, 0, 0, 0, 0
                    if oi_mode == 'full':
                        oi_row['CALLS_Bid_Qty'], oi_row['CALLS_Bid_Price'], oi_row['CALLS_Ask_Price'], oi_row[
                            'CALLS_Ask_Qty'] = 0, 0, 0, 0
                    pass

                oi_row['Strike_Price'] = payload['records']['data'][m]['strikePrice']

                try:
                    oi_row['PUTS_OI'] = payload['records']['data'][m]['PE']['openInterest']
                    oi_row['PUTS_Chng_in_OI'] = payload['records']['data'][m]['PE']['changeinOpenInterest']
                    oi_row['PUTS_Volume'] = payload['records']['data'][m]['PE']['totalTradedVolume']
                    oi_row['PUTS_IV'] = payload['records']['data'][m]['PE']['impliedVolatility']
                    oi_row['PUTS_LTP'] = payload['records']['data'][m]['PE']['lastPrice']
                    oi_row['PUTS_Net_Chng'] = payload['records']['data'][m]['PE']['change']
                    if oi_mode == 'full':
                        oi_row['PUTS_Bid_Qty'] = payload['records']['data'][m]['PE']['bidQty']
                        oi_row['PUTS_Bid_Price'] = payload['records']['data'][m]['PE']['bidprice']
                        oi_row['PUTS_Ask_Price'] = payload['records']['data'][m]['PE']['askPrice']
                        oi_row['PUTS_Ask_Qty'] = payload['records']['data'][m]['PE']['askQty']
                except KeyError:
                    oi_row['PUTS_OI'], oi_row['PUTS_Chng_in_OI'], oi_row['PUTS_Volume'], oi_row['PUTS_IV'], oi_row[
                        'PUTS_LTP'], oi_row['PUTS_Net_Chng'] = 0, 0, 0, 0, 0, 0
                    if oi_mode == 'full':
                        oi_row['PUTS_Bid_Qty'], oi_row['PUTS_Bid_Price'], oi_row['PUTS_Ask_Price'], oi_row[
                            'PUTS_Ask_Qty'] = 0, 0, 0, 0

                # if oi_mode == 'full':
                #     oi_row['CALLS_Chart'], oi_row['PUTS_Chart'] = 0, 0
                oi_data = pd.concat([oi_data, pd.DataFrame([oi_row])], ignore_index=True)
                oi_data['Symbol'] = symbol
                oi_data['Fetch_Time'] = payload['records']['timestamp']
        return oi_data

    # def expiry_dates_future():
    #     """
    #     get the future and option expiry dates as per stock or index given
    #     :return: list of dates
    #     """
    #     payload = nse.get_nse_option_chain("TCS").json()
    #     return payload['records']['expiryDates']
    #
    #
    # def expiry_dates_option_index():
    #     """
    #     get the future and option expiry dates as per stock or index given
    #     :return: dictionary
    #     """
    #     # data_df = pd.DataFrame(columns=['index', 'expiry_date'])
    #     data_dict = {}
    #     for ind in indices_list:
    #         payload = nse.get_nse_option_chain(ind).json()
    #         data_dict.update({ind: payload['records']['expiryDates']})
    #     return data_dict
    #
    #
    # nse = NSE()
    # if __name__ == '__main__':
    #     df = nse.nse_live_option_chain('NIFTY', '22-02-2024')
    #     data = pd.DataFrame(df)
    #     data.to_excel('option.xlsx')


nse = NSE()
data_dict = nse.indices_data()
menu = ['Sectorial Flow', 'Pre Open Market', 'Equity Market', 'Option Chain']
value = st.sidebar.radio('Select Menu', menu)
if value == 'Sectorial Flow':
    if st.button("Refresh", key='Sectorial Flow'):
        st.rerun()


    def sentiment_chart(values):
        custom_colors = ['#08bdbd', '#d36135']
        fig = plt.figure(figsize=(4, 4))
        plt.pie(values, colors=custom_colors, autopct='%1.1f%%',
                startangle=90, wedgeprops=dict(width=0.4))
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        plt.gca().add_artist(centre_circle)
        plt.title('Sentiment Dial', y=1.1)
        plt.axis('equal')
        plt.subplots_adjust(bottom=0.4)
        return fig


    def ratio_chart(values1):
        custom_colors = ['#08bdbd', '#d36135']
        fig = plt.figure(figsize=(4, 4))
        plt.pie(values1, colors=custom_colors, autopct='%1.1f%%',
                startangle=90, wedgeprops=dict(width=0.4))
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        plt.gca().add_artist(centre_circle)
        plt.title('A/D Ratio', y=1.1)
        plt.axis('equal')
        plt.subplots_adjust(bottom=0.4)
        return fig


    def create_bar_graph(index_list, percent_change_list):
        # Precompute color list
        color_list = ['#08bdbd' if v >= 0 else '#d36135' for v in percent_change_list]

        # Create bar chart
        fig = go.Figure(go.Bar(x=index_list, y=percent_change_list, marker_color=color_list))

        # Customize hover details
        hover_text = [f"{index}: {value}%" for index, value in zip(index_list, percent_change_list)]
        fig.update_traces(hoverinfo='text', hovertext=hover_text)

        # Update layout
        fig.update_layout(
            title=dict(text='Sectorial Flow', x=0.5),  # Centered title
            margin=dict(l=40, r=40, b=40, t=60),
            xaxis=dict(title='Indices', tickmode='array', tickvals=list(range(len(index_list))),
                       ticktext=index_list, tickangle=270, tickfont=dict(size=14, family='Arial'), fixedrange=True),
            yaxis=dict(title='% Change', fixedrange=True),
            dragmode=False,
            showlegend=False,
            height=600
        )

        # Display the bar chart in Streamlit
        return fig


    def sectorial_flow():
        df = nse.indices_data()
        indices_to_drop = [0, 15]
        df = df.drop(indices_to_drop)

        # Convert relevant columns to numeric type
        df['percentChange'] = pd.to_numeric(df['percentChange'])
        df['advances'] = pd.to_numeric(df['advances'])
        df['declines'] = pd.to_numeric(df['declines'])

        # Calculate positive and negative percent changes
        positive_values = df['percentChange'][df['percentChange'] >= 0].sum()
        negative_values = abs(df['percentChange'][df['percentChange'] < 0].sum())

        # Calculate total advances and declines
        advances = df['advances'].sum()
        declines = df['declines'].sum()

        # Data to represent long and short positions
        labels = ['Bullish', 'Bearish']
        values = [positive_values, negative_values]

        # Data to represent advances and declines
        labels1 = ['Advances', 'Declines']
        values1 = [advances, declines]

        # Data to represent symbols with percentage change
        index_list = df['indexSymbol'].tolist()
        percent_change_list = df['percentChange'].tolist()

        # Create two columns
        col1, col2 = st.columns(2)

        with col1:
            data = {"Category": labels,
                    "Values": values
                    }

            fig = sentiment_chart(values)
            st.pyplot(fig, use_container_width=True)
            fig = pd.DataFrame(data)
            st.write(fig)

        with col2:
            data = {"Category": labels1,
                    "Values": values1
                    }

            fig = ratio_chart(values1)
            st.pyplot(fig, use_container_width=True)
            fig = pd.DataFrame(data)
            st.write(fig)

        fig = create_bar_graph(index_list, percent_change_list)
        st.plotly_chart(fig, use_container_width=True)


    sectorial_flow()

elif value == 'Pre Open Market':
    value = st.sidebar.selectbox('Select index here', pre_market_categories)
    if st.button("Refresh", key='Pre Open Market'):
        st.rerun()


    def percent_chart(data):
        # Sort values into positive and negative
        positive_df = data[data['pChange'] > 0].sort_values(by='pChange', ascending=False)
        negative_df = data[data['pChange'] < 0].sort_values(by='pChange', ascending=False)

        # Define colors for positive and negative values
        colors = ['green'] * len(positive_df) + ['red'] * len(negative_df)

        # Concatenate positive and negative DataFrames
        sorted_df = pd.concat([positive_df, negative_df])

        # Remove gap between boxes
        fig, ax = plt.subplots(figsize=(16, 8))
        squarify.plot(sizes=sorted_df['pChange'].abs(),
                      label=sorted_df['symbol'] + '\n' + sorted_df['pChange'].apply(lambda x: "{:.2f}".format(x)),
                      color=colors, alpha=0.7, edgecolor="white", linewidth=0.5,
                      text_kwargs={'color': 'white'})

        # Show label and value in each box
        plt.axis('off')

        plt.gca().invert_yaxis()

        # Display the chart using Streamlit
        return fig


    def pre_market_data_chart(value):
        data = nse.pre_market_data(value)
        fig = percent_chart(data)
        st.pyplot(fig, use_container_width=True)
        st.write(data)


    pre_market_data_chart(value)

elif value == 'Equity Market':
    value = st.sidebar.selectbox('Select index here', equity_market_categories)
    if st.button("Refresh", key='Equity Market'):
        st.rerun()


    def percent_chart(data):
        # Sort values into positive and negative
        positive_df = data[data['pChange'] > 0].sort_values(by='pChange', ascending=False)
        negative_df = data[data['pChange'] < 0].sort_values(by='pChange', ascending=False)

        # Define colors for positive and negative values
        colors = ['green'] * len(positive_df) + ['red'] * len(negative_df)

        # Concatenate positive and negative DataFrames
        sorted_df = pd.concat([positive_df, negative_df])

        # Remove gap between boxes
        fig, ax = plt.subplots(figsize=(16, 8))
        squarify.plot(sizes=sorted_df['pChange'].abs(),
                      label=sorted_df['symbol'] + '\n' + sorted_df['pChange'].apply(lambda x: "{:.2f}".format(x)),
                      color=colors, alpha=0.7, edgecolor="white", linewidth=0.5,
                      text_kwargs={'color': 'white'})

        # Show label and value in each box
        plt.axis('off')

        plt.gca().invert_yaxis()

        # Display the chart using Streamlit
        return fig


    def equity_data_chart(value):
        # Retrieve data
        data = nse.equity_market_data(value)
        fig = percent_chart(data)
        st.pyplot(fig, use_container_width=True)
        st.write(data)


    equity_data_chart(value)

elif value == 'Option Chain':
    indices_list = ['NIFTY', 'FINNIFTY', 'BANKNIFTY', 'MIDCPNIFTY']
    value = st.sidebar.selectbox('Select Index', indices_list)


    def nifty_expdates():
        # Get the current date
        current_date = datetime.now()

        # Calculate the difference in days between the current day and the next Thursday (weekday 3)
        days_until_next_thursday = (3 - current_date.weekday() + 7) % 7

        # Calculate the date for the next Thursday
        next_thursday = current_date + timedelta(days=days_until_next_thursday)

        # Initialize a list to store Thursday dates
        thursday_dates = []

        # Collect all Thursdays for the current week and the next five weeks
        for _ in range(4):  # Six weeks total (current week + next five weeks)
            thursday_dates.append(next_thursday.strftime("%d-%m-%Y"))
            next_thursday += timedelta(days=7)

        return thursday_dates


    def bn_expdates():
        # Get the current date
        current_date = datetime.now()

        # Calculate the difference in days between the current day and the next Wednesday (weekday 2)
        days_until_next_wednesday = (2 - current_date.weekday() + 7) % 7

        # Calculate the date for the next Wednesday
        next_wednesday = current_date + timedelta(days=days_until_next_wednesday)

        # Initialize a list to store Wednesday dates
        wednesday_dates = []

        # Collect all Wednesdays for the current week and the next five weeks
        for _ in range(4):  # Six weeks total (current week + next five weeks)
            wednesday_dates.append(next_wednesday.strftime("%d-%m-%Y"))
            next_wednesday += timedelta(days=7)

        # Drop the first Wednesday (current week's Wednesday)
        # wednesday_dates.pop(0)

        return wednesday_dates


    def fn_expdates():
        # Get the current date
        current_date = datetime.now()

        # Calculate the difference in days between the current day and the next Tuesday (weekday 1)
        days_until_next_tuesday = (1 - current_date.weekday() + 7) % 7

        # Calculate the date for the next Tuesday
        next_tuesday = current_date + timedelta(days=days_until_next_tuesday)

        # Initialize a list to store Tuesday dates
        tuesday_dates = []

        # Collect all Tuesdays for the current week and the next five weeks
        for _ in range(4):  # Six weeks total (current week + next five weeks)
            tuesday_dates.append(next_tuesday.strftime("%d-%m-%Y"))
            next_tuesday += timedelta(days=7)

        # Drop the first Tuesday (current week's Tuesday)

        return tuesday_dates


    def midn_expdates():
        # Get the current date
        current_date = datetime.now()

        # Calculate the difference in days between the current day and the next Monday (weekday 0)
        days_until_next_monday = (0 - current_date.weekday() + 7) % 7

        # Calculate the date for the next Monday
        next_monday = current_date + timedelta(days=days_until_next_monday)

        # Initialize a list to store Monday dates
        monday_dates = []

        # Collect all Mondays for the current week and the next five weeks
        for _ in range(4):  # Six weeks total (current week + next five weeks)
            monday_dates.append(next_monday.strftime("%d-%m-%Y"))
            next_monday += timedelta(days=7)

        return monday_dates


    def oc_pcr(labels1, values1):
        # Custom colors
        custom_colors = ['#d36135', '#08bdbd']  # Example custom colors
        # Create a donut chart
        fig = plt.figure(figsize=(4, 4))
        plt.pie(values1, labels=labels1, colors=custom_colors, autopct='%1.1f%%',
                startangle=90,
                wedgeprops=dict(width=0.4))
        # Draw a circle in the middle to make it a donut chart
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig.gca().add_artist(centre_circle)
        # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.axis('equal')
        # Add title in the middle
        plt.title('Net CE/PE Total OI', y=1.1)
        plt.subplots_adjust(bottom=0.2)
        return fig


    def oc_dial(labels, values):
        # Sample data
        categories = labels
        values = values
        # Default colors for bars
        default_colors = ['#08bdbd', '#d36135']
        # Determine colors based on conditions
        for i, value in enumerate(values):
            if value >= 0:
                if i == 0:
                    default_colors[i] = '#08bdbd'  # First bar color: green if value crosses above 0
                else:
                    default_colors[i] = '#d36135'  # Second bar color: red if value crosses above 0
            elif value <= 0:
                if i == 0:
                    default_colors[i] = '#d36135'  # First bar color: red if value crosses below 0
                else:
                    default_colors[i] = '#08bdbd'  # Second bar color: green if value crosses below 0

        # Create bar chart with custom colors
        fig, ax = plt.subplots(figsize=(4, 4))
        plt.subplots_adjust(bottom=0.2)
        bars = ax.bar(categories, values, color=default_colors)

        # Add labels and title
        # ax.set_xlabel('Categories')
        # ax.set_ylabel('Values')
        ax.set_title('CE/PE Change in OI', y=1.1)
        ax.tick_params(axis='x', labelsize=8)
        ax.tick_params(axis='y', labelsize=6)

        # Remove the border
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Add values on top of the bars
        for bar, value in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 1, str(value), ha='center', color='black')

        return fig


    def change_in_oi_bar_chart(calls_chng_in_oi, puts_chng_in_oi, strike_price, current_strike_price):
        # Create a dataframe from the data
        data = {
            'CALLS_Chng_in_OI': calls_chng_in_oi,
            'PUTS_Chng_in_OI': puts_chng_in_oi,
            'Strike_Price': strike_price
        }
        df = pd.DataFrame(data)

        # Define colors based on the conditions
        call_colors = ['#d36135' if val >= 0 else '#08bdbd' for val in df['CALLS_Chng_in_OI']]
        put_colors = ['#08bdbd' if val >= 0 else '#d36135' for val in df['PUTS_Chng_in_OI']]

        # Create the bar chart using Plotly Express
        fig = px.bar(df, y='Strike_Price', x=['CALLS_Chng_in_OI', 'PUTS_Chng_in_OI'],
                     labels={'value': 'Change in Open Interest', 'variable': 'Option Type'},
                     orientation='h',
                     height=2500,
                     text='value',
                     # barmode='group',
                     color_discrete_sequence=[call_colors, put_colors])

        # Customize hover details to include strike price and set font size
        fig.update_traces(hovertemplate='Strike Price: %{y}<br>' +
                                        'Change in OI: %{value}<br>' +
                                        '<extra></extra>',
                          hoverlabel=dict(font_size=14),  # Set font size for hover text
                          insidetextfont=dict(size=14, color='white')  # Set font size and color for the values
                          )

        # Add a solid white line for the current strike price
        fig.add_shape(type="line",
                      y0=current_strike_price,
                      x0=0,
                      y1=current_strike_price,
                      x1=min(max(df['CALLS_Chng_in_OI']), max(df['PUTS_Chng_in_OI'])),
                      line=dict(color="black", width=1, dash="solid")
                      )

        # Remove zoom
        fig.update_layout(
            margin=dict(l=0, r=0, b=0, t=40),
            xaxis=dict(title_text='Change in Open Interest', fixedrange=True,
                       title_font=dict(family='Arial'), tickfont=dict(size=14, family='Arial')),
            # Set x-axis title name and font size
            yaxis=dict(title_text='Strike Price', fixedrange=True,
                       title_font=dict(family='Arial'), tickfont=dict(size=14, family='Arial')),
            # Set y-axis title name and font size
            showlegend=False,
            font=dict(size=18, family='Calibri'),
            title=dict(text='CE/PE Change in OI', x=0.4, y=None)  # Centered title
        )

        return fig


    def total_oi_bar_chart(calls_oi, puts_oi, strike_price, current_strike_price):
        # Create a dataframe from the data
        data = {
            'CALLS_OI': calls_oi,
            'PUTS_OI': puts_oi,
            'Strike_Price': strike_price
        }
        df = pd.DataFrame(data)

        # Define colors based on the conditions
        call_colors = ['#d36135' if val >= 0 else '#08bdbd' for val in calls_oi]
        put_colors = ['#08bdbd' if val >= 0 else '#d36135' for val in puts_oi]

        # Create the bar chart using Plotly Express
        fig = px.bar(df, x='Strike_Price', y=['CALLS_OI', 'PUTS_OI'],
                     labels={'value': 'Total Open Interest', 'variable': 'Option Type'},
                     orientation='v',
                     height=500,
                     # text='value',
                     # barmode='group',
                     color_discrete_sequence=[call_colors, put_colors])

        # Customize hover details to include strike price and set font size
        fig.update_traces(hovertemplate='Strike Price: %{x}<br>' +
                                        'Total OI: %{value}<br>' +
                                        '<extra></extra>',
                          hoverlabel=dict(font_size=14),  # Set font size for hover text
                          insidetextfont=dict(size=14, color='white')  # Set font size and color for the values
                          )

        # Add a solid white line for the current strike price
        fig.add_shape(type="line",
                      x0=current_strike_price,
                      y0=0,
                      x1=current_strike_price,
                      y1=min(max(calls_oi), max(puts_oi)),
                      line=dict(color="black", width=1, dash="solid")
                      )

        # Remove zoom
        fig.update_layout(
            margin=dict(l=0, r=0, b=0, t=40),
            xaxis=dict(title_text='Strike Price', fixedrange=True,
                       title_font=dict(family='Arial'), tickfont=dict(size=14, family='Arial')),
            # Set x-axis title name and font size
            yaxis=dict(title_text='Total Open Interest', fixedrange=True,
                       title_font=dict(family='Arial'), tickfont=dict(size=14, family='Arial')),
            # Set y-axis title name and font size
            showlegend=False,
            font=dict(size=18, family='Calibri'),
            title=dict(text='CE/PE Total OI', x=0.4, y=None)  # Centered title
        )

        return fig


    def plot_option_chain_analysis(value, exp_dates):
        derivative_df = nse.nse_live_option_chain(value, exp_dates)

        # Convert relevant columns to integers
        int_columns = ['CALLS_Chng_in_OI', 'PUTS_Chng_in_OI', 'CALLS_OI', 'PUTS_OI']
        derivative_df[int_columns] = derivative_df[int_columns].astype(int)

        # Calculate total change in open interest for calls and puts
        call_chng_in_OI = derivative_df['CALLS_Chng_in_OI'].sum()
        puts_chng_in_OI = derivative_df['PUTS_Chng_in_OI'].sum()

        # Calculate total open interest for calls and puts
        call_OI = derivative_df['CALLS_OI'].sum()
        puts_OI = derivative_df['PUTS_OI'].sum()

        # Calculate net total open interest for calls and puts
        net_call_OI = call_OI + call_chng_in_OI
        net_put_OI = puts_OI + puts_chng_in_OI
        pcr = net_put_OI / net_call_OI
        pcr_ratio = format(pcr, ".2f")

        index_mapping = {
            "NIFTY": 0,
            "BANKNIFTY": 18,
            "FINNIFTY": 20,
            "MIDCPNIFTY": 15
        }

        index_name = index_mapping.get(value)

        price_value = data_dict.loc[index_name]['last']

        # Center-align text using HTML tags within st.write()
        st.write(
            f"<div style='text-align:center; margin-bottom: 20px; font-family: Calibri, sans-serif; font-size: 20px; "
            f"font-weight: bold;'>{value} : {price_value} &nbsp;&nbsp;&nbsp;&nbsp; P/C Ratio : {pcr_ratio}</div>",
            unsafe_allow_html=True)

        # Plot donut charts and line charts
        col1, col2 = st.columns(2)

        with col1:
            # Plot donut chart for change in open interest
            fig = oc_dial(['Put Change in OI', 'Call Change in OI'], [puts_chng_in_OI, call_chng_in_OI])
            st.pyplot(fig, use_container_width=True)

        with col2:
            # Plot donut chart for put-call ratio
            fig1 = oc_pcr(['Call OI', 'Put OI'], [net_call_OI, net_put_OI])
            st.pyplot(fig1, use_container_width=True)

            st.write(
                f"<div style='text-align:center; font-family: Calibri, sans-serif; font-size: 16px; font-weight: "
                f"bold;'>Net Call OI : {net_call_OI}&nbsp;&nbsp;&nbsp;&nbsp;Net Put OI : {net_put_OI}</div>",
                unsafe_allow_html=True)

        fig = change_in_oi_bar_chart(derivative_df['CALLS_Chng_in_OI'], derivative_df['PUTS_Chng_in_OI'],
                                     derivative_df['Strike_Price'], price_value)

        st.plotly_chart(fig, use_container_width=True)

        fig = total_oi_bar_chart(derivative_df['CALLS_OI'], derivative_df['PUTS_OI'], derivative_df['Strike_Price'],
                                 price_value)

        st.plotly_chart(fig, use_container_width=True)


    if value == 'NIFTY':
        exp_dates = st.sidebar.selectbox('Select expiry', nifty_expdates())
        if st.button("Refresh", key='NIFTY'):
            st.rerun()
        plot_option_chain_analysis(value, exp_dates)

    elif value == 'BANKNIFTY':
        exp_dates = st.sidebar.selectbox('Select expiry', bn_expdates())
        if st.button("Refresh", key='BANKNIFTY'):
            st.rerun()
        plot_option_chain_analysis(value, exp_dates)

    elif value == 'FINNIFTY':
        exp_dates = st.sidebar.selectbox('Select expiry', fn_expdates())
        if st.button("Refresh", key='FINNIFTY'):
            st.rerun()
        plot_option_chain_analysis(value, exp_dates)

    elif value == 'MIDCPNIFTY':
        exp_dates = st.sidebar.selectbox('Select expiry', midn_expdates())
        if st.button("Refresh", key='MIDCPNIFTY'):
            st.rerun()
        plot_option_chain_analysis(value, exp_dates)

    else:
        st.error('Wrong Input')
