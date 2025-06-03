# -*- coding: utf-8 -*-
"""
src/data/location_data.py

Elâzığ içindeki teslimat/ticari noktaların genişletilmiş listesi ve
CSV'den yükleme işlevleri.
"""

import pandas as pd
from typing import Dict, Tuple

def load_default_locations() -> Dict[str, Tuple[float, float]]:
    """
    Elâzığ içindeki yaygın olarak kullanılan 20+ noktanın (örneğin
    alışveriş merkezleri, parklar, tarihi alanlar, üniversiteler, vb.)
    koordinatlarını döner.
    Format: { "YerAdı": (latitude, longitude), ... }
    """
    return {
        "Elâzığ Merkez Yaya Merkezi":        (38.6744, 39.2220),
        "Forum AVM Elazığ":                  (38.6736, 39.2167),
        "Elâzığ Belediye Market":            (38.6794, 39.2248),
        "Şehirlerarası Otobüs Terminali":     (38.6732, 39.2211),
        "Elâzığ Devlet Hastanesi":            (38.6658, 39.2192),
        "Elâzığ Üniversitesi":                (38.6565, 39.2241),
        "Harput Kalesi":                      (38.6975, 39.2356),
        "Fethi Paşa Parkı":                   (38.6750, 39.2235),
        "Buzluk Mağarası":                    (38.6780, 39.2350),
        "Karakama Tünelleri":                 (38.6930, 39.1810),
        "Elâzığ Müzesi":                      (38.6740, 39.2270),
        "Elâzığ Kapalı Spor Salonu":           (38.6650, 39.2140),
        "Emek Mahallesi Cami":                (38.6755, 39.2180),
        "Hamamönü Çarşısı":                   (38.6760, 39.2240),
        "Kent Park":                          (38.6785, 39.2275),
        "Dilaver Yılmaz Parkı":               (38.6782, 39.2108),
        "Hayrettin Karaca Öğrenci Yurdu":     (38.6600, 39.2170),
        "8 Şubat Stadı":                      (38.6630, 39.2160),
        "Elâzığ Valiliği Binası":              (38.6755, 39.2205),
        "Elâzığ Otobüs Garajı":               (38.6725, 39.2218),
    }

def load_locations_from_csv(
    path,
    lat_col: str = "latitude",
    lon_col: str = "longitude",
    name_col: str = "name"
) -> Dict[str, Tuple[float, float]]:
    """
    CSV dosyasından teslimat/ticari nokta listesini okur.
    Gerekli kolonlar: name, latitude, longitude.
    Format: { "YerAdı": (latitude, longitude), ... }
    """
    df = pd.read_csv(path)
    required_cols = {name_col, lat_col, lon_col}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"CSV dosyası şu kolonları içermeli: {required_cols}")

    locations: Dict[str, Tuple[float, float]] = {}
    for _, row in df.iterrows():
        locations[row[name_col]] = (float(row[lat_col]), float(row[lon_col]))
    return locations
