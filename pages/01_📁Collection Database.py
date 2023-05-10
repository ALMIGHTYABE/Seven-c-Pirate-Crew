# Importing Libraries
import time

import pandas as pd
import streamlit as st
import yaml
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from st_btn_select import st_btn_select

# App
st.set_page_config(
    page_title="Collection Database",
    page_icon="icons/piratelife.png",
    layout="wide",
)

# Title
st.title("📁 Collection Database")

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

    # Read Data
    pixel_pirate_data = config["home"]["pixel_pirates"]


    def get_data(data) -> pd.DataFrame:
        return pd.read_csv(data)


    df = get_data(pixel_pirate_data)

    # Sidebar Data
    batch = pd.unique(df["Batch"])
    type = pd.unique(df["Type"])
    background = pd.unique(df["Background"])
    base = pd.unique(df["Base"])
    outfit = pd.unique(df["Outfit"])
    necklace = pd.unique(df["Necklace"])
    eye = pd.unique(df["Eye"])
    beard = pd.unique(df["Beard"])
    hair = pd.unique(df["Hair"])
    hat = pd.unique(df["Hat"])
    hand = pd.unique(df["Hand_Accessories"])
    shoulder = pd.unique(df["Shoulder"])
    mouth = pd.unique(df["Mouth"])

    # Sidebar - title & filters
    st.sidebar.markdown('### Data Filters')
    batch_choice = st.sidebar.multiselect(
        'Choose Batch:', batch, default=batch)
    type_choice = st.sidebar.multiselect(
        'Choose Type:', type, default=type)
    background_choice = st.sidebar.multiselect(
        'Choose Background:', background, default=background)
    base_choice = st.sidebar.multiselect(
        'Choose Base:', base, default=base)
    outfit_choice = st.sidebar.multiselect(
        'Choose Outfit:', outfit, default=outfit)
    necklace_choice = st.sidebar.multiselect(
        'Choose Necklace:', necklace, default=necklace)
    eye_choice = st.sidebar.multiselect(
        'Choose Eye:', eye, default=eye)
    beard_choice = st.sidebar.multiselect(
        'Choose Beard:', beard, default=beard)
    hair_choice = st.sidebar.multiselect(
        'Choose Hair:', hair, default=hair)
    hat_choice = st.sidebar.multiselect(
        'Choose Hat:', hat, default=hat)
    hand_choice = st.sidebar.multiselect(
        'Choose Hand:', hand, default=hand)
    shoulder_choice = st.sidebar.multiselect(
        'Choose Shoulder:', shoulder, default=shoulder)
    mouth_choice = st.sidebar.multiselect(
        'Choose Mouth:', mouth, default=mouth)

    # dataframe filter
    df = df[df["Batch"].isin(batch_choice)]
    df = df[df["Type"].isin(type_choice)]
    df = df[df["Background"].isin(background_choice)]
    df = df[df["Base"].isin(base_choice)]
    df = df[df["Outfit"].isin(outfit_choice)]
    df = df[df["Necklace"].isin(necklace_choice)]
    df = df[df["Eye"].isin(eye_choice)]
    df = df[df["Beard"].isin(beard_choice)]
    df = df[df["Hair"].isin(hair_choice)]
    df = df[df["Hat"].isin(hat_choice)]
    df = df[df["Hand_Accessories"].isin(hand_choice)]
    df = df[df["Shoulder"].isin(shoulder_choice)]
    df = df[df["Mouth"].isin(mouth_choice)]


    # Aggrid Defined
    def aggrid_interactive_table(df: pd.DataFrame):
        """Creates an st-aggrid interactive table based on a dataframe.

        Args:
            df (pd.DataFrame]): Source dataframe

        Returns:
            dict: The selected row
        """
        options = GridOptionsBuilder.from_dataframe(df, enableRowGroup=True, enableValue=True, enablePivot=True)
        options.configure_side_bar(filters_panel=True)
        options.configure_selection(selection_mode="multiple", rowMultiSelectWithClick=True)

        selection = AgGrid(
            df,
            enable_enterprise_modules=True,
            gridOptions=options.build(),
            update_mode=GridUpdateMode.MODEL_CHANGED,
            allow_unsafe_jscode=True,
            height=400
        )

        return selection


    # creating a single-element container
    placeholder = st.empty()

    # Empty Placeholder Filled
    with placeholder.container():
        st.markdown("### Pixel Pirate Data")
        selection = aggrid_interactive_table(
            df[['number', 'Batch', 'Type', 'Rank', 'Total Score', 'Background', 'Base', 'Outfit',
                'Necklace', 'Eye', 'Beard', 'Hair', 'Hat', 'Hand_Accessories', 'Shoulder',
                'Mouth']].sort_values(by="number"))

        # Image Data
        image_number = [i['number'] for i in selection["selected_rows"]]
        image_url = (df[df['number'].isin(image_number)]['image'])

        if selection:
            st.image(image_url.tolist(), caption=["# " + str(i) for i in image_number], width=200)  # Images

        time.sleep(1)

# Pirate Life
if selection == "Pirate Life":

    # Read Data
    pirate_life_data = config["home"]["pirate_life"]


    def get_data(data) -> pd.DataFrame:
        return pd.read_csv(data)


    df = get_data(pirate_life_data)

    # Sidebar Data
    batch = pd.unique(df["Batch"])
    type = pd.unique(df["Type"])
    background = pd.unique(df["Background"])
    skin = pd.unique(df["Skin"])
    body = pd.unique(df["Body"])
    eyes = pd.unique(df["Eyes"])
    weapon = pd.unique(df["Weapon"])
    necklace = pd.unique(df["Necklace"])
    eyepatch = pd.unique(df["Eye Patch"])
    hair = pd.unique(df["Hair"])
    hat = pd.unique(df["Hat"])
    mouth = pd.unique(df["Mouth"])
    pet = pd.unique(df["Pet"])

    # Sidebar - title & filters
    st.sidebar.markdown('### Data Filters')
    batch_choice = st.sidebar.multiselect(
        'Choose Batch:', batch, default=batch)
    type_choice = st.sidebar.multiselect(
        'Choose Type:', type, default=type)
    background_choice = st.sidebar.multiselect(
        'Choose Background:', background, default=background)
    skin_choice = st.sidebar.multiselect(
        'Choose Skin:', skin, default=skin)
    body_choice = st.sidebar.multiselect(
        'Choose Body:', body, default=body)
    eyes_choice = st.sidebar.multiselect(
        'Choose Eyes:', eyes, default=eyes)
    weapon_choice = st.sidebar.multiselect(
        'Choose Weapon:', weapon, default=weapon)
    necklace_choice = st.sidebar.multiselect(
        'Choose Necklace:', necklace, default=necklace)
    eyepatch_choice = st.sidebar.multiselect(
        'Choose Eyepatch:', eyepatch, default=eyepatch)
    hair_choice = st.sidebar.multiselect(
        'Choose Hair:', hair, default=hair)
    hat_choice = st.sidebar.multiselect(
        'Choose Hat:', hat, default=hat)
    mouth_choice = st.sidebar.multiselect(
        'Choose Mouth:', mouth, default=mouth)
    pet_choice = st.sidebar.multiselect(
        'Choose Pet:', pet, default=pet)

    # dataframe filter
    df = df[df["Batch"].isin(batch_choice)]
    df = df[df["Type"].isin(type_choice)]
    df = df[df["Background"].isin(background_choice)]
    df = df[df["Skin"].isin(skin_choice)]
    df = df[df["Body"].isin(body_choice)]
    df = df[df["Eyes"].isin(eyes_choice)]
    df = df[df["Weapon"].isin(weapon_choice)]
    df = df[df["Necklace"].isin(necklace_choice)]
    df = df[df["Eye Patch"].isin(eyepatch_choice)]
    df = df[df["Hair"].isin(hair_choice)]
    df = df[df["Hat"].isin(hat_choice)]
    df = df[df["Mouth"].isin(mouth_choice)]
    df = df[df["Pet"].isin(pet_choice)]


    # Aggrid Defined
    def aggrid_interactive_table(df: pd.DataFrame):
        """Creates an st-aggrid interactive table based on a dataframe.

        Args:
            df (pd.DataFrame]): Source dataframe

        Returns:
            dict: The selected row
        """
        options = GridOptionsBuilder.from_dataframe(df, enableRowGroup=True, enableValue=True, enablePivot=True)
        options.configure_side_bar(filters_panel=True)
        options.configure_selection(selection_mode="multiple", rowMultiSelectWithClick=True)

        selection = AgGrid(
            df,
            enable_enterprise_modules=True,
            gridOptions=options.build(),
            update_mode=GridUpdateMode.MODEL_CHANGED,
            allow_unsafe_jscode=True,
            height=400
        )

        return selection


    # creating a single-element container
    placeholder = st.empty()

    # Empty Placeholder Filled
    with placeholder.container():
        st.markdown("### Pirate Life Data")
        selection = aggrid_interactive_table(
            df[['number', 'Batch', 'Type', 'Rank', 'Total Score', 'Background', 'Skin', 'Body', 'Eyes', 'Weapon',
                'Necklace', 'Eye Patch', 'Hair',
                'Hat', 'Mouth', 'Pet']].sort_values(by="number"))

        # Image Data
        image_number = [i['number'] for i in selection["selected_rows"]]
        image_url = (df[df['number'].isin(image_number)]['image'])

        if selection:
            st.image(image_url.tolist(), caption=["# " + str(i) for i in image_number], width=200)  # Images

        time.sleep(1)
