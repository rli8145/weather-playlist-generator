import pandas as pd

chat = pd.read_csv("data/chat.csv")
claude = pd.read_csv("data/claude.csv")
ryan = pd.read_csv("data/ryan.csv")

claude = claude[["weather"]+[c for c in claude.columns if c != "weather"]]

merged = pd.concat([chat, claude, ryan], axis=0, ignore_index=True)
merged.to_csv("data/track_data.csv", index=False)