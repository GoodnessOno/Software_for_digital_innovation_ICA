**STUDENT ID - S3573368**
**STUDENT NAME - GOODNESS ONONOGBU**
**Historical Weather Insights — ICA (Software for Digital Innovation)**

Innovation begins with structure, and structure earns trust. This project implements a modular Python application that retrieves, analyses, visualises, and extends **historical weather data** using a local relational database and external archive API calls, all designed with resilience and integrity at its core.

The system is built in **three phases**, enhanced with a **CLI layer (`argparse`)** for flexible runtime behaviour control without hardcoded parameters.

---

## **Project Features**

### **Phase 1 — Relational Queries and Analytics**

* Retrieves all countries and cities using SQL joins
* Computes annual temperature averages
* Computes 7-day precipitation aggregates
* Ranks wettest cities and temperature variability ranges
* Outputs all float values to **2 decimal places** for readability

### **Phase 2 — Comparative Static Charts**

Generates and saves:

1. 7-Day Precipitation by City
2. Daily Min/Max Temperatures by Month
3. Average Daily Precipitation by Country
4. Grouped Temperature Stats by City
5. Avg Temperature vs Avg Precipitation (Scatter)
6. Total Precipitation by City (Ranked)

Charts are stored as PNG artefacts in:

```
/charts/
```

### **Phase 3 — Archive API Retrieval + DB Extension**

* Parses coordinates and timezone from the database
* Fetches 14-day historical weather from Open-Meteo
* Inserts new rows without duplication using a **unique city-date index**
* Gracefully handles invalid URLs or offline failures using controlled retries
* Preserves database integrity even under failure conditions

---

## **Project Folder Structure**

```
/s3573368_ICA_Software_for_digital_innovation/
   ├── src/
   │     ├── db_utils.py
   │     ├── phase1.py
   │     ├── phase2.py
   │     ├── phase3.py
   │     ├── pycache
   ├── db/
   │     ├── CIS4044-N-SDI-OPENMETEO-PARTIAL.db
├── charts/  (generated static charts saved here)
├── main.py  (application runner)
├── README.md  (this file)
```

---

## **Installation and Dependencies**

Python Version:

```
3.14.2
```

Install required external libraries:

```
pip install requests matplotlib
```

*(Note: `argparse`, `sqlite3`, `os`, `typing` are standard library modules and require no installation.)*

---

## **How to Run the Application**

The system now supports CLI-driven behaviour. You may run:
```
python main.py
```

## **Assumptions**

* `city_id` values must exist in the `cities` table
* Dates should follow `YYYY-MM-DD` format
* `latlong` in DB is stored as `"<lat>,<long>"`
* Charts are static and saved as PNG for traceability and reporting

---

## **Testing Integrity**

The application has undergone structured **black-box testing** validating:

* valid/invalid inputs
* empty datasets
* duplicate prevention
* offline/API failures
* graceful error messaging without crashes

All test outputs are unique to this implementation and were generated from real database and API runtime results, reinforcing originality and independent execution.

---


