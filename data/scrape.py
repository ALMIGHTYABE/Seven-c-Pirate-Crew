# Import Packages
import os
import time
import datetime
from pathlib import Path

import pandas as pd
import requests
import yaml
from web3 import Web3
import concurrent.futures

from application_logging import logger

today = datetime.datetime.now()

file_name = "Scraper_Log_" + str(today.strftime("%B")) + "_" + str(today.year) + ".txt"
file_path = Path("logs", file_name)
os.makedirs(os.path.dirname(file_path), exist_ok=True)
log_writer = logger.App_Logger()
file_object = open(file_path, 'a+')
log_writer = logger.App_Logger()

params_path = "./params.yaml"


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


config = read_params(params_path)

# Scrape Data and Save to CSV
# Pixel Pirates
try:
    log_writer.log(file_object, "Pixel Pirate Scrape Started")

    # NFT DATA
    ppnos = pd.read_csv(config["traits"]["pixel_pirates_sheets_url"])
    nft_df = pd.read_csv(config["scrape1"]["traits"])

    provider_url = config["scrape1"]["provider_url"]
    w3 = Web3(Web3.HTTPProvider(provider_url))

    abi = config["scrape1"]["abi"]
    contract_address = config["scrape1"]["contract_address"]

    contract_instance = w3.eth.contract(address=contract_address, abi=abi)
    wallet_address = []
    def ppaddress(tokenID):
        print(tokenID)
        wallet_address.append({'number' : tokenID, 'address' : contract_instance.functions.ownerOf(int(tokenID)).call()})

    with concurrent.futures.ThreadPoolExecutor() as ex:
        ex.map(ppaddress, nft_df["number"])

    wallet_df = pd.DataFrame(wallet_address)
    nft_df = nft_df.merge(wallet_df, on='number', how='left')  # Appending addresses to DF
    nft_df.sort_values(by=['number'], ascending=True, inplace=True)
    nft_df.to_csv("data/pixel pirates/address.csv", index=False)  # Save to CSV

    # SALES DATA
    sales_history = config["scrape1"]["sales_history"]

    r = requests.get(sales_history)
    # Status Code Check
    if r.status_code == 200:
        sale = r.json()['sales']
        sales_hist = pd.json_normalize(sale)  # JSON to DF
        sales_hist.price = sales_hist.price.apply(lambda x: int(x) / 1000000000000000000)
        sales_hist.endTime = sales_hist.endTime.apply(
            lambda x: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(x))))
        sales_hist['endTime'] = pd.to_datetime(sales_hist['endTime']).dt.date
        sales_hist['tokenId'] = sales_hist['tokenId'].apply(lambda x: int(x))
        sales_hist = sales_hist[sales_hist["tokenId"].isin(nft_df["number"])]
        sales_hist = pd.merge(sales_hist, nft_df[['number', 'image', 'Batch', 'Type', 'Rank', 'Total Score']],
                              left_on='tokenId', right_on='number', how='left')
        sales_hist['image'] = sales_hist['image'].apply(lambda x: '<img src=' + x + ' width="100">')
        sales_hist['Rarity Score / FTM'] = sales_hist['Total Score'] / sales_hist['price']
        sales_hist.to_csv("data/pixel pirates/history.csv", index=False)  # Save to CSV
        log_writer.log(file_object, "Pixel Pirate Scrape Successful")
except Exception as e:
    log_writer.log(file_object,
                   "Error occurred while scraping Pixel Pirates for Error: %s" % e)

# Pirate Life
try:
    log_writer.log(file_object, "Pirate Life Scrape Started")

    # NFT DATA
    life_df = pd.read_csv(config["traits"]["pirate_life_sheets_url"])
    nft_df = pd.read_csv(config["scrape2"]["traits"])

    provider_url = config["scrape2"]["provider_url"]
    w3 = Web3(Web3.HTTPProvider(provider_url))

    abi = config["scrape2"]["abi"]
    contract_address = config["scrape2"]["contract_address"]

    contract_instance = w3.eth.contract(address=contract_address, abi=abi)
    wallet_address = []
    def pladdress(tokenID):
        print(tokenID)
        wallet_address.append({'number' : tokenID, 'address' : contract_instance.functions.ownerOf(int(tokenID)).call()})

    with concurrent.futures.ThreadPoolExecutor() as ex:
        ex.map(pladdress, nft_df["number"])

    wallet_df = pd.DataFrame(wallet_address)
    nft_df = nft_df.merge(wallet_df, on='number', how='left')  # Appending addresses to DF
    nft_df.sort_values(by=['number'], ascending=True, inplace=True)
    nft_df.to_csv("data/pirate life/address.csv", index=False)  # Save to CSV

    # SALES DATA
    sales_history = config["scrape2"]["sales_history"]

    r = requests.get(sales_history)
    # Status Code Check
    if r.status_code == 200:
        sale = r.json()['sales']
        sales_hist = pd.json_normalize(sale)  # JSON to DF
        sales_hist.price = sales_hist.price.apply(lambda x: int(x) / 1000000000000000000)
        sales_hist.endTime = sales_hist.endTime.apply(
            lambda x: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(x))))
        sales_hist['endTime'] = pd.to_datetime(sales_hist['endTime']).dt.date
        sales_hist['tokenId'] = sales_hist['tokenId'].apply(lambda x: int(x))
        sales_hist = sales_hist[sales_hist["tokenId"].isin(nft_df["number"])]
        sales_hist = pd.merge(sales_hist, nft_df[['number', 'image', 'Batch', 'Type', 'Rank', 'Total Score']],
                              left_on='tokenId', right_on='number', how='left')
        sales_hist['image'] = sales_hist['image'].apply(lambda x: '<img src=' + x + ' width="100">')
        sales_hist['Rarity Score / FTM'] = sales_hist['Total Score'] / sales_hist['price']
        sales_hist.to_csv("data/pirate life/history.csv", index=False)  # Save to CSV
        log_writer.log(file_object, "Pirate Life Scrape Successful")
except Exception as e:
    log_writer.log(file_object,
                   "Error occurred while scraping Pirate Life for Error: %s" %e)
