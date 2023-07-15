# Import Packages
import os
import datetime
from pathlib import Path

import pandas as pd
import requests
import yaml
import concurrent.futures

from application_logging import logger

today = datetime.datetime.now()

file_name = "Scraper_Log_" + str(today.strftime("%B")) + "_" + str(today.year) + ".txt"
file_path = Path("logs", file_name)
os.makedirs(os.path.dirname(file_path), exist_ok=True)
log_writer = logger.App_Logger()
file_object = open(file_path, 'a+')

params_path = "./params.yaml"


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


config = read_params(params_path)

# Pixel Pirate Traits
# Scrape Data
try:
    log_writer.log(file_object, "Pixel Pirate Traits Scrape Started")

    pp_df = pd.read_csv(config["traits"]["pixel_pirates_sheets_url"])
    hedgey_url = config["traits"]["pixel_pirates_hedgey_url"]
    nft_list = []

    nft_list.append(config["traits"]["pixel_pirate_manual_addition"])  # Manual Addition

    def ppscrape(tokenID):
        nft = requests.get(hedgey_url + str(tokenID))
        # Status Code Check
        if nft.status_code == 200:
            # Name Check
            name = nft.json()['name']
            try:
                index = name.index('#')
            except ValueError:
                index = len(name)
            if name[:index].strip() == "Pixel Pirates":
                number = int(name[index + 1:])
                image = nft.json()['image']
                date = nft.json()['date']
                Background = nft.json()['attributes'][0]['value']
                Base = nft.json()['attributes'][1]['value']
                Outfit = nft.json()['attributes'][2]['value']
                Necklace = nft.json()['attributes'][3]['value']
                Eye = nft.json()['attributes'][4]['value']
                Beard = nft.json()['attributes'][5]['value']
                Hair = nft.json()['attributes'][6]['value']
                Hat = nft.json()['attributes'][7]['value']
                Hand_Accessories = nft.json()['attributes'][8]['value']
                Shoulder = nft.json()['attributes'][9]['value']
                Mouth = nft.json()['attributes'][10]['value']
                Unlock_Date = nft.json()['attributes'][13]['value']
                nft_list.append({'name': name, 'number': number, 'image': image, 'date': date, 'Background': Background,
                                 'Base': Base, 'Outfit': Outfit, 'Necklace': Necklace, 'Eye': Eye, 'Beard': Beard,
                                 'Hair': Hair, 'Hat': Hat, 'Hand_Accessories': Hand_Accessories, 'Shoulder': Shoulder,
                                 'Mouth': Mouth, 'Unlock_Date': Unlock_Date})

    with concurrent.futures.ThreadPoolExecutor() as ex:
        ex.map(ppscrape, pp_df['Number'])

    nft_df = pd.DataFrame(nft_list)  # List to df
    nft_df.sort_values(by=['number'], ascending=True, inplace=True)
    nft_df = nft_df.merge(pp_df, left_on='number', right_on='Number', how='left')  # Appending Batch Number and Type to DF

    # Rarity Score Computation
    traits = ['Background', 'Base', 'Outfit', 'Necklace', 'Eye', 'Beard', 'Hair', 'Hat', 'Hand_Accessories', 'Shoulder',
              'Mouth']  # Trait List

    for i in traits:  # Score Computation
        trait_score = []
        for j in nft_df[i]:
            score = 1 / (sum(nft_df[i] == j) / nft_df[i].count())
            trait_score.append(score)
        name = i + " Score"
        nft_df[name] = trait_score

    nft_df['Bonus Score'] = 0  # Bonus Score based on NFT Type
    nft_df.loc[nft_df['Type'] == "Legendary", 'Bonus Score'] = 5000
    nft_df.loc[nft_df['Type'] == "Specials", 'Bonus Score'] = 2000

    score_list = ['Bonus Score', 'Background Score', 'Base Score', 'Outfit Score', 'Necklace Score', 'Eye Score',
                  'Beard Score', 'Hair Score', 'Hat Score', 'Hand_Accessories Score', 'Shoulder Score', 'Mouth Score']

    nft_df['Total Score'] = nft_df[score_list].sum(axis=1)  # Summation of Scores

    nft_df['Rank'] = nft_df['Total Score'].rank(ascending=False)

    nft_df = nft_df.reindex(
        columns=['name', 'number', 'image', 'date', 'Batch', 'Type', 'Rank', 'Total Score', 'Bonus Score', 'Background',
                 'Background Score', 'Base', 'Base Score', 'Outfit', 'Outfit Score',
                 'Necklace', 'Necklace Score', 'Eye', 'Eye Score', 'Beard', 'Beard Score', 'Hair', 'Hair Score', 'Hat',
                 'Hat Score', 'Hand_Accessories', 'Hand_Accessories Score', 'Shoulder', 'Shoulder Score', 'Mouth',
                 'Mouth Score',
                 'Unlock_Date'])  # Ordering of Columns

    log_writer.log(file_object, "Pixel Pirate Traits Scrape Successful")
except Exception as e:
    log_writer.log(file_object,
                   "Error occurred while scraping Traits for Pixel Pirates for Error: %s" % e)

# Save to CSV
try:
    log_writer.log(file_object, "Pixel Pirates Traits to CSV Started")
    nft_df.to_csv("data/pixel pirates/traits.csv", index=False)
    log_writer.log(file_object, "Pixel Pirates Traits to CSV Successful")
except Exception as e:
    log_writer.log(file_object,
                   "Error occurred while writing Pixel Pirates Traits to CSV Error: %s" % e)

# Pirate Life Traits
# Scrape Data
try:
    log_writer.log(file_object, "Pirate Life Traits Scrape Started")

    life_df = pd.read_csv(config["traits"]["pirate_life_sheets_url"])
    hedgey_url = config["traits"]["pirate_life_hedgey_url"]
    nft_list = []

    def plscrape(tokenID):
        nft = requests.get(hedgey_url + str(tokenID))
        # Status Code Check
        if nft.status_code == 200:
            # Name Check
            name = nft.json()['name']
            number = tokenID
            image = nft.json()['image']
            date = nft.json()['date']
            Background = nft.json()['attributes'][0]['value']
            Skin = nft.json()['attributes'][1]['value']
            Body = nft.json()['attributes'][2]['value']
            Eyes = nft.json()['attributes'][3]['value']
            Weapon = nft.json()['attributes'][4]['value']
            Necklace = nft.json()['attributes'][5]['value']
            Eye_Patch = nft.json()['attributes'][6]['value']
            Hair = nft.json()['attributes'][7]['value']
            Hat = nft.json()['attributes'][8]['value']
            Mouth = nft.json()['attributes'][9]['value']
            Pet = nft.json()['attributes'][10]['value']
            Unlock_Date = nft.json()['attributes'][13]['value']
            nft_list.append({'name': name, 'number': number, 'image': image, 'date': date, 'Background': Background,
                             'Skin': Skin, 'Body': Body, 'Eyes': Eyes, 'Weapon': Weapon, 'Necklace': Necklace,
                             'Eye Patch': Eye_Patch, 'Hair': Hair, 'Hat': Hat, 'Mouth': Mouth,
                             'Pet': Pet, 'Unlock_Date': Unlock_Date})

    with concurrent.futures.ThreadPoolExecutor() as ex:
        ex.map(plscrape, life_df['Number'])

    nft_df = pd.DataFrame(nft_list)  # List to df
    nft_df.sort_values(by=['number'], ascending=True, inplace=True)
    nft_df = nft_df.merge(life_df, left_on='number', right_on='Number', how='left')  # Appending Batch Number and Type to DF

    # Rarity Score Computation
    traits = ['Background', 'Skin', 'Body', 'Eyes', 'Weapon', 'Necklace', 'Eye Patch', 'Hair', 'Hat', 'Mouth',
              'Pet']  # Trait List

    for i in traits:  # Score Computation
        trait_score = []
        for j in nft_df[i]:
            score = 1 / (sum(nft_df[i] == j) / nft_df[i].count())
            trait_score.append(score)
        name = i + " Score"
        nft_df[name] = trait_score

    score_list = ['Background Score', 'Skin Score', 'Body Score', 'Eyes Score', 'Weapon Score',
                  'Necklace Score', 'Eye Patch Score', 'Hair Score', 'Hat Score', 'Mouth Score', 'Pet Score']

    nft_df['Total Score'] = nft_df[score_list].sum(axis=1)  # Summation of Scores

    nft_df['Rank'] = nft_df['Total Score'].rank(ascending=False)

    nft_df = nft_df.reindex(
        columns=['name', 'number', 'image', 'date', 'Batch', 'Type', 'Rank', 'Total Score', 'Background',
                 'Background Score', 'Skin', 'Skin Score', 'Body', 'Body Score',
                 'Eyes', 'Eyes Score', 'Weapon', 'Weapon Score', 'Necklace', 'Necklace Score',
                 'Eye Patch', 'Eye Patch Score', 'Hair', 'Hair Score', 'Hat', 'Hat Score',
                 'Mouth', 'Mouth Score', 'Pet', 'Pet Score', 'Unlock_Date'])  # Ordering of Columns

    log_writer.log(file_object, "Pirate Life Traits Scrape Successful")
except Exception as e:
    log_writer.log(file_object,
                   "Error occurred while scraping Traits for Pirate Life for Error: %s" % e)

# Save to CSV
try:
    log_writer.log(file_object, "Pirate Life Traits to CSV Started")
    nft_df.to_csv("data/pirate life/traits.csv", index=False)
    log_writer.log(file_object, "Pirate Life Traits to CSV Successful")
except Exception as e:
    log_writer.log(file_object,
                   "Error occurred while writing Pirate Life Traits to CSV Error: %s" % e)
