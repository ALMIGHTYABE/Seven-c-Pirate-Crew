# Importing Libraries
import time

import pandas as pd  # read csv, df manipulation
import streamlit as st  # data web app development
import yaml
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

# App
st.set_page_config(
    page_title="Seven c Pirate Crew",
    # page_icon="icons/pp.png",
    layout="wide",
)

# Dashboard Title
col1, col2 = st.columns(2)
col1.title("🏴‍☠️Seven c Pirate Crew")
col2.markdown('<div style="text-align: right;">Data is updated every 30 minutes</div>', unsafe_allow_html=True)

# Params
params_path = "params.yaml"


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


config = read_params(params_path)

# # Read Data
# dataset_url = config["main"]["data-source"]
#
#
# def get_data() -> pd.DataFrame:
#     return pd.read_csv(dataset_url)
#
#
# df = get_data()
# nft_df = get_data()
#
# # Data Manipulation
# ## Sidebar Data
# batch = pd.unique(df["Batch"])
# type = pd.unique(df["Type"])
# background = pd.unique(df["Background"])
# base = pd.unique(df["Base"])
# outfit = pd.unique(df["Outfit"])
# necklace = pd.unique(df["Necklace"])
# eye = pd.unique(df["Eye"])
# beard = pd.unique(df["Beard"])
# hair = pd.unique(df["Hair"])
# hat = pd.unique(df["Hat"])
# hand = pd.unique(df["Hand_Accessories"])
# shoulder = pd.unique(df["Shoulder"])
# mouth = pd.unique(df["Mouth"])
#
# # Top-Level Filters
# address_filter = st.multiselect("Select your address", pd.unique(df["address"]))
#
# # Sidebar - title & filters
# st.sidebar.markdown('### Data Filters')
# batch_choice = st.sidebar.multiselect(
#     'Choose batch:', batch, default=batch)
# type_choice = st.sidebar.multiselect(
#     'Choose type:', type, default=type)
# background_choice = st.sidebar.multiselect(
#     'Choose background:', background, default=background)
# base_choice = st.sidebar.multiselect(
#     'Choose base:', base, default=base)
# outfit_choice = st.sidebar.multiselect(
#     'Choose outfit:', outfit, default=outfit)
# necklace_choice = st.sidebar.multiselect(
#     'Choose necklace:', necklace, default=necklace)
# eye_choice = st.sidebar.multiselect(
#     'Choose eye:', eye, default=eye)
# beard_choice = st.sidebar.multiselect(
#     'Choose beard:', beard, default=beard)
# hair_choice = st.sidebar.multiselect(
#     'Choose hair:', hair, default=hair)
# hat_choice = st.sidebar.multiselect(
#     'Choose hat:', hat, default=hat)
# hand_choice = st.sidebar.multiselect(
#     'Choose hand:', hand, default=hand)
# shoulder_choice = st.sidebar.multiselect(
#     'Choose shoulder:', shoulder, default=shoulder)
# mouth_choice = st.sidebar.multiselect(
#     'Choose mouth:', mouth, default=mouth)
#
# # creating a single-element container
# placeholder = st.empty()
#
# # dataframe filter
# df = df[df["address"].isin(address_filter)]
# df = df[df["Batch"].isin(batch_choice)]
# df = df[df["Type"].isin(type_choice)]
# df = df[df["Background"].isin(background_choice)]
# df = df[df["Base"].isin(base_choice)]
# df = df[df["Outfit"].isin(outfit_choice)]
# df = df[df["Necklace"].isin(necklace_choice)]
# df = df[df["Eye"].isin(eye_choice)]
# df = df[df["Beard"].isin(beard_choice)]
# df = df[df["Hair"].isin(hair_choice)]
# df = df[df["Hat"].isin(hat_choice)]
# df = df[df["Hand_Accessories"].isin(hand_choice)]
# df = df[df["Shoulder"].isin(shoulder_choice)]
# df = df[df["Mouth"].isin(mouth_choice)]
#
#
# # Aggrid Defined
# def aggrid_interactive_table(df: pd.DataFrame):
#     """Creates an st-aggrid interactive table based on a dataframe.
#
#     Args:
#         df (pd.DataFrame]): Source dataframe
#
#     Returns:
#         dict: The selected row
#     """
#     options = GridOptionsBuilder.from_dataframe(df, enableRowGroup=True, enableValue=True, enablePivot=True)
#     options.configure_side_bar(filters_panel=True)
#     options.configure_selection("single")
#
#     selection = AgGrid(
#         df,
#         enable_enterprise_modules=True,
#         gridOptions=options.build(),
#         theme="light",
#         update_mode=GridUpdateMode.MODEL_CHANGED,
#         allow_unsafe_jscode=True,
#     )
#
#     return selection
#
#
# # Empty Placeholder Filled
# with placeholder.container():
#     if address_filter:
#         # Number of NFTS
#         st.markdown("### Number of Pixel Pirates: {}".format(str(df.shape[0])))
#
#         # Image
#         st.image(df["image"].tolist(), caption=["# " + str(i) for i in df["number"]], width=100)  # Images
#
#         # Filtered Table
#         st.markdown("### PP Details")
#         selection = aggrid_interactive_table(
#             df[['number', 'Batch', 'Type', 'Total Score', 'Background', 'Base', 'Outfit',
#                 'Necklace', 'Eye', 'Beard', 'Hair', 'Hat', 'Hand_Accessories', 'Shoulder',
#                 'Mouth']])
#
#         # Filtered Missing Traits
#         missing_traits = st.checkbox('See Missing Traits')
#         if missing_traits:
#             st.markdown("### Missing Traits")
#             missing_type_filter = st.multiselect("PP Type", ["Common", "Specials", "Legendary"],
#                                                  default=pd.unique(df["Type"]))
#             missing_df = df[df["Type"].isin(missing_type_filter)]
#             missing_nft_df = nft_df[nft_df["Type"].isin(missing_type_filter)]
#
#             # Finding Missing Traits
#             background_missing = [i for i in pd.unique(missing_nft_df["Background"]) if
#                                   i not in pd.unique(missing_df["Background"])]
#             base_missing = [i for i in pd.unique(missing_nft_df["Base"]) if i not in pd.unique(missing_df["Base"])]
#             outfit_missing = [i for i in pd.unique(missing_nft_df["Outfit"]) if
#                               i not in pd.unique(missing_df["Outfit"])]
#             necklace_missing = [i for i in pd.unique(missing_nft_df["Necklace"]) if
#                                 i not in pd.unique(missing_df["Necklace"])]
#             eye_missing = [i for i in pd.unique(missing_nft_df["Eye"]) if i not in pd.unique(missing_df["Eye"])]
#             beard_missing = [i for i in pd.unique(missing_nft_df["Beard"]) if i not in pd.unique(missing_df["Beard"])]
#             hair_missing = [i for i in pd.unique(missing_nft_df["Hair"]) if i not in pd.unique(missing_df["Hair"])]
#             hat_missing = [i for i in pd.unique(missing_nft_df["Hat"]) if i not in pd.unique(missing_df["Hat"])]
#             hand_missing = [i for i in pd.unique(missing_nft_df["Hand_Accessories"]) if
#                             i not in pd.unique(missing_df["Hand_Accessories"])]
#             shoulder_missing = [i for i in pd.unique(missing_nft_df["Shoulder"]) if
#                                 i not in pd.unique(missing_df["Shoulder"])]
#             mouth_missing = [i for i in pd.unique(missing_nft_df["Mouth"]) if i not in pd.unique(missing_df["Mouth"])]
#
#             missing = pd.DataFrame(
#                 [background_missing, base_missing, outfit_missing, necklace_missing, eye_missing, beard_missing,
#                  hair_missing,
#                  hat_missing, hand_missing, shoulder_missing, mouth_missing])
#             missing = missing.transpose()
#             missing.columns = ['Background', 'Base', 'Outfit', 'Necklace', 'Eye', 'Beard', 'Hair', 'Hat',
#                                'Hand_Accessories',
#                                'Shoulder', 'Mouth']
#             missing.fillna('', inplace=True)
#
#             selection = aggrid_interactive_table(missing)
#         else:
#             pass
#
#     time.sleep(1)
