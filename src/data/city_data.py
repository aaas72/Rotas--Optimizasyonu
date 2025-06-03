# -*- coding: utf-8 -*-
"""
src/data/city_data.py

Varsayılan şehir listesini veya harici bir CSV dosyasından
şehir verilerini yükleme fonksiyonları.
"""

import pandas as pd
from typing import Dict, Tuple

def load_default_cities() -> Dict[str, Tuple[float, float]]:
    """
    Türkiye'deki örnek şehirlerin koordinatlarını döner.
    Format: { "ŞehirAdı": (latitude, longitude), ... }
    """
    return {
        "İstanbul": (41.0082, 28.9784),
        "Ankara":   (39.9334, 32.8597),
        "İzmir":    (38.4192, 27.1287),
        "Bursa":    (40.1826, 29.0665),
        "Antalya":  (36.8969, 30.7133),
        "Adana":    (37.0000, 35.3213),
        "Konya":    (37.8667, 32.4833),
        "Gaziantep": (37.0662, 37.3833),
        "Şanlıurfa": (37.1500, 38.8000),
        "Trabzon":  (41.0000, 39.7167)
    }

def load_cities_from_csv(
    path,
    lat_col: str = "latitude",
    lon_col: str = "longitude",
    name_col: str = "name"
) -> Dict[str, Tuple[float, float]]:
    """
    CSV dosyasından şehir listesini okur. Gerekli kolonlar: latitude, longitude, name.
    Format: { "ŞehirAdı": (latitude, longitude), ... }
    """
    df = pd.read_csv(path)
    required_cols = {lat_col, lon_col, name_col}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"CSV dosyası şu kolonları içermeli: {required_cols}")

    cities: Dict[str, Tuple[float, float]] = {}
    for _, row in df.iterrows():
        cities[row[name_col]] = (float(row[lat_col]), float(row[lon_col]))
    return cities
