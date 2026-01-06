# Author: GOODNESS ONONOGBU
# Student ID: S3573368
# Date: 2025 - 01 - 06

import sqlite3

# Phase 1 - Starter
# Note: Display all real/float numbers to 2 decimal places.

def select_all_countries(connection):
    """
    Selects all countries from the countries table and prints them.
    """
    try:
        query = "SELECT id, name, timezone FROM countries ORDER BY name;"
        cursor = connection.cursor()
        results = cursor.execute(query)

        for row in results:
            print(
                f"Country Id: {row['id']} -- "
                f"Country Name: {row['name']} -- "
                f"Timezone: {row['timezone']}"
            )

    except sqlite3.OperationalError as ex:
        print(ex)


def select_all_cities(connection):
    """
    Selects all cities and prints each city with its country and timezone.
    """
    try:
        query = """
        SELECT
            c.id AS city_id,
            c.name AS city_name,
            co.id AS country_id,
            co.name AS country_name,
            co.timezone AS timezone
        FROM cities c
        JOIN countries co ON c.country_id = co.id
        ORDER BY co.name, c.name;
        """

        cursor = connection.cursor()
        results = cursor.execute(query)

        for row in results:
            print(
                f"City Id: {row['city_id']} -- City: {row['city_name']} | "
                f"Country: {row['country_name']} (Id: {row['country_id']}) | "
                f"Timezone: {row['timezone']}"
            )

    except sqlite3.OperationalError as ex:
        print(ex)

'''
Good

In additional to successfully completing *all* the "Satisfactory" queries, 
implement the queries that satisfy the each query requirements indicated by the name
of the function and any parameters to achieve a potential mark in the range 60-69.
'''
def average_annual_temperature(connection, city_id, year):
    """
    Prints the average mean temperature for a given city in a given year.
    Output is displayed to 2 decimal places.
    """
    try:
        query = """
        SELECT AVG(d.mean_temp) AS avg_temp
        FROM daily_weather_entries d
        WHERE d.city_id = ?
          AND substr(d.date, 1, 4) = ?;
        """

        cursor = connection.cursor()
        row = cursor.execute(query, (city_id, str(year))).fetchone()

        avg_temp = row["avg_temp"]
        if avg_temp is None:
            print(f"No temperature data found for city_id={city_id} in year={year}.")
            return

        print(f"Average annual mean temperature (city_id={city_id}, year={year}): {avg_temp:.2f}°C")

    except sqlite3.OperationalError as ex:
        print(ex)


def average_seven_day_precipitation(connection, city_id, start_date):
    """
    Prints the average precipitation for a 7-day window starting from start_date (inclusive)
    for a given city_id.
    start_date must be in YYYY-MM-DD format.
    Output is displayed to 2 decimal places.
    """
    try:
        query = """
        SELECT AVG(d.precipitation) AS avg_precip
        FROM daily_weather_entries d
        WHERE d.city_id = ?
          AND d.date >= ?
          AND d.date < date(?, '+7 days');
        """

        cursor = connection.cursor()
        row = cursor.execute(query, (city_id, start_date, start_date)).fetchone()

        avg_precip = row["avg_precip"]
        if avg_precip is None:
            print(f"No precipitation data found for city_id={city_id} starting from {start_date}.")
            return

        print(
            f"Average 7-day precipitation (city_id={city_id}, start_date={start_date}): "
            f"{avg_precip:.2f} mm"
        )

    except sqlite3.OperationalError as ex:
        print(ex)


'''
Very good

In additional to successfully completing *all* the "Satisfactory" and "Good" queries, 
implement the queries that satisfy the each query requirements indicated by the name
of the function and any parameters to achieve a potential mark in the range 70-79.
'''
def average_mean_temp_by_city(connection, date_from, date_to):
    """
    Prints the average mean temperature per city between date_from and date_to (inclusive).
    Dates must be in YYYY-MM-DD format.
    """
    try:
        query = """
        SELECT
            c.id AS city_id,
            c.name AS city_name,
            AVG(d.mean_temp) AS avg_mean_temp
        FROM daily_weather_entries d
        JOIN cities c ON d.city_id = c.id
        WHERE d.date >= ?
          AND d.date <= ?
        GROUP BY c.id, c.name
        ORDER BY avg_mean_temp DESC;
        """

        cursor = connection.cursor()
        results = cursor.execute(query, (date_from, date_to)).fetchall()

        if not results:
            print(f"No results found between {date_from} and {date_to}.")
            return

        print(f"Average mean temperature by city ({date_from} to {date_to}):")
        for row in results:
            print(
                f" - {row['city_name']} (city_id={row['city_id']}): "
                f"{row['avg_mean_temp']:.2f}°C"
            )

    except sqlite3.OperationalError as ex:
        print(ex)

def average_annual_precipitation_by_country(connection, year):
    """
    Prints the average daily precipitation per country for a given year.
    Output displayed to 2 decimal places.
    """
    try:
        query = """
        SELECT
            co.id AS country_id,
            co.name AS country_name,
            AVG(d.precipitation) AS avg_precip
        FROM daily_weather_entries d
        JOIN cities c ON d.city_id = c.id
        JOIN countries co ON c.country_id = co.id
        WHERE substr(d.date, 1, 4) = ?
        GROUP BY co.id, co.name
        ORDER BY avg_precip DESC;
        """

        cursor = connection.cursor()
        results = cursor.execute(query, (str(year),)).fetchall()

        if not results:
            print(f"No precipitation data found for year={year}.")
            return

        print(f"Average daily precipitation by country (year={year}):")
        for row in results:
            print(
                f" - {row['country_name']} (country_id={row['country_id']}): "
                f"{row['avg_precip']:.2f} mm"
            )

    except sqlite3.OperationalError as ex:
        print(ex)


'''
Excellent

To achieve 80+ you will identify several suitable queries of your own that go beyond 
basic requirements for this phase.
'''

def wettest_city_by_year(connection, year):
    """
    Prints the city with the highest total precipitation in a given year.
    """
    try:
        query = """
        SELECT
            c.id AS city_id,
            c.name AS city_name,
            SUM(d.precipitation) AS total_precip
        FROM daily_weather_entries d
        JOIN cities c ON d.city_id = c.id
        WHERE substr(d.date, 1, 4) = ?
        GROUP BY c.id, c.name
        ORDER BY total_precip DESC
        LIMIT 1;
        """

        cursor = connection.cursor()
        row = cursor.execute(query, (str(year),)).fetchone()

        if row is None:
            print(f"No precipitation data found for year={year}.")
            return

        print(
            f"Wettest city in {year}: {row['city_name']} (city_id={row['city_id']}) "
            f"with total precipitation {row['total_precip']:.2f} mm"
        )

    except sqlite3.OperationalError as ex:
        print(ex)

def temperature_variability_by_city(connection, date_from, date_to):
    """
    Prints temperature variability (max of max_temp - min of min_temp) per city
    within a date range. Higher values indicate more extreme temperature swings.
    """
    try:
        query = """
        SELECT
            c.id AS city_id,
            c.name AS city_name,
            (MAX(d.max_temp) - MIN(d.min_temp)) AS temp_range
        FROM daily_weather_entries d
        JOIN cities c ON d.city_id = c.id
        WHERE d.date >= ?
          AND d.date <= ?
        GROUP BY c.id, c.name
        ORDER BY temp_range DESC;
        """

        cursor = connection.cursor()
        results = cursor.execute(query, (date_from, date_to)).fetchall()

        if not results:
            print(f"No temperature data found between {date_from} and {date_to}.")
            return

        print(f"Temperature variability by city ({date_from} to {date_to}):")
        for row in results:
            print(
                f" - {row['city_name']} (city_id={row['city_id']}): "
                f"{row['temp_range']:.2f}°C range"
            )

    except sqlite3.OperationalError as ex:
        print(ex)

def top_rainfall_days_for_city(connection, city_id, year, limit=5):
    """
    Prints the top rainfall days for a city in a given year.
    """
    try:
        query = """
        SELECT
            d.date AS date,
            d.precipitation AS precipitation
        FROM daily_weather_entries d
        WHERE d.city_id = ?
          AND substr(d.date, 1, 4) = ?
        ORDER BY d.precipitation DESC
        LIMIT ?;
        """

        cursor = connection.cursor()
        results = cursor.execute(query, (city_id, str(year), int(limit))).fetchall()

        if not results:
            print(f"No rainfall data found for city_id={city_id} in year={year}.")
            return

        print(f"Top {limit} rainfall days for city_id={city_id} in {year}:")
        for row in results:
            print(f" - {row['date']}: {row['precipitation']:.2f} mm")

    except sqlite3.OperationalError as ex:
        print(ex)



if __name__ == "__main__":
    # Create a SQLite3 connection and call the various functions
    # above, printing the results to the terminal.
    pass