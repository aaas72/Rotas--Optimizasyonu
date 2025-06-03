# -*- coding: utf-8 -*-
"""
src/ui/plots.py

Plotly kullanarak ACO algoritmasının konverjans grafiğini
ve mesafe matrisinin ısı haritasını çizer.
"""

import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

def plot_convergence(history: list):
    """
    ACO algoritmasının her iterasyondaki en iyi, ortalama ve en kötü mesafe değerlerini çizer.
    Args:
      - history: [
          {"iteration": 1, "best_distance": x, "average_distance": y, "worst_distance": z}, ...
        ]
    """
    df = pd.DataFrame(history)
    fig = px.line(
        df,
        x="iteration",
        y=["best_distance", "average_distance", "worst_distance"],
        labels={"value": "Mesafe (km)", "variable": "Metrik"},
        title="ACO Konverjans Grafiği"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_distance_matrix_heatmap(dist_matrix: np.ndarray, location_names: list):
    """
    Mesafe matrisini ısısal harita (heatmap) olarak çizer.
    Args:
      - dist_matrix: (n x n) mesafe matrisi (numpy array).
      - location_names: [ "Yer1", "Yer2", ... ] listesi.
    """
    import plotly.figure_factory as ff

    fig = ff.create_annotated_heatmap(
        z=dist_matrix.round(2).tolist(),
        x=location_names,
        y=location_names,
        colorscale="Viridis",
        showscale=True
    )
    fig.update_layout(
        title="Mesafe Matrisi Isı Haritası (km)",
        width=700,
        height=700
    )
    st.plotly_chart(fig, use_container_width=False)
