# Import Packages
import pandas as pd
import yaml
from web3 import Web3

params_path = "./params.yaml"


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


config = read_params(params_path)

# Scrape Data and Save to CSV
# Pixel Pirates
try:
    ppnos = pd.read_csv(config["scrape1"]["sheets_url"])
    nft_df = pd.read_csv(config["scrape1"]["traits"])

    provider_url = config["scrape1"]["provider_url"]
    w3 = Web3(Web3.HTTPProvider(provider_url))

    abi = config["scrape1"]["abi"]
    contract_address = config["scrape1"]["contract_address"]

    contract_instance = w3.eth.contract(address=contract_address, abi=abi)
    wallet_address = []
    for i in nft_df["number"]:
        wallet_address.append(contract_instance.functions.ownerOf(int(i)).call())

    nft_df["address"] = wallet_address  # Appending addresses to DF
    nft_df.to_csv("data/pixel pirates/address.csv", index=False)  # Save to CSV

except Exception as e:
    error = {"error": e}

# Pirate Life
try:
    life_df = pd.read_csv(config["traits"]["sheets_url"])
    nft_df = pd.read_csv(config["scrape2"]["traits"])

    provider_url = config["scrape2"]["provider_url"]
    w3 = Web3(Web3.HTTPProvider(provider_url))

    abi = config["scrape2"]["abi"]
    contract_address = config["scrape2"]["contract_address"]

    contract_instance = w3.eth.contract(address=contract_address, abi=abi)
    wallet_address = []
    for i in nft_df["number"]:
        wallet_address.append(contract_instance.functions.ownerOf(int(i)).call())

    nft_df["address"] = wallet_address  # Appending addresses to DF
    nft_df.to_csv("data/pirate life/address.csv", index=False)  # Save to CSV

except Exception as e:
    error = {"error": e}
