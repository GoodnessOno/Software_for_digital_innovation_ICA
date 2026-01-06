from pathlib import Path
import matplotlib.pyplot as plt

def save_figure(fig, filename):
    """
    Saves a matplotlib figure into a 'charts' folder in the project root.
    If fig is None, nothing is saved.
    """
    if fig is None:
        return

    charts_dir = Path("charts")
    charts_dir.mkdir(exist_ok=True)

    # Ensure filename ends with .png
    if not filename.lower().endswith(".png"):
        filename += ".png"

    fig.savefig(charts_dir / filename, dpi=200, bbox_inches="tight")


def plot_seven_day_precipitation(connection, city_id, start_date):
    query = """
    SELECT date, precipitation
    FROM daily_weather_entries
    WHERE city_id = ?
      AND date >= ?
      AND date < date(?, '+7 days')
    ORDER BY date;
    """

    cursor = connection.cursor()
    rows = cursor.execute(query, (city_id, start_date, start_date)).fetchall()

    if not rows:
        print(f"No data found for city_id={city_id} from {start_date} for 7 days.")
        return None

    dates = [r["date"] for r in rows]
    precips = [r["precipitation"] for r in rows]

    fig = plt.figure()
    plt.bar(dates, precips)
    plt.title(f"7-Day Precipitation (City ID {city_id}) from {start_date}")
    plt.xlabel("Date")
    plt.ylabel("Precipitation (mm)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_daily_min_max_for_month(connection, city_id, year, month):
    month_str = f"{int(month):02d}"
    year_str = str(year)

    query = """
    SELECT date, min_temp, max_temp
    FROM daily_weather_entries
    WHERE city_id = ?
      AND substr(date, 1, 4) = ?
      AND substr(date, 6, 2) = ?
    ORDER BY date;
    """

    cursor = connection.cursor()
    rows = cursor.execute(query, (city_id, year_str, month_str)).fetchall()

    if not rows:
        print(f"No data found for city_id={city_id} in {year_str}-{month_str}.")
        return None

    dates = [r["date"] for r in rows]
    mins = [r["min_temp"] for r in rows]
    maxs = [r["max_temp"] for r in rows]

    fig = plt.figure()
    plt.plot(dates, mins, label="Min Temp (°C)")
    plt.plot(dates, maxs, label="Max Temp (°C)")
    plt.title(f"Daily Min/Max Temperature (City ID {city_id}) - {year_str}-{month_str}")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    return fig

def plot_avg_daily_precip_by_country(connection, year):
    """
    Bar chart showing average daily precipitation by country for a given year.
    """
    query = """
    SELECT
        co.name AS country_name,
        AVG(d.precipitation) AS avg_precip
    FROM daily_weather_entries d
    JOIN cities c ON d.city_id = c.id
    JOIN countries co ON c.country_id = co.id
    WHERE substr(d.date, 1, 4) = ?
    GROUP BY co.name
    ORDER BY avg_precip DESC;
    """

    cursor = connection.cursor()
    rows = cursor.execute(query, (str(year),)).fetchall()

    if not rows:
        print(f"No precipitation data found for year={year}.")
        return None

    countries = [r["country_name"] for r in rows]
    avg_precips = [r["avg_precip"] for r in rows]

    fig = plt.figure()
    plt.bar(countries, avg_precips)
    plt.title(f"Average Daily Precipitation by Country ({year})")
    plt.xlabel("Country")
    plt.ylabel("Average Daily Precipitation (mm)")
    plt.tight_layout()
    return fig

def plot_grouped_temp_stats_by_city(connection, date_from, date_to):
    """
    Grouped bar chart showing average min/mean/max temperatures by city
    within a given date range.
    """
    query = """
    SELECT
        c.name AS city_name,
        AVG(d.min_temp) AS avg_min_temp,
        AVG(d.mean_temp) AS avg_mean_temp,
        AVG(d.max_temp) AS avg_max_temp
    FROM daily_weather_entries d
    JOIN cities c ON d.city_id = c.id
    WHERE d.date >= ?
      AND d.date <= ?
    GROUP BY c.name
    ORDER BY c.name;
    """

    cursor = connection.cursor()
    rows = cursor.execute(query, (date_from, date_to)).fetchall()

    if not rows:
        print(f"No temperature data found between {date_from} and {date_to}.")
        return None

    city_names = [r["city_name"] for r in rows]
    mins = [r["avg_min_temp"] for r in rows]
    means = [r["avg_mean_temp"] for r in rows]
    maxs = [r["avg_max_temp"] for r in rows]

    # grouped bars
    x = list(range(len(city_names)))
    width = 0.25

    fig = plt.figure()
    plt.bar([i - width for i in x], mins, width=width, label="Avg Min Temp")
    plt.bar(x, means, width=width, label="Avg Mean Temp")
    plt.bar([i + width for i in x], maxs, width=width, label="Avg Max Temp")

    plt.title(f"Average Temperature Statistics by City ({date_from} to {date_to})")
    plt.xlabel("City")
    plt.ylabel("Temperature (°C)")
    plt.xticks(ticks=x, labels=city_names, rotation=20)
    plt.legend()
    plt.tight_layout()
    return fig

def plot_scatter_avg_temp_vs_precip_by_city(connection, date_from, date_to):
    """
    Scatter plot comparing average mean temperature vs average precipitation per city
    over a given date range.
    """
    query = """
    SELECT
        c.name AS city_name,
        AVG(d.mean_temp) AS avg_temp,
        AVG(d.precipitation) AS avg_precip
    FROM daily_weather_entries d
    JOIN cities c ON d.city_id = c.id
    WHERE d.date >= ?
      AND d.date <= ?
    GROUP BY c.name
    ORDER BY c.name;
    """

    cursor = connection.cursor()
    rows = cursor.execute(query, (date_from, date_to)).fetchall()

    if not rows:
        print(f"No data found between {date_from} and {date_to}.")
        return None

    temps = [r["avg_temp"] for r in rows]
    precips = [r["avg_precip"] for r in rows]
    labels = [r["city_name"] for r in rows]

    fig = plt.figure()
    plt.scatter(temps, precips)
    plt.title(f"Avg Temperature vs Avg Precipitation by City ({date_from} to {date_to})")
    plt.xlabel("Average Mean Temperature (°C)")
    plt.ylabel("Average Daily Precipitation (mm)")

    # annotate each point
    for i, label in enumerate(labels):
        plt.annotate(label, (temps[i], precips[i]))

    plt.tight_layout()
    return fig

def plot_total_precip_by_city(connection, date_from, date_to):
    """
    Bar chart showing total precipitation by city across a date range.
    """
    query = """
    SELECT
        c.name AS city_name,
        SUM(d.precipitation) AS total_precip
    FROM daily_weather_entries d
    JOIN cities c ON d.city_id = c.id
    WHERE d.date >= ?
      AND d.date <= ?
    GROUP BY c.name
    ORDER BY total_precip DESC;
    """

    cursor = connection.cursor()
    rows = cursor.execute(query, (date_from, date_to)).fetchall()

    if not rows:
        print(f"No precipitation data found between {date_from} and {date_to}.")
        return None

    city_names = [r["city_name"] for r in rows]
    totals = [r["total_precip"] for r in rows]

    fig = plt.figure()
    plt.bar(city_names, totals)
    plt.title(f"Total Precipitation by City ({date_from} to {date_to})")
    plt.xlabel("City")
    plt.ylabel("Total Precipitation (mm)")
    plt.xticks(rotation=20)
    plt.tight_layout()
    return fig
