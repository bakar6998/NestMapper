"""
clean_data.py
Cleans and processes all NYC Open Data files
and prepares them for loading into PostgreSQL

Run with:
python scripts/clean_data.py
"""

import pandas as pd
import numpy as np
import json
import os

# Paths
RAW_DATA_PATH = 'data/raw/'
CLEANED_DATA_PATH = 'data/cleaned/'

print("🗽 NestMapper NYC — Data Cleaning Pipeline")
print("=" * 50)


def clean_subway_stations():
    """
    Cleans MTA subway stations data
    Extracts subway lines per neighborhood
    """
    print("\n🚇 Cleaning subway stations data...")

    try:
        df = pd.read_csv(
            f'{RAW_DATA_PATH}subway_stations.csv'
        )

        print(f"Raw columns: {df.columns.tolist()}")
        print(f"Total stations: {len(df)}")

        # Keep only relevant columns
        # Column names may vary — adjust if needed
        relevant_cols = []
        for col in df.columns:
            if any(keyword in col.lower() for keyword in
                   ['name', 'line', 'borough', 'lat', 'lon',
                    'gtfs', 'stop', 'nta']):
                relevant_cols.append(col)

        df_clean = df[relevant_cols].copy()

        # Remove duplicates
        df_clean = df_clean.drop_duplicates()

        # Remove null values
        df_clean = df_clean.dropna()

        # Save cleaned data
        df_clean.to_csv(
            f'{CLEANED_DATA_PATH}subway_stations.csv',
            index=False
        )

        print(f"✅ Cleaned stations: {len(df_clean)}")
        print(f"Columns kept: {relevant_cols}")
        return df_clean

    except Exception as e:
        print(f"❌ Error cleaning subway data: {e}")
        return None


def clean_crime_data():
    """
    Cleans NYPD crime data
    Calculates crime index per neighborhood
    """
    print("\n🚔 Cleaning crime data...")

    try:
        # Read only needed columns to save memory
        df = pd.read_csv(
            f'{RAW_DATA_PATH}crime_data.csv',
            usecols=lambda x: any(
                keyword in x.upper() for keyword in
                ['BORO', 'LAW_CAT', 'NTA', 'LAT', 'LON',
                 'OFNS', 'PD_DESC', 'CMPLNT']
            ),
            low_memory=False
        )

        print(f"Raw columns: {df.columns.tolist()}")
        print(f"Total complaints: {len(df)}")

        # Remove nulls
        df = df.dropna()

        # Group by borough and count crimes
        if 'BORO_NM' in df.columns:
            borough_crime = df.groupby('BORO_NM').size().reset_index()
            borough_crime.columns = ['borough', 'crime_count']
            print("\nCrime by borough:")
            print(borough_crime)

            # Save
            borough_crime.to_csv(
                f'{CLEANED_DATA_PATH}crime_by_borough.csv',
                index=False
            )

        # Save full cleaned data
        df.to_csv(
            f'{CLEANED_DATA_PATH}crime_data.csv',
            index=False
        )

        print(f"✅ Cleaned crime records: {len(df)}")
        return df

    except Exception as e:
        print(f"❌ Error cleaning crime data: {e}")
        return None


def clean_schools_data():
    """
    Cleans NYC schools data
    Counts schools per neighborhood
    """
    print("\n🏫 Cleaning schools data...")

    try:
        df = pd.read_csv(
            f'{RAW_DATA_PATH}schools.csv'
        )

        print(f"Raw columns: {df.columns.tolist()}")
        print(f"Total schools: {len(df)}")

        # Keep relevant columns
        keep_cols = [col for col in df.columns if any(
            keyword in col.lower() for keyword in
            ['name', 'boro', 'lat', 'lon',
             'nta', 'geographic', 'location']
        )]

        df_clean = df[keep_cols].copy()

        # Remove duplicates and nulls
        df_clean = df_clean.drop_duplicates()
        df_clean = df_clean.dropna(
            subset=['Latitude', 'Longitude']
            if 'Latitude' in df_clean.columns
            else df_clean.columns[:2]
        )

        # Count schools by borough
        if 'Geographic' in df_clean.columns:
            schools_by_borough = df_clean.groupby(
                'Geographic'
            ).size().reset_index()
            schools_by_borough.columns = [
                'borough', 'school_count'
            ]
            print("\nSchools by borough:")
            print(schools_by_borough)

        # Save
        df_clean.to_csv(
            f'{CLEANED_DATA_PATH}schools.csv',
            index=False
        )

        print(f"✅ Cleaned schools: {len(df_clean)}")
        return df_clean

    except Exception as e:
        print(f"❌ Error cleaning schools data: {e}")
        return None


def clean_neighborhoods_geojson():
    """
    Cleans NYC neighborhood boundaries GeoJSON
    Extracts neighborhood names and boroughs
    """
    print("\n🗺️ Cleaning neighborhoods GeoJSON...")

    try:
        # Find geojson file
        geojson_files = [
            f for f in os.listdir(RAW_DATA_PATH)
            if f.endswith('.geojson')
        ]

        if not geojson_files:
            print("❌ No GeoJSON file found!")
            return None

        geojson_file = geojson_files[0]
        print(f"Found: {geojson_file}")

        with open(f'{RAW_DATA_PATH}{geojson_file}') as f:
            data = json.load(f)

        features = data['features']
        print(f"Total neighborhoods: {len(features)}")

        # Extract properties
        neighborhoods = []
        for feature in features:
            props = feature['properties']
            neighborhoods.append(props)

        df = pd.DataFrame(neighborhoods)
        print(f"Columns: {df.columns.tolist()}")
        print("\nSample data:")
        print(df.head(3))

        # Save
        df.to_csv(
            f'{CLEANED_DATA_PATH}neighborhoods.csv',
            index=False
        )

        print(f"✅ Cleaned neighborhoods: {len(df)}")
        return df

    except Exception as e:
        print(f"❌ Error cleaning GeoJSON: {e}")
        return None


def main():
    """
    Runs all cleaning functions
    """
    print("\nStarting data cleaning pipeline...")

    # Create cleaned folder if not exists
    os.makedirs(CLEANED_DATA_PATH, exist_ok=True)

    # Run all cleaners
    neighborhoods = clean_neighborhoods_geojson()
    subway = clean_subway_stations()
    crime = clean_crime_data()
    schools = clean_schools_data()

    print("\n" + "=" * 50)
    print("✅ Data cleaning complete!")
    print(f"Neighborhoods: {len(neighborhoods) if neighborhoods is not None else 0}")
    print(f"Subway stations: {len(subway) if subway is not None else 0}")
    print(f"Crime records: {len(crime) if crime is not None else 0}")
    print(f"Schools: {len(schools) if schools is not None else 0}")
    print("\nCleaned files saved to data/cleaned/")
    print("Next step: Run seed_data.py to load into PostgreSQL")


if __name__ == '__main__':
    main()