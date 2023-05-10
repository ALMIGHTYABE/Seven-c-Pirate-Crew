# Importing Libraries
import time

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
import yaml
from st_btn_select import st_btn_select

# App
st.set_page_config(
    page_title="Collection Stats",
    page_icon="icons/piratelife.png",
    layout="wide",
)

# Title
st.title("📊 Collection Stats")

# Sidebar Mint Info
# st.sidebar.info("Pirate Life Batch Six: [Mint Now](https://v1.hedgey.finance/#/nfts/)")
# st.sidebar.info("Pirate Life Batch Six: Minted Out!")

# Params
params_path = "params.yaml"


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


config = read_params(params_path)

# Select Button
selection = st_btn_select(("Pixel Pirates", "Pirate Life"))

# Pixel Pirates
if selection == "Pixel Pirates":
    st.markdown("### Pixel Pirates")

    # Read Data
    pixel_pirate_data = config["home"]["pixel_pirates"]
    pixel_pirate_stats = config["stats"]["pixel_pirates"]


    def get_data(data) -> pd.DataFrame:
        return pd.read_csv(data)


    nft_df = get_data(pixel_pirate_data)

    # Scraping Data
    r = requests.get(pixel_pirate_stats)
    stats = r.json()
    stats_df = pd.json_normalize(stats)
    columns_with_nos = ['collection.stats.floor',
                        'collection.stats.lastSellPrice',
                        'collection.stats.totalVolumeTraded',
                        'collection.stats.volumeLast7Days',
                        'collection.stats.volumeLast24Hours',
                        'collection.stats.floorCap']
    for i in columns_with_nos:
        stats_df[i] = stats_df[i].apply(lambda x: int(x) / 1000000000000000000)  # Format Conversion

    # Getting data ready
    unique_holders = len(nft_df.address.unique())  # Unique PP Holders
    nft_floor = stats_df['collection.stats.floor'][0]  # PP Floor
    number_of_nft = len(nft_df)  # Number of PPs
    number_of_active_sales = stats_df['collection.stats.activeSales'][0]  # Number of Active Sales
    number_of_trades_24hr = stats_df['collection.stats.numTradesLast24Hours'][0]  # Number of Trades Last 24 Hours
    volume_24hr = stats_df['collection.stats.volumeLast24Hours'][0]  # Volume Last 24 Hours
    number_of_trades_7d = stats_df['collection.stats.numTradesLast7Days'][0]  # Number of Trades Last 7 Days
    volume_7d = stats_df['collection.stats.volumeLast7Days'][0]  # Volume Last 7 Days
    number_of_trades_alltime = stats_df['collection.stats.totalTrades'][0]  # Total Number of Sales
    volume_alltime = stats_df['collection.stats.totalVolumeTraded'][0]  # Total Volume Traded

    # creating a single-element container
    placeholder = st.empty()

    # Empty Placeholder Filled
    with placeholder.container():
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Unique NFT Holders", unique_holders)
        col2.metric("Number of NFTs", number_of_nft)
        col3.metric("Collection Floor in FTM", nft_floor)
        col4.metric("Number of Active Sales", number_of_active_sales)

        dfg = nft_df['address'].value_counts().reset_index().sort_values('address', ascending=False).head(10)
        dfg['index'] = [i[:6] for i in dfg['index']]
        fig = px.bar(dfg, x='address', y='index', labels={"address": "Number of NFTs", "index": "Holders"},
                     text='address')
        fig.update_layout(title="Top 10 NFT Whales", xaxis_title="Number of NFTs", yaxis_title="Holders",
                          yaxis={'categoryorder': 'total ascending'}, yaxis_type='category')
        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3 = st.columns(3)

        col1.markdown("#### Last 24 Hours")
        col2.markdown("#### Last 7 Days")
        col3.markdown("#### All Time")

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        col1.metric("Number of Trades", number_of_trades_24hr)
        col2.metric("Volume Traded in FTM", volume_24hr)
        col3.metric("Number of Trades", number_of_trades_7d)
        col4.metric("Volume Traded in FTM", volume_7d)
        col5.metric("Number of Trades", number_of_trades_alltime)
        col6.metric("Volume Traded in FTM", volume_alltime)

        time.sleep(1)

# Pirate Life
if selection == "Pirate Life":
    st.markdown("### Pirate Life")

    # Read Data
    pirate_life_data = config["home"]["pirate_life"]
    pirate_life_stats = config["stats"]["pirate_life"]


    def get_data(data) -> pd.DataFrame:
        return pd.read_csv(data)


    nft_df = get_data(pirate_life_data)

    # Scraping Data
    r = requests.get(pirate_life_stats)
    stats = r.json()
    stats_df = pd.json_normalize(stats)
    columns_with_nos = ['collection.stats.floor',
                        'collection.stats.lastSellPrice',
                        'collection.stats.totalVolumeTraded',
                        'collection.stats.volumeLast7Days',
                        'collection.stats.volumeLast24Hours',
                        'collection.stats.floorCap']
    for i in columns_with_nos:
        stats_df[i] = stats_df[i].apply(lambda x: int(x) / 1000000000000000000)  # Format Conversion

    # Getting data ready
    unique_holders = len(nft_df.address.unique())  # Unique PP Holders
    nft_floor = stats_df['collection.stats.floor'][0]  # PP Floor
    number_of_nft = len(nft_df)  # Number of PPs
    number_of_active_sales = stats_df['collection.stats.activeSales'][0]  # Number of Active Sales
    number_of_trades_24hr = stats_df['collection.stats.numTradesLast24Hours'][0]  # Number of Trades Last 24 Hours
    volume_24hr = stats_df['collection.stats.volumeLast24Hours'][0]  # Volume Last 24 Hours
    number_of_trades_7d = stats_df['collection.stats.numTradesLast7Days'][0]  # Number of Trades Last 7 Days
    volume_7d = stats_df['collection.stats.volumeLast7Days'][0]  # Volume Last 7 Days
    number_of_trades_alltime = stats_df['collection.stats.totalTrades'][0]  # Total Number of Sales
    volume_alltime = stats_df['collection.stats.totalVolumeTraded'][0]  # Total Volume Traded

    # creating a single-element container
    placeholder = st.empty()

    # Empty Placeholder Filled
    with placeholder.container():
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Unique NFT Holders", unique_holders)
        col2.metric("Number of NFTs", number_of_nft)
        col3.metric("Collection Floor in FTM", nft_floor)
        col4.metric("Number of Active Sales", number_of_active_sales)

        dfg = nft_df['address'].value_counts().reset_index().sort_values('address', ascending=False).head(10)
        dfg['index'] = [i[:6] for i in dfg['index']]
        fig = px.bar(dfg, x='address', y='index', labels={"address": "Number of NFTs", "index": "Holders"},
                     text='address')
        fig.update_layout(title="Top 10 NFT Whales", xaxis_title="Number of NFTs", yaxis_title="Holders",
                          yaxis={'categoryorder': 'total ascending'}, yaxis_type='category')
        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3 = st.columns(3)

        col1.markdown("#### Last 24 Hours")
        col2.markdown("#### Last 7 Days")
        col3.markdown("#### All Time")

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        col1.metric("Number of Trades", number_of_trades_24hr)
        col2.metric("Volume Traded in FTM", volume_24hr)
        col3.metric("Number of Trades", number_of_trades_7d)
        col4.metric("Volume Traded in FTM", volume_7d)
        col5.metric("Number of Trades", number_of_trades_alltime)
        col6.metric("Volume Traded in FTM", volume_alltime)

        time.sleep(1)
