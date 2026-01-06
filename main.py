import sqlite3
import matplotlib.pyplot as plt
from src.db_utils import get_connection, run_query
from src import phase1
from src import phase2
from src import phase3


DB_PATH = "./db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db"


def print_schema(conn):
    rows = run_query(conn, "PRAGMA table_info(daily_weather_entries);")
    print("\nDatabase Schema for daily_weather_entries:")
    for r in rows:
        print(f" - {r['name']} ({r['type']})")

    rows = run_query(conn, "PRAGMA table_info(cities);")
    print("\nSchema for cities:")
    for r in rows:
        print(f" - {r['name']} ({r['type']})")

def main():
    conn = get_connection(DB_PATH)

    try:
        print_schema(conn)

        print("\nPhase 1 Outputs:\n")

        print("All Countries:")
        phase1.select_all_countries(conn)

        print("\nAll Cities:")
        phase1.select_all_cities(conn)  
        
        print("\nAverage Annual Temperature (London, 2023):")
        phase1.average_annual_temperature(conn, city_id=2, year=2023)

        print("\nAverage 7-Day Precipitation (Middlesbrough from 2023-01-01):")
        phase1.average_seven_day_precipitation(conn, city_id=1, start_date="2023-01-01")

        print("\nAverage Mean Temp by City (2023-01-01 to 2023-01-31):")
        phase1.average_mean_temp_by_city(conn, "2023-01-01", "2023-01-31")

        print("\nAverage Annual Precipitation by Country (2023):")
        phase1.average_annual_precipitation_by_country(conn, 2023)

        print("\nExcellent: Wettest City (2023):")
        phase1.wettest_city_by_year(conn, 2023)

        print("\nExcellent: Temperature Variability by City (2023-01-01 to 2023-12-31):")
        phase1.temperature_variability_by_city(conn, "2023-01-01", "2023-12-31")

        print("\nExcellent: Top Rainfall Days (London, 2023):")
        phase1.top_rainfall_days_for_city(conn, city_id=2, year=2023, limit=5)

        print("\n--- Phase 2 Charts ---\n")

        fig1 = phase2.plot_seven_day_precipitation(conn, city_id=1, start_date="2023-01-01")
        phase2.save_figure(fig1, "chart1_7day_precip_city1_2023-01-01")

        fig2 = phase2.plot_daily_min_max_for_month(conn, city_id=2, year=2023, month=12)
        phase2.save_figure(fig2, "chart2_min_max_temp_city2_2023-12")

        fig3 = phase2.plot_avg_daily_precip_by_country(conn, year=2023)
        phase2.save_figure(fig3, "chart3_avg_daily_precip_by_country_2023")

        fig4 = phase2.plot_grouped_temp_stats_by_city(conn, "2023-01-01", "2023-01-31")
        phase2.save_figure(fig4, "chart4_grouped_temp_stats_by_city_2023-01")

        fig5 = phase2.plot_scatter_avg_temp_vs_precip_by_city(conn, "2023-01-01", "2023-12-31")
        phase2.save_figure(fig5, "chart5_scatter_temp_vs_precip_by_city_2023")

        fig6 = phase2.plot_total_precip_by_city(conn, "2023-01-01", "2023-12-31")
        phase2.save_figure(fig6, "chart6_total_precip_by_city_2023")

        print("\n--- Phase 3: API Update ---\n")
        phase3.update_city_weather_from_api(conn, city_id=2, start_date="2025-01-01", end_date="2025-01-14")
        phase3.update_city_weather_from_api(conn, city_id=3, start_date="2025-02-01", end_date="2025-02-28")


        rows = run_query(conn, """
        SELECT COUNT(*) AS cnt
        FROM daily_weather_entries
        WHERE city_id = 2 AND substr(date, 1, 4) = '2025';
        """)
        print(f"Rows for London in 2025 now: {rows[0]['cnt']}")

        rows = run_query(conn, """
        SELECT COUNT(*) AS cnt
        FROM daily_weather_entries
        WHERE city_id = 3 AND substr(date, 1, 4) = '2025';
        """)
        print(f"Rows for Paris in 2025 now: {rows[0]['cnt']}")

        # Show all figures together
        plt.show()

    finally:
        conn.close()

if __name__ == "__main__":
    main()
