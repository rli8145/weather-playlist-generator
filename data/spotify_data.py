import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

features = ["danceability", "energy", "valence", "tempo", "acousticness", "loudness"]