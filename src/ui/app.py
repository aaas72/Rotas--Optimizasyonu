# -*- coding: utf-8 -*-
"""
src/ui/app.py

Streamlit arayüzü:
- Teslimat/ticari noktaları (Elâzığ) seçmek için:
  1) Varsayılan listedeki noktaları işaretlemek
  2) Haritaya tıklayarak yeni noktalar eklemek
- ACO parametrelerini ayarlamak
- En uygun rotayı hesaplayıp harita ve grafiklerle sonuçları göstermek
"""

import streamlit as st
import pandas as pd
import numpy as np
import logging
import os
import sys

# Proje kök dizinini PYTHONPATH’e ekleyelim, böylece modüllerimizi kolayca import ederiz
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# OSM verisini yükleyen ve mesafe matrisi oluşturan işlevler
from data.osm_data import load_osm_graph, compute_distance_matrix

# Ön tanımlı noktaları ve CSV’den gelen noktaları yükleyen işlevler
from data.location_data import load_default_locations, load_locations_from_csv

# ACO algoritmasını içeren sınıf
from aco.algorithm import ACO

# Harita ve grafik görselleştirme işlevleri
from ui.map_visualization import show_route_map
from ui.plots import plot_convergence, show_distance_matrix_heatmap

# Harita üzerindeki tıklamaları almak için gerekli paketler
from streamlit_folium import st_folium
import folium

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_session():
    """
    Streamlit oturumu için gerekli session_state değişkenlerini başlatır.
    """
    if "results" not in st.session_state:
        st.session_state.results = None
    if "selected_locations" not in st.session_state:
        st.session_state.selected_locations = {}
    if "clicked_points" not in st.session_state:
        st.session_state.clicked_points = []


def main():
    # Sayfa başlığı ve yerleşim ayarları
    st.set_page_config(page_title="Elâzığ Teslimat Rotası Optimizasyonu", layout="wide")
    st.title("Elâzığ Teslimat Rotası Optimizasyonu")
    st.markdown("Ant Colony Optimization (ACO) algoritması kullanarak Elâzığ'daki teslimat rotasını optimize edin.")
    st.markdown("---")

    initialize_session()

    # ====== Kenar Çubuğu: Nokta Seçim Yöntemi ve ACO Parametreleri ====== #
    with st.sidebar:
        st.header("1. Nokta Seçim Yöntemi")

        # Kullanıcıya iki seçenek sunuyoruz: Liste veya Harita
        selection_method = st.radio(
            "Nokta Nasıl Seçilsin?",
            ("Varsayılan Liste", "Haritadan Tıkla")
        )

        # ----- Varsayılan Liste ile Nokta Seçim Bölümü ----- #
        if selection_method == "Varsayılan Liste":
            st.write("Varsayılan noktalar arasından seçim yapın veya CSV dosyası yükleyin.")

            data_source = st.radio(
                "Veri Kaynağı:",
                ("Varsayılan Noktalar", "CSV Yükle")
            )

            # Varsayılan noktalar listesinden seçim
            if data_source == "Varsayılan Noktalar":
                default_locs = load_default_locations()
                search_query = st.text_input("Nokta Ara:", "")
                # Arama sorgusuna göre listeyi filtreleyelim
                filtered = {
                    name: coord
                    for name, coord in default_locs.items()
                    if search_query.lower() in name.lower()
                }
                selected = {}
                for name, coord in filtered.items():
                    if st.checkbox(f"{name} ({coord[0]:.4f}, {coord[1]:.4f})", key=name):
                        selected[name] = coord
                if len(selected) < 2:
                    st.info("Lütfen en az 2 nokta seçin.")
                st.session_state.selected_locations = selected

            # CSV dosyası yükleme bölümü
            else:
                st.write("CSV dosyası yükleyin. Gerekli kolonlar: name, latitude, longitude")
                uploaded_file = st.file_uploader("CSV Dosyası Seç", type=["csv"])
                if uploaded_file is not None:
                    try:
                        locs_from_csv = load_locations_from_csv(
                            path=uploaded_file,
                            lat_col="latitude",
                            lon_col="longitude",
                            name_col="name"
                        )
                        st.success(f"{len(locs_from_csv)} nokta yüklendi.")
                        st.session_state.selected_locations = locs_from_csv
                    except Exception as e:
                        st.error(f"CSV yüklenirken hata: {e}")
                        st.session_state.selected_locations = {}

        # ----- Haritadan Tıklayarak Nokta Seçim Bölümü ----- #
        else:
            st.write("Haritaya tıklayarak en az 2 nokta seçin.")

            # “Noktaları Temizle” düğmesi: Tüm tıklamaları sıfırlar
            if st.button("Noktaları Temizle"):
                st.session_state.clicked_points = []
                st.session_state.selected_locations = {}

            # Folium haritasını ayarlayalım (Elâzığ merkezine yakın bir konum)
            center = (38.6744, 39.2220)
            m = folium.Map(location=center, zoom_start=13, tiles="OpenStreetMap")
            # Tıklanınca marker ekle
            folium.ClickForMarker(popup="Seçilen Nokta").add_to(m)

            # Haritayı göster, kullanıcı tıklaması varsa last_clicked kaydedilir
            map_data = st_folium(m, width=700, height=500)

            # Kullanıcı tıkladıysa, tıklanan koordinatı listeye ekle (eşsiz olacak şekilde)
            if map_data and map_data.get("last_clicked"):
                point = map_data["last_clicked"]
                coords = (point["lat"], point["lng"])
                if coords not in st.session_state.clicked_points:
                    st.session_state.clicked_points.append(coords)

            st.subheader("Seçilen Noktalar:")
            if not st.session_state.clicked_points:
                st.write("Henüz nokta seçilmedi.")
            else:
                # Seçilen noktaların listesini göster
                for idx, (lat, lon) in enumerate(st.session_state.clicked_points):
                    st.write(f"{idx+1}. ({lat:.4f}, {lon:.4f})")

            # En az 2 nokta seçildiyse, bunları sözlüğe dönüştür
            if len(st.session_state.clicked_points) >= 2:
                selected = {
                    f"Nokta {i+1}": coords
                    for i, coords in enumerate(st.session_state.clicked_points)
                }
                st.session_state.selected_locations = selected
            else:
                st.session_state.selected_locations = {}

        st.markdown("---")
        st.header("2. ACO Parametreleri")

        # Seçilmiş nokta sayısı yetersizse butonu devre dışı bırak
        if len(st.session_state.selected_locations) < 2:
            st.warning("En az 2 nokta seçmelisiniz.")
            st.button("Optimizasyonu Başlat", disabled=True)
            return

        # ACO algoritması için temel parametreler
        ant_count = st.number_input("Karınca Sayısı", min_value=2, max_value=100, value=20, step=1)
        iterations = st.number_input("Iterasyon Sayısı", min_value=10, max_value=1000, value=100, step=10)
        seed = st.number_input("Rastgele Tohum", min_value=0, max_value=999999, value=42, step=1)

        # Gelişmiş parametreler gizlenebilir bir bölümde
        with st.expander("Gelişmiş Ayarlar"):
            alpha = st.slider("Alpha (Feromon Etkisi)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
            beta = st.slider("Beta (Mesafe Etkisi)", min_value=0.1, max_value=5.0, value=3.0, step=0.1)
            rho = st.slider("Rho (Feromon Buharlaşma)", min_value=0.01, max_value=1.0, value=0.3, step=0.01)
            Q = st.number_input("Q (Feromon Sabiti)", min_value=1, max_value=500, value=100, step=1)

        st.markdown("---")
        run_button = st.button("Optimizasyonu Başlat")

    # ====== Hesaplama ve Sonuçları Gösterme Bölümü ====== #
    if run_button:
        selected = st.session_state.selected_locations
        loc_names = list(selected.keys())
        loc_coords = list(selected.values())

        try:
            # OSM grafiğini yükleyip proje edilmiş haliyle mesafe matrisi oluşturuyoruz
            with st.spinner("OSM verisi yükleniyor..."):
                graph = load_osm_graph()
            with st.spinner("Mesafe matrisi hesaplanıyor..."):
                dist_matrix = compute_distance_matrix(graph, loc_coords)
        except FileNotFoundError as e:
            st.error(f"Hata: {e}")
            st.stop()

        st.success("Mesafe matrisi başarıyla oluşturuldu.")
        st.info("ACO algoritması çalıştırılıyor...")

        # ACO algoritmasını çalıştır
        aco = ACO(
            distance_matrix=dist_matrix,
            ant_count=ant_count,
            alpha=alpha,
            beta=beta,
            rho=rho,
            Q=Q,
            seed=seed
        )
        best_route, best_distance, history = aco.run(iterations=iterations)

        st.session_state.results = {
            "loc_names": loc_names,
            "distance_matrix": dist_matrix,
            "best_route": best_route,
            "best_distance": best_distance,
            "history": history
        }

        st.success(f"Optimizasyon tamamlandı! En kısa mesafe: {best_distance:.2f} km")

    # Eğer sonuç varsa, üç sekmede göster
    if st.session_state.results is not None:
        data = st.session_state.results
        loc_names = data["loc_names"]
        dist_mat = data["distance_matrix"]
        best_route = data["best_route"]
        best_dist = data["best_distance"]
        history = data["history"]

        st.markdown("---")
        st.header("Sonuçlar")

        # Sekme 1: Harita
        tab1, tab2, tab3 = st.tabs(["Harita", "Konverjans Grafiği", "Detaylar"])
        with tab1:
            st.subheader("Optimum Rota Haritası")
            ordered_locs = {name: st.session_state.selected_locations[name] for name in loc_names}
            show_route_map(
                ordered_locs,
                best_route,
                map_width=1000,
                map_height=600
            )

        # Sekme 2: Konverjans Grafiği ve Mesafe Matrisi Isı Haritası
        with tab2:
            st.subheader("ACO Konverjans Grafiği")
            plot_convergence(history)
            with st.expander("Mesafe Matrisi Isı Haritası"):
                show_distance_matrix_heatmap(dist_mat, loc_names)

        # Sekme 3: Detay Tablosu
        with tab3:
            st.subheader("Rota Detayları")
            order = best_route[:-1]
            df = pd.DataFrame({
                "Sıra": list(range(1, len(order) + 1)),
                "Nokta": [loc_names[i] for i in order],
                "Enlem": [st.session_state.selected_locations[loc_names[i]][0] for i in order],
                "Boylam": [st.session_state.selected_locations[loc_names[i]][1] for i in order],
                "Bir Sonraki Noktaya Mesafe (km)": [
                    dist_mat[order[i], order[i + 1]] for i in range(len(order) - 1)
                ] + [dist_mat[order[-1], order[0]]]
            })
            # Mesafe sütununu biçimlendir
            df["Bir Sonraki Noktaya Mesafe (km)"] = df["Bir Sonraki Noktaya Mesafe (km)"].map(lambda x: f"{x:.2f}")
            st.dataframe(df, width=800)

            full_route = " → ".join([loc_names[i] for i in best_route])
            st.markdown(f"**Tam Rota:** {full_route}")
            st.markdown(f"**Toplam Mesafe:** **{best_dist:.2f} km**")

            # CSV indirme butonu
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Rotayı CSV Olarak İndir",
                data=csv_data,
                file_name="optimized_route.csv",
                mime="text/csv"
            )


if __name__ == "__main__":
    main()
