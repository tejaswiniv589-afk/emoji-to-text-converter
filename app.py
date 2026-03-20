import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mapping import load_combos, convert

# Load combos
combos = load_combos("combos.json")

# Page config
st.set_page_config(page_title="Emoji → Text Converter", page_icon="😃", layout="wide")

st.title("😃 Emoji → Text Converter")
st.write("Type text with emojis and see it converted into meaningful text.")

# Input box
user_input = st.text_area("Enter text with emojis:", "I love pizza 🍕❤️😂")

if st.button("Convert"):
    converted = convert(user_input, combos, friendly=True)
    st.subheader("Converted Text:")
    st.success(converted)

# ---- Dashboard Section ----
st.markdown("---")
st.header("📊 Emoji Usage Dashboard")

# Track emoji usage
import emoji
emoji_list = [c for c in user_input if c in emoji.EMOJI_DATA]
if emoji_list:
    df = pd.DataFrame({"Emoji": emoji_list})
    emoji_counts = df["Emoji"].value_counts().reset_index()
    emoji_counts.columns = ["Emoji", "Count"]

    st.dataframe(emoji_counts)

    fig, ax = plt.subplots()
    ax.bar(emoji_counts["Emoji"], emoji_counts["Count"])
    ax.set_ylabel("Count")
    ax.set_title("Emoji Frequency")
    st.pyplot(fig)
else:
    st.info("No emojis found in input yet.")


