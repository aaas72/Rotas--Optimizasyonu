# -*- coding: utf-8 -*-
"""
src/aco/utils.py

ACO algoritması veya başka yerler için yardımcı fonksiyonlar içerir.
Örnek: Haversine mesafesi hesaplama fonksiyonu.
"""

import math
from typing import Tuple

def haversine_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    İki nokta arasındaki büyük daire (great-circle) mesafesini
    Haversine formülü ile hesaplar.
    Args:
      - coord1: (latitude, longitude) formatında birinci nokta.
      - coord2: (latitude, longitude) formatında ikinci nokta.
    Returns:
      - Mesafe (kilometre cinsinden).
    """
    R = 6371.0  # Dünya yarıçapı (km)

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = math.sin(d_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c
