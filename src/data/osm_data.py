# -*- coding: utf-8 -*-
"""
src/data/osm_data.py

Yerel olarak kaydedilmiş elazig_osm.graphml dosyasını yükler,
ağını projekte eder ve verilen koordinatlara göre
mesafe matrisini (km) oluşturur.
"""

import osmnx as ox
import networkx as nx
import numpy as np
import streamlit as st
from typing import List, Tuple
from pathlib import Path

@st.cache_resource(show_spinner=False)
def load_osm_graph() -> nx.Graph:
    """
    Elâzığ'ın OSM GraphML dosyasını yükler ve görüntüyü projekte eder.
    Dosya konumu, bu dosyanın bulunduğu klasöre göre dinamik olarak belirlenir.
    Returns:
      - Projected NetworkX Graph (kenar ağırlığı: "length").
    """
    base_dir = Path(__file__).parent  # src/data klasörü
    graphml_path = base_dir / "elazig_osm.graphml"

    if not graphml_path.exists():
        raise FileNotFoundError(f"OSM GraphML bulunamadı: {graphml_path}")

    graph = ox.load_graphml(str(graphml_path))
    graph_proj = ox.project_graph(graph)  # Projeksiyon yaparak KDTree bağımlılığı kaldırılır
    return graph_proj

@st.cache_data(show_spinner=False)
def compute_distance_matrix(
    _graph: nx.Graph,
    location_coords: List[Tuple[float, float]]
) -> np.ndarray:
    """
    Proje edilmiş OSM grafiği üzerinden her koordinat çifti için
    en kısa yol mesafesini (kilometre cinsinden) hesaplar.
    Args:
      - _graph: load_osm_graph() tarafından dönen proje edilmiş grafik.
      - location_coords: [(latitude, longitude), ...] listesi.
    Returns:
      - (n x n) numpy.ndarray mesafe matrisi (km).
    """
    graph_proj = _graph

    # 1. Her (lat, lon) noktasını aynı CRS'e projekte et
    from shapely.geometry import Point
    projected_points = []
    for lat, lon in location_coords:
        geom = Point(lon, lat)
        geom_proj = ox.projection.project_geometry(geom, to_crs=graph_proj.graph["crs"])[0]
        projected_points.append((geom_proj.x, geom_proj.y))

    n = len(projected_points)
    dist_matrix = np.zeros((n, n), dtype=float)

    # 2. Her proje edilmiş nokta için en yakın node'u bul
    nodes = []
    for x, y in projected_points:
        node = ox.distance.nearest_nodes(graph_proj, X=x, Y=y)
        nodes.append(node)

    # 3. i<j çiftleri arasında en kısa yolu Dijkstra ile hesapla
    for i in range(n):
        for j in range(i + 1, n):
            try:
                length_m = nx.shortest_path_length(
                    graph_proj,
                    source=nodes[i],
                    target=nodes[j],
                    weight="length"
                )
                km = length_m / 1000.0
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                km = float("inf")
            dist_matrix[i, j] = km
            dist_matrix[j, i] = km

    # 4. Diyagonal değerleri (i,i) çok küçük yap (0 bölünme hatasını önlemek için)
    np.fill_diagonal(dist_matrix, 1e-10)
    return dist_matrix
