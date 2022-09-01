# Importing Libraries
import streamlit as st

# App
st.set_page_config(
    page_title="About",
    page_icon="icons/piratelife.png",
    layout="wide",
)

# Title
st.title("💬 About")

# Content
st.write("""## What is Seven c Pirate Crew?
The ‘Seven c Pirate Crew’ is a collective for all things pirate…

Want to be an on chain pirate? The ‘Seven c’ collection was launched with ‘Pixel Pirates’ and now continues with ‘Pirate Life.' Both FNFTs contain $cLQDR, an auto-compounding liquid version of Liquid Driver's xLQDR.

Treasure hunts will continue and new pirate gems will be unearthed. Are you an on chain pirate? If so come and join the Pirate Crew!

## Why this Tracker?
This was created by me aka 🍓ALMIGHTY ABE🍓 to help Seven c Pirate Crew holders to view their collection, check out the various attributes they hold, follow sales on Secondary, and more.

## Important Links
My Twitter: https://twitter.com/KingAbraham69

Hoeem's Twitter: https://twitter.com/crypthoem/

LiquidDriver Discord: https://discord.gg/liquiddriver

Hedgey Finance Discord: https://discord.gg/hedgey

Twitter community:
https://twitter.com/i/communities/1529078922847068160

Pixel Pirate Secondary market:
https://paintswap.finance/marketplace/collections/0x2aa5d15eb36e5960d056e8fea6e7bb3e2a06a351

Pirate Life Secondary market:
https://paintswap.finance/marketplace/collections/0xb75b8dac018f36cdc1e16042bb598c99885ecbf9



## Note
This web app is in beta.

The scores calculated are not official, I am not responsible for any losses incurred due to the same.

The rarity scores is roughly calculated as follows:
[Rarity Score for a Trait Value] = 1 / ([Number of Items with that Trait Value] / [Total Number of Items in Collection])

Additionally a bonus score is given to PPs that were 1/1s and specials.


### If you like this project, you may buy me a cup of coffee. ☕
""")
st.code("0x5783Fb2f3d93364041d49097b66086703527AeaC")

