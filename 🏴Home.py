# Importing Libraries
import time
import requests
import pandas as pd  # read csv, df manipulation
import streamlit as st  # data web app development
import yaml
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from st_btn_select import st_btn_select

# App
st.set_page_config(
    page_title="Seven c Pirate Crew",
    page_icon="icons/piratelife.png",
    layout="wide",
)

# Params
params_path = "params.yaml"


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


config = read_params(params_path)

# Dashboard Logo & Title
st.image("icons/piratelife.png", width=100)
col1, col2 = st.columns(2)
col1.title("Seven c Pirate Crew")
col2.markdown('<div style="text-align: right;">Data is updated every hour</div>', unsafe_allow_html=True)

# Sidebar Mint Info
# st.sidebar.info("Pirate Life Batch Six: [Mint Now](https://v1.hedgey.finance/#/nfts/)")
# st.sidebar.info("Pirate Life Batch Six: Minted Out!")

# Select Button
selection = st_btn_select(("Pixel Pirates", "Pirate Life"))

# cLQDR Price
params = {
    'from': '0x814c66594a22404e101FEcfECac1012D8d75C156',
    'to': '0x10b620b2dbAC4Faa7D7FFD71Da486f5D44cd86f9',
    'amount': '1000000000000000000',
}
try:
    response = requests.get('https://router.firebird.finance/fantom/route', params=params)
    cLQDR_ratio = int(response.json()['maxReturn']['paths'][0]['amountTo']) / 1000000000000000000
    LQDR_price = response.json()['maxReturn']['tokens']['0x10b620b2dbac4faa7d7ffd71da486f5d44cd86f9']['price']
    cLQDR_price = cLQDR_ratio*LQDR_price
except Exception as e:
    print(e)

# Pixel Pirates
if selection == "Pixel Pirates":
    st.markdown("### Pixel Pirates")

    # Read Data
    pixel_pirate_data = config["home"]["pixel_pirates"]


    def get_data(data) -> pd.DataFrame:
        return pd.read_csv(data)


    df = get_data(pixel_pirate_data)
    nft_df = get_data(pixel_pirate_data)

    # Data Manipulation
    ## Sidebar Data
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

    # Top-Level Filters
    address_filter = st.multiselect("Select your address", pd.unique(df["address"]))

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

    # creating a single-element container
    placeholder = st.empty()

    # dataframe filter
    df = df[df["address"].isin(address_filter)]
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
        options.configure_selection("single")

        selection = AgGrid(
            df,
            enable_enterprise_modules=True,
            gridOptions=options.build(),
            update_mode=GridUpdateMode.MODEL_CHANGED,
            allow_unsafe_jscode=True,
        )

        return selection


    # Empty Placeholder Filled
    with placeholder.container():
        if address_filter:
            # Number of NFTs and value
            col1, col2, col3, col4, col5 = st.columns(5)

            col1.metric("Total Number of NFTs", df.shape[0])
            col2.metric("Number of Commons",df[df["Type"]=="Common"].shape[0])
            col3.metric("Number of Specials",df[df["Type"]=="Specials"].shape[0])
            col4.metric("Number of Legendaries",df[df["Type"]=="Legendary"].shape[0])
            col5.metric("Value of cLQDR Locked", "$" + str(round((df.shape[0] * cLQDR_price), 2)))


            # Image
            st.image(df["image"].tolist(), caption=["# " + str(i) for i in df["number"]], width=150)  # Images
            
            # Filtered Table
            st.markdown("### Pixel Pirate Data")
            selection = aggrid_interactive_table(
                df[['number', 'Batch', 'Type', 'Rank', 'Total Score', 'Background', 'Base', 'Outfit',
                    'Necklace', 'Eye', 'Beard', 'Hair', 'Hat', 'Hand_Accessories', 'Shoulder',
                    'Mouth']])
            
            # Batch Wise Info
            batch_count = st.checkbox('See Batchwise Count')
            if batch_count:
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                col1.metric("Batch 1", df[df["Batch"] == 1].shape[0])
                col2.metric("Batch 2", df[df["Batch"] == 2].shape[0])
                col3.metric("Batch 3", df[df["Batch"] == 3].shape[0])
                col4.metric("Batch 4", df[df["Batch"] == 4].shape[0])
                col5.metric("Batch 5", df[df["Batch"] == 5].shape[0])
                col6.metric("Batch 6", df[df["Batch"] == 6].shape[0])
            else:
                pass
            
            # Filtered Missing Traits
            missing_traits = st.checkbox('See Missing Traits')
            if missing_traits:
                st.markdown("### Missing Traits")
                missing_type_filter = st.multiselect("Pixel Pirate Type", ["Common", "Specials", "Legendary"],
                                                     default=pd.unique(df["Type"]))
                missing_df = df[df["Type"].isin(missing_type_filter)]
                missing_nft_df = nft_df[nft_df["Type"].isin(missing_type_filter)]

                # Finding Missing Traits
                background_missing = [i for i in pd.unique(missing_nft_df["Background"]) if
                                      i not in pd.unique(missing_df["Background"])]
                base_missing = [i for i in pd.unique(missing_nft_df["Base"]) if i not in pd.unique(missing_df["Base"])]
                outfit_missing = [i for i in pd.unique(missing_nft_df["Outfit"]) if
                                  i not in pd.unique(missing_df["Outfit"])]
                necklace_missing = [i for i in pd.unique(missing_nft_df["Necklace"]) if
                                    i not in pd.unique(missing_df["Necklace"])]
                eye_missing = [i for i in pd.unique(missing_nft_df["Eye"]) if i not in pd.unique(missing_df["Eye"])]
                beard_missing = [i for i in pd.unique(missing_nft_df["Beard"]) if
                                 i not in pd.unique(missing_df["Beard"])]
                hair_missing = [i for i in pd.unique(missing_nft_df["Hair"]) if i not in pd.unique(missing_df["Hair"])]
                hat_missing = [i for i in pd.unique(missing_nft_df["Hat"]) if i not in pd.unique(missing_df["Hat"])]
                hand_missing = [i for i in pd.unique(missing_nft_df["Hand_Accessories"]) if
                                i not in pd.unique(missing_df["Hand_Accessories"])]
                shoulder_missing = [i for i in pd.unique(missing_nft_df["Shoulder"]) if
                                    i not in pd.unique(missing_df["Shoulder"])]
                mouth_missing = [i for i in pd.unique(missing_nft_df["Mouth"]) if
                                 i not in pd.unique(missing_df["Mouth"])]

                missing = pd.DataFrame(
                    [background_missing, base_missing, outfit_missing, necklace_missing, eye_missing, beard_missing,
                     hair_missing,
                     hat_missing, hand_missing, shoulder_missing, mouth_missing])
                missing = missing.transpose()
                missing.columns = ['Background', 'Base', 'Outfit', 'Necklace', 'Eye', 'Beard', 'Hair', 'Hat',
                                   'Hand_Accessories',
                                   'Shoulder', 'Mouth']
                missing.fillna('', inplace=True)

                selection = aggrid_interactive_table(missing)
            else:
                pass

        time.sleep(1)

# Pirate Life
if selection == "Pirate Life":
    st.markdown("### Pirate Life")

    # Read Data
    pirate_life_data = config["home"]["pirate_life"]


    def get_data(data) -> pd.DataFrame:
        return pd.read_csv(data)


    df = get_data(pirate_life_data)
    nft_df = get_data(pirate_life_data)

    # Data Manipulation
    ## Sidebar Data
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

    # Top-Level Filters
    address_filter = st.multiselect("Select your address", pd.unique(df["address"]))

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

    # creating a single-element container
    placeholder = st.empty()

    # dataframe filter
    df = df[df["address"].isin(address_filter)]
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
        options.configure_selection("single")

        selection = AgGrid(
            df,
            enable_enterprise_modules=True,
            gridOptions=options.build(),
            update_mode=GridUpdateMode.MODEL_CHANGED,
            allow_unsafe_jscode=True,
        )

        return selection


    # Empty Placeholder Filled
    with placeholder.container():
        if address_filter:
            # Number of NFTs and value
            col1, col2, col3, col4, col5 = st.columns(5)

            col1.metric("Total Number of NFTs", df.shape[0])
            col2.metric("Number of Commons",df[df["Type"]=="Common"].shape[0])
            col3.metric("Number of Stories",df[df["Type"]=="Story"].shape[0])
            col4.metric("Number of Treasures",df[df["Type"]=="Treasure"].shape[0])
            col5.metric("Value of cLQDR Locked", "$" + str(round((df.shape[0] * 2 * cLQDR_price), 2)))


            # Image
            st.image(df["image"].tolist(), caption=["# " + str(i) for i in df["number"]], width=150)  # Images

            # Filtered Table
            st.markdown("### Pirate Life Data")
            selection = aggrid_interactive_table(
                df[['number', 'Batch', 'Type', 'Rank', 'Total Score', 'Background', 'Skin', 'Body',
                    'Eyes', 'Weapon', 'Necklace', 'Eye Patch', 'Hair', 'Hat', 'Mouth', 'Pet']])

            # Batch Wise Info
            batch_count = st.checkbox('See Batchwise Count')
            if batch_count:
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                col1.metric("Treasure", df[df["Batch"] == "Treasure"].shape[0])
                col2.metric("Batch 1", df[df["Batch"] == "1"].shape[0])
                col3.metric("Batch 2", df[df["Batch"] == "2"].shape[0])
                col4.metric("Batch 3", df[df["Batch"] == "3"].shape[0])
                col5.metric("Batch 4", df[df["Batch"] == "4"].shape[0])
                col6.metric("Batch 5", df[df["Batch"] == "5"].shape[0])
                col7.metric("Batch 6", df[df["Batch"] == "6"].shape[0])
            else:
                pass
            
            # Filtered Missing Traits
            missing_traits = st.checkbox('See Missing Traits')
            if missing_traits:
                st.markdown("### Missing Traits")
                # missing_type_filter = st.multiselect("Pirate Life Type", ["Treaure", "Common", "Specials", "Legendary"],
                # default=pd.unique(df["Type"]))
                missing_type_filter = st.multiselect("Pirate Life Type", pd.unique(df["Type"]),
                                                     default=pd.unique(df["Type"]))
                missing_df = df[df["Type"].isin(missing_type_filter)]
                missing_nft_df = nft_df[nft_df["Type"].isin(missing_type_filter)]
                
                # Finding Missing Traits
                background_missing = [i for i in pd.unique(missing_nft_df["Background"]) if
                                      i not in pd.unique(missing_df["Background"])]
                skin_missing = [i for i in pd.unique(missing_nft_df["Skin"]) if i not in pd.unique(missing_df["Skin"])]
                body_missing = [i for i in pd.unique(missing_nft_df["Body"]) if i not in pd.unique(missing_df["Body"])]
                eyes_missing = [i for i in pd.unique(missing_nft_df["Eyes"]) if i not in pd.unique(missing_df["Eyes"])]
                weapon_missing = [i for i in pd.unique(missing_nft_df["Weapon"]) if
                                  i not in pd.unique(missing_df["Weapon"])]
                necklace_missing = [i for i in pd.unique(missing_nft_df["Necklace"]) if
                                    i not in pd.unique(missing_df["Necklace"])]
                eyepatch_missing = [i for i in pd.unique(missing_nft_df["Eye Patch"]) if
                                    i not in pd.unique(missing_df["Eye Patch"])]
                hair_missing = [i for i in pd.unique(missing_nft_df["Hair"]) if i not in pd.unique(missing_df["Hair"])]
                hat_missing = [i for i in pd.unique(missing_nft_df["Hat"]) if i not in pd.unique(missing_df["Hat"])]
                mouth_missing = [i for i in pd.unique(missing_nft_df["Mouth"]) if
                                 i not in pd.unique(missing_df["Mouth"])]
                pet_missing = [i for i in pd.unique(missing_nft_df["Pet"]) if i not in pd.unique(missing_df["Pet"])]

                missing = pd.DataFrame(
                    [background_missing, skin_missing, body_missing, eyes_missing, weapon_missing, necklace_missing,
                     eyepatch_missing, hair_missing, hat_missing, mouth_missing, pet_missing])
                missing = missing.transpose()
                missing.columns = ['Background', 'Skin', 'Body', 'Eyes', 'Weapon', 'Necklace', 'Eye Patch', 'Hair',
                                   'Hat', 'Mouth', 'Pet']
                missing.fillna('', inplace=True)

                selection = aggrid_interactive_table(missing)
            else:
                pass

        time.sleep(1)
