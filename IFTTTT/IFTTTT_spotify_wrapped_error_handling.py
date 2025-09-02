import pandas as pd
import re
from datetime import datetime
from collections import Counter

CONFIG = {
    'columnA-name': 'date', # date
    'columnB-name' :'song', # song
    'columnC-name': 'artist' # artist
} # Title this to match your header. Case sensitive.

WRAP_LINKS = [
    "https://docs.google.com/spreadsheets/d/1oJX1-uI1qv2qyhgIUWnbemtJK3HUDMWPjvxxO5-gQaE/edit?gid=0#gid=0",
    "https://docs.google.com/spreadsheets/d/1_AZFcjQU9PBlvh6CAuMMhULD8q_mGZ68xAF9OwHSfVU/edit?gid=0#gid=0",
    "https://docs.google.com/spreadsheets/d/1Gl4VepIvtB8s8zvP3Q29_8kX4JIbLoHqWaEJGO9AaDs/edit?gid=0#gid=0",
    "https://docs.google.com/spreadsheets/d/1O5BrMizv1lZvjD7h6tobX5FlnlcLImifxyaLnGkGjn4/edit?gid=0#gid=0"
    
] # Insert Google Sheet links inside the list

if not WRAP_LINKS:
    print("WRAP value not defined. Please configure the value to continue.")
    exit()

if not CONFIG or CONFIG is None:
    print("CONFIG is missing.\nEither remove this fail safe, or ensure that config is set up correctly.")
    exit()

current_datetime = datetime.now()
current_month = current_datetime.strftime("%B") # Automatically computes current month if you want to do it monthly
current_month = "2025"

def convert_google_sheet_url(url):
    # Regular expression to match and capture the necessary part of the URL
    pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?'

    # Replace function to construct the new URL for CSV export
    replacement = lambda m: f'https://docs.google.com/spreadsheets/d/{m.group(1)}/export?' + (f'gid={m.group(3)}&' if m.group(3) else '') + 'format=csv'

    # Replace using regex
    new_url = re.sub(pattern, replacement, url)

    return new_url

# Cargar datos desde los dos Google Sheets
dataframes = []
for link in WRAP_LINKS:
    try:
        pandas_url = convert_google_sheet_url(link)
        df = pd.read_csv(pandas_url)
        dataframes.append(df)
    except Exception as e:
        print(f"Error cargando {link}: {e}")

# Si no se pudieron cargar datos, salir
if not dataframes:
    print("Error: No se pudo cargar ninguna hoja de cálculo.")
    exit()

# Unir los DataFrames en uno solo
df = pd.concat(dataframes, ignore_index=True)

artist = CONFIG['columnC-name']
try:
    counts = Counter(df[artist])
    wrapped_artist = CONFIG['columnC-name']
    wrapped_song = CONFIG['columnB-name']
except (KeyError, AttributeError): # Two common errors raised when a problem occurs.
    print("Please check your google spreadsheet and ensure the headers both exist and match the config.")
    quit()

df_date = df[CONFIG['columnA-name']]

# Inicializar wrapped como un DataFrame vacío
wrapped = pd.DataFrame()

print("\n")
if df_date.str.contains(f'{current_month}').any():
    wrapped = df[df_date.str.contains(f'{current_month}')]

    print(f"JANUARY SONG NUMBER: {len(df[df_date.str.contains('January')])} (ROUGHLY {3*len(df[df_date.str.contains('January')]) / 60} HOURS)")
    print(f"FEBRUARY SONG NUMBER: {len(df[df_date.str.contains('February')])} (ROUGHLY {3*len(df[df_date.str.contains('February')]) / 60} HOURS)")
    print(f"MARCH SONG NUMBER: {len(df[df_date.str.contains('March')])} (ROUGHLY {3*len(df[df_date.str.contains('March')]) / 60} HOURS)")
    print(f"APRIL SONG NUMBER: {len(df[df_date.str.contains('April')])} (ROUGHLY {3*len(df[df_date.str.contains('April')]) / 60} HOURS)")
    print(f"MAY SONG NUMBER: {len(df[df_date.str.contains('May')])} (ROUGHLY {3*len(df[df_date.str.contains('May')]) / 60} HOURS)")
    print(f"JUNE SONG NUMBER: {len(df[df_date.str.contains('June')])} (ROUGHLY {3*len(df[df_date.str.contains('June')]) / 60} HOURS)")
    print(f"JULY SONG NUMBER: {len(df[df_date.str.contains('July')])} (ROUGHLY {3*len(df[df_date.str.contains('July')]) / 60} HOURS)")
    print(f"AUGUST SONG NUMBER: {len(df[df_date.str.contains('August')])} (ROUGHLY {3*len(df[df_date.str.contains('August')]) / 60} HOURS)")
    print(f"SEPTEMBER SONG NUMBER: {len(df[df_date.str.contains('September')])} (ROUGHLY {3*len(df[df_date.str.contains('September')]) / 60} HOURS)")
    print(f"OCTOBER SONG NUMBER: {len(df[df_date.str.contains('October')])} (ROUGHLY {3*len(df[df_date.str.contains('October')]) / 60} HOURS)")
    print(f"NOVEMBER SONG NUMBER: {len(df[df_date.str.contains('November')])} (ROUGHLY {3*len(df[df_date.str.contains('November')]) / 60} HOURS)")
    print(f"DECEMBER SONG NUMBER: {len(df[df_date.str.contains('December')])} (ROUGHLY {3*len(df[df_date.str.contains('December')]) / 60} HOURS)")

print("\n")

counts_1 = Counter(wrapped[wrapped_artist])
counts_2 = Counter(wrapped[wrapped_song])

most_popular_artist = dict()
most_popular_song = dict()

print(f"I LISTENED TO {len(counts_1.items())} DIFFERENT ARTISTS IN 2025\n")

print(f"I LISTENED TO {len(wrapped)} SONGS IN 2025 (ROUGHLY {3*len(wrapped)} MINUTES OR {3*len(wrapped) / 60} HOURS OR {3*len(wrapped) / 60 / 24} DAYS) \n")

print(f"I LISTENED TO {len(counts_2.items())} DIFFERENT SONGS IN 2025\n")

print("_________________________________________________________\n")

for key, value in counts_1.items():
    if value >= 2:
        most_popular_artist[key] = value

for key, value in counts_2.items():
    if value >= 2:
        most_popular_song[key] = value

most_popular_artist = (dict(sorted(most_popular_artist.items(), key=lambda x:x[1], reverse = True)))
most_popular_song = (dict(sorted(most_popular_song.items(), key=lambda x:x[1], reverse = True)))

print("MY TOP TEN ARTISTS ON SPOTIFY OF 2025")
for i, (artist, count) in enumerate(most_popular_artist.items()):
    if i < 10:
        print(count, artist)

print("\nMY TOP TEN SONGS ON SPOTIFY OF 2025")
for i, (song, count) in enumerate(most_popular_song.items()):
    if i < 10:
        print(count, song)

print("\n")
print("_________________________________________________________\n")
print("\n")

artist_counts = Counter(wrapped[wrapped_artist])
count_taylor_swift = artist_counts.get("Måneskin", 0)  # Cambia "Måneskin" por el artista que quieras
print(f"Måneskin COUNT: {count_taylor_swift}")
print("\n")
