import pandas as pd

chat = pd.read_csv("data/chat.csv")
claude = pd.read_csv("data/claude.csv")
personal = pd.read_csv("data/ryan.csv")

claude = claude[["weather"]+[c for c in claude.columns if c != "weather"]]

merged = pd.concat([chat, claude, personal], axis=0, ignore_index=True)
merged = merged.replace({"snow": "snowy"})

merged.to_csv("data/track_data.csv", index=False)