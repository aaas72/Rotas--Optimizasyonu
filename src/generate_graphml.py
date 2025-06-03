# -*- coding: utf-8 -*-
"""
generate_graphml.py

Elâzığ ilinin OSM yol ağını indirir ve
src/data/elazig_osm.graphml dosyasına kaydeder.

Bu dosyayı yalnızca bir kez çalıştırın.
"""

import osmnx as ox
from pathlib import Path

def main():
    print("Başlatılıyor: Elâzığ OSM verisi indiriliyor...")

    place_name = "Elâzığ, Turkey"
    network_type = "drive"

    print(f"OSM'den '{place_name}' bölgesi yükleniyor...")
    graph = ox.graph_from_place(place_name, network_type=network_type)

    print("Ağ kenarlarına uzunluk (length) bilgisi ekleniyor...")
    ox.distance.add_edge_lengths(graph)

    output_dir = Path("src/data")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "elazig_osm.graphml"
    print(f"GraphML dosyası kaydediliyor: {output_path}")
    ox.save_graphml(graph, filepath=str(output_path))

    print("Başarıyla kaydedildi: elazig_osm.graphml")
    print("generate_graphml.py işlemi tamamlandı.")

if __name__ == "__main__":
    main()
