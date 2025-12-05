"""
Diagnostic script to check data loading and compatibility issues
Run this in a Jupyter notebook cell to diagnose data problems
"""

import pandas as pd
import numpy as np
from datetime import datetime

def diagnose_data_issues(df_air_quality, df_weather, df_air_quality_clean=None, df_weather_clean=None):
    """
    Comprehensive diagnostic check for data compatibility issues
    """
    print("=" * 70)
    print("DATA DIAGNOSTIC REPORT")
    print("=" * 70)
    
    # Check if dataframes exist
    print("\n1. DATASET EXISTENCE CHECK")
    print("-" * 70)
    print(f"df_air_quality exists: {'✓' if 'df_air_quality' in globals() else '✗'}")
    print(f"df_weather exists: {'✓' if 'df_weather' in globals() else '✗'}")
    
    if df_air_quality is None or df_weather is None:
        print("\n⚠️  CRITICAL: One or both datasets are not loaded!")
        return
    
    # Check raw datasets
    print("\n2. RAW DATASET INFORMATION")
    print("-" * 70)
    print(f"\nAir Quality Dataset:")
    print(f"  Shape: {df_air_quality.shape}")
    print(f"  Columns: {list(df_air_quality.columns)}")
    
    # Check for date columns in air quality
    date_cols_air = [col for col in df_air_quality.columns if 'date' in col.lower() or 'Date' in col]
    print(f"  Date-related columns: {date_cols_air}")
    
    # Check date information if available
    if 'Date' in df_air_quality.columns:
        try:
            # Try to parse dates
            sample_dates = df_air_quality['Date'].head(10).tolist()
            print(f"  Sample dates: {sample_dates}")
            if 'Time' in df_air_quality.columns:
                sample_times = df_air_quality['Time'].head(5).tolist()
                print(f"  Sample times: {sample_times}")
        except:
            pass
    
    print(f"\nWeather Dataset:")
    print(f"  Shape: {df_weather.shape}")
    print(f"  Columns: {list(df_weather.columns)}")
    
    if 'date' in df_weather.columns:
        print(f"  Date range:")
        print(f"    Min: {df_weather['date'].min()}")
        print(f"    Max: {df_weather['date'].max()}")
        print(f"    Unique dates: {df_weather['date'].nunique()}")
    
    if 'city' in df_weather.columns:
        print(f"  Cities: {df_weather['city'].unique().tolist()}")
        print(f"  Number of cities: {df_weather['city'].nunique()}")
    
    # Check for city column in air quality
    city_cols_air = [col for col in df_air_quality.columns if 'city' in col.lower() or 'City' in col]
    print(f"  City-related columns in air quality: {city_cols_air if city_cols_air else 'NONE FOUND'}")
    
    # Check cleaned datasets if provided
    if df_air_quality_clean is not None and df_weather_clean is not None:
        print("\n3. CLEANED DATASET INFORMATION")
        print("-" * 70)
        
        print(f"\nCleaned Air Quality Dataset:")
        print(f"  Shape: {df_air_quality_clean.shape}")
        print(f"  Columns: {list(df_air_quality_clean.columns)}")
        
        if 'date' in df_air_quality_clean.columns:
            print(f"  Date range:")
            print(f"    Min: {df_air_quality_clean['date'].min()}")
            print(f"    Max: {df_air_quality_clean['date'].max()}")
            print(f"    Unique dates: {df_air_quality_clean['date'].nunique()}")
            print(f"    Date type: {df_air_quality_clean['date'].dtype}")
        
        if 'city' in df_air_quality_clean.columns:
            print(f"  Cities: {df_air_quality_clean['city'].unique().tolist()}")
        else:
            print(f"  ⚠️  NO CITY COLUMN FOUND")
        
        print(f"\nCleaned Weather Dataset:")
        print(f"  Shape: {df_weather_clean.shape}")
        print(f"  Columns: {list(df_weather_clean.columns)}")
        
        if 'date' in df_weather_clean.columns:
            print(f"  Date range:")
            print(f"    Min: {df_weather_clean['date'].min()}")
            print(f"    Max: {df_weather_clean['date'].max()}")
            print(f"    Unique dates: {df_weather_clean['date'].nunique()}")
            print(f"    Date type: {df_weather_clean['date'].dtype}")
        
        # Check date overlap
        print("\n4. DATE OVERLAP ANALYSIS")
        print("-" * 70)
        
        if 'date' in df_air_quality_clean.columns and 'date' in df_weather_clean.columns:
            # Normalize dates to date only (remove time component)
            air_dates = set(df_air_quality_clean['date'].dt.date.unique())
            weather_dates = set(df_weather_clean['date'].dt.date.unique())
            
            overlap = air_dates.intersection(weather_dates)
            
            print(f"  Air Quality unique dates: {len(air_dates)}")
            print(f"  Weather unique dates: {len(weather_dates)}")
            print(f"  Overlapping dates: {len(overlap)}")
            
            if len(overlap) == 0:
                print(f"\n  ❌ CRITICAL: NO DATE OVERLAP!")
                print(f"  Air Quality date range: {min(air_dates)} to {max(air_dates)}")
                print(f"  Weather date range: {min(weather_dates)} to {max(weather_dates)}")
            else:
                print(f"  ✓ Date overlap found: {len(overlap)} matching dates")
                print(f"  Sample overlapping dates: {list(overlap)[:5]}")
        
        # Check merge compatibility
        print("\n5. MERGE COMPATIBILITY")
        print("-" * 70)
        
        merge_keys = []
        if 'date' in df_air_quality_clean.columns and 'date' in df_weather_clean.columns:
            merge_keys.append('date')
            print(f"  ✓ 'date' column exists in both datasets")
        else:
            print(f"  ✗ 'date' column missing in one or both datasets")
        
        if 'city' in df_air_quality_clean.columns and 'city' in df_weather_clean.columns:
            merge_keys.append('city')
            print(f"  ✓ 'city' column exists in both datasets")
        else:
            print(f"  ⚠️  'city' column missing in one or both datasets")
            if 'city' not in df_air_quality_clean.columns:
                print(f"     - Missing in air quality dataset")
            if 'city' not in df_weather_clean.columns:
                print(f"     - Missing in weather dataset")
        
        print(f"\n  Merge keys available: {merge_keys}")
        
        # Simulate merge
        if len(merge_keys) > 0:
            try:
                test_merge = pd.merge(
                    df_air_quality_clean,
                    df_weather_clean,
                    on=merge_keys,
                    how='inner'
                )
                print(f"  Test merge result: {test_merge.shape[0]} rows")
                if test_merge.shape[0] == 0:
                    print(f"  ❌ CRITICAL: Merge results in 0 rows!")
                else:
                    print(f"  ✓ Merge successful")
            except Exception as e:
                print(f"  ✗ Merge failed: {e}")
    
    print("\n" + "=" * 70)
    print("END OF DIAGNOSTIC REPORT")
    print("=" * 70)

# Usage instructions
print("""
To use this diagnostic script in your notebook:

1. Run this cell to define the function
2. Then run: diagnose_data_issues(df_air_quality, df_weather, df_air_quality_clean, df_weather_clean)

Or for just raw data:
   diagnose_data_issues(df_air_quality, df_weather)
""")

