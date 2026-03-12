import requests
import pandas as pd
import os
from datetime import datetime, timedelta

def fetch_and_append():
    end   = datetime.today().strftime("%Y-%m-%d")
    start = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude":   28.0871,
        "longitude":  30.7618,
        "start_date": start,
        "end_date":   end,
        "hourly": [
            "temperature_2m",
            "dewpoint_2m",
            "relativehumidity_2m",
            "precipitation",
            "windspeed_10m"
        ],
        "timezone": "Africa/Cairo"
    }

    r = requests.get(url, params=params)
    df_new = pd.DataFrame(r.json()["hourly"])

    path = "data/minia_weather.csv"
    os.makedirs("data", exist_ok=True)

    if os.path.exists(path):
        df_old = pd.read_csv(path)
        df = pd.concat([df_old, df_new]).drop_duplicates("time")
    else:
        df = df_new

    df.to_csv(path, index=False)
    print(f"✅ Saved {len(df_new)} rows — Total: {len(df)}")

fetch_and_append()
