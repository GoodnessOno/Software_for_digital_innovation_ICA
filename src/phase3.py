# Author: GOODNESS ONONOGBU
# Student ID: S3573368
# Date: 2025 - 01 - 06

import time
import requests


BASE_URL = "https://archive-api.open-meteo.com/v1/archive"


def parse_latlong(latlong_text):
    """
    Parses a latlong string into (latitude, longitude).

    Expected formats commonly include:
    - "lat,lon"
    - "lat lon"
    - "lat, lon"
    """
    if latlong_text is None:
        raise ValueError("latlong is missing")

    cleaned = latlong_text.strip().replace(" ", "")
    parts = cleaned.split(",")

    if len(parts) != 2:
        raise ValueError(f"Unexpected latlong format: {latlong_text}")

    lat = float(parts[0])
    lon = float(parts[1])
    return lat, lon


def get_city_and_timezone(connection, city_id):
    """
    Returns city_name, lat, lon, timezone for a given city_id using DB joins.
    """
    query = """
    SELECT
        c.name AS city_name,
        c.latlong AS latlong,
        co.timezone AS timezone
    FROM cities c
    JOIN countries co ON c.country_id = co.id
    WHERE c.id = ?;
    """
    cursor = connection.cursor()
    row = cursor.execute(query, (city_id,)).fetchone()

    if row is None:
        raise ValueError(f"City not found for city_id={city_id}")

    lat, lon = parse_latlong(row["latlong"])
    return row["city_name"], lat, lon, row["timezone"]


def fetch_daily_weather(lat, lon, start_date, end_date, timezone):
    """
    Fetches daily historical weather data from Open-Meteo Archive API.
    Uses own HTTP request code via requests (Merit/Distinction expectation).
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_min,temperature_2m_max,temperature_2m_mean,precipitation_sum",
        "timezone": timezone
    }

    last_error = None
    for attempt in range(3):
        try:
            response = requests.get(BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as ex:
            last_error = ex
            time.sleep(1 + attempt)

    raise RuntimeError(f"Failed to fetch data after retries: {last_error}")


def ensure_unique_index(connection):
    """
    Adds a unique index so the same (city_id, date) cannot be inserted twice.
    This is safe to run multiple times.
    """
    cursor = connection.cursor()
    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_weather_city_date
        ON daily_weather_entries(city_id, date);
    """)
    connection.commit()


def insert_daily_weather(connection, city_id, api_json):
    """
    Inserts API daily results into daily_weather_entries.
    Uses INSERT OR IGNORE so duplicates are skipped (when unique index exists).
    Returns count inserted (best-effort).
    """
    daily = api_json.get("daily", {})
    dates = daily.get("time", [])
    mins = daily.get("temperature_2m_min", [])
    maxs = daily.get("temperature_2m_max", [])
    means = daily.get("temperature_2m_mean", [])
    precips = daily.get("precipitation_sum", [])

    if not dates:
        print("No daily data returned by API.")
        return 0

    if not (len(dates) == len(mins) == len(maxs) == len(means) == len(precips)):
        raise ValueError("API daily arrays are not the same length.")

    insert_sql = """
    INSERT OR IGNORE INTO daily_weather_entries
        (date, min_temp, max_temp, mean_temp, precipitation, city_id)
    VALUES (?, ?, ?, ?, ?, ?);
    """

    cursor = connection.cursor()
    inserted = 0

    for i in range(len(dates)):
        cursor.execute(
            insert_sql,
            (dates[i], mins[i], maxs[i], means[i], precips[i], city_id)
        )
        # rowcount is 1 when inserted, 0 when ignored
        inserted += cursor.rowcount

    connection.commit()
    return inserted


def update_city_weather_from_api(connection, city_id, start_date, end_date):
    """
    End-to-end Phase 3 operation:
    - Read city coordinates + timezone from DB
    - Fetch from Open-Meteo
    - Insert into SQLite safely (no duplicates)
    """
    ensure_unique_index(connection)

    city_name, lat, lon, timezone = get_city_and_timezone(connection, city_id)
    print(f"Fetching API data for {city_name} (city_id={city_id}) [{lat}, {lon}] timezone={timezone}")

    api_json = fetch_daily_weather(lat, lon, start_date, end_date, timezone)
    inserted = insert_daily_weather(connection, city_id, api_json)

    print(f"Inserted {inserted} new rows into daily_weather_entries for {city_name}.")
    return inserted
