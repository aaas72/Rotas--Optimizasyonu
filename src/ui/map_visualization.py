# -*- coding: utf-8 -*-
"""
src/ui/map_visualization.py

Folium kullanarak optimize edilmiş rotayı harita üzerinde gösterir.
"""

import folium
import numpy as np
from streamlit_folium import st_folium
from typing import Dict, Tuple, List

def show_route_map(
    locations: Dict[str, Tuple[float, float]],
    route: List[int],
    map_width: int = 800,
    map_height: int = 500
) -> None:
    """
    Teslimat noktalarını ve en iyi rotayı Folium haritasında çizer.
    Args:
      - locations: { "YerAdı": (latitude, longitude), ... }
      - route: [0, 2, 1, 3, 0] gibi indekslerden oluşan rota listesi.
      - map_width/map_height: Harita boyutları (Streamlit görünümü için).
    """
    location_names = list(locations.keys())
    coords = list(locations.values())

    # Haritayı noktaların ortalaması civarında başlat
    center_lat = np.mean([c[0] for c in coords])
    center_lon = np.mean([c[1] for c in coords])
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles="OpenStreetMap")

    # Rota çizgisi (PolyLine)
    route_coords = [coords[idx] for idx in route]
    folium.PolyLine(
        locations=route_coords,
        color="red",
        weight=3,
        opacity=0.8
    ).add_to(m)

    # Rota üzerindeki noktalara işaretçi ekle (öncelik sırasına göre)
    for pos, idx in enumerate(route[:-1]):  # son öğe, başlangıca dönüş olduğu için ekleme yapılmaz
        name = location_names[idx]
        lat, lon = coords[idx]
        color = "darkgreen" if pos == 0 else "blue"
        popup_html = f"<b>{name}</b><br>Öncelik: {pos + 1}"
        folium.Marker(
            location=(lat, lon),
            popup=popup_html,
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(m)

    # Rotada olmayan noktaları gri simgeyle ekle
    remaining = set(range(len(location_names))) - set(route)
    for idx in remaining:
        name = location_names[idx]
        lat, lon = coords[idx]
        folium.Marker(
            location=(lat, lon),
            popup=f"<b>{name}</b><br>(Rota Dışı)",
            icon=folium.Icon(color="gray", icon="home")
        ).add_to(m)

    st_folium(m, width=map_width, height=map_height)
