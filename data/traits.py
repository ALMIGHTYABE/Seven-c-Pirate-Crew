# Import Packages
import pandas as pd
import requests
import yaml

params_path = "./params.yaml"


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


config = read_params(params_path)

# Scrape Data
try:
    life_df = pd.read_csv(config["traits"]["sheets_url"])
    hedgey_url = config["traits"]["hedgey_url"]
    nft_list = []

    for i in life_df['Number']:
        nft = requests.get(hedgey_url + str(i))
        # Status Code Check
        if nft.status_code == 200:
            # Name Check
            name = nft.json()['name']
            number = i
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

    nft_df = pd.DataFrame(nft_list)  # List to df
    nft_df['Batch'] = life_df['Batch']  # Appending Batch Number to DF
    nft_df['Type'] = life_df['Type']  # Appending Type to DF

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

    # nft_df['Bonus Score'] = 0  # Bonus Score based on NFT Type
    # nft_df.loc[nft_df['Type'] == "Legendary", 'Bonus Score'] = 5000
    # nft_df.loc[nft_df['Type'] == "Specials", 'Bonus Score'] = 2000

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

except Exception as e:
    error = {"error": e}

# Save to CSV
try:
    nft_df.to_csv("data/pirate life/traits.csv", index=False)
except Exception as e:
    error = {"error": e}
