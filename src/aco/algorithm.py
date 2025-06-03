# -*- coding: utf-8 -*-
"""
src/aco/algorithm.py

Ant Colony Optimization (ACO) algoritmasını
Travelling Salesman Problem (TSP) benzeri problemler için uygular.
"""

import numpy as np
import random
from typing import List, Tuple, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ACO:
    """
    ACO sınıfı:
    - Mesafe matrisi (n x n) alır.
    - Her iterasyonda belirli sayıda karınca ile en kısa turu bulmaya çalışır.
    """

    def __init__(
        self,
        distance_matrix: np.ndarray,
        ant_count: int = 10,
        alpha: float = 1.0,
        beta: float = 3.0,
        rho: float = 0.3,
        Q: float = 100,
        seed: Optional[int] = None
    ):
        """
        Args:
          - distance_matrix: (n x n) boyutlu mesafe matrisi (kilometre cinsinden).
          - ant_count: Her iterasyonda kaç karınca kullanılacağı.
          - alpha: Feromon etkisi katsayısı.
          - beta: Mesafe (heuristic) etkisi katsayısı.
          - rho: Feromon buharlaşma oranı (0 < rho < 1).
          - Q: Feromon ekleme sabiti (Q / yol uzunluğu).
          - seed: Rastgele sayı üreteci için tohum (isteğe bağlı).
        """
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        # Mesafe matrisini kopya al ve diyagonali küçük bir değere ayarla (sıfır olmasın)
        self.distances = distance_matrix.copy()
        np.fill_diagonal(self.distances, 1e-10)

        self.num_nodes = self.distances.shape[0]  # Şehir veya nokta sayısı
        self.ant_count = ant_count
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q

        # Başlangıç feromon matrisi: tüm kenarlar için 0.1 (örnek değer)
        self.pheromone = np.ones((self.num_nodes, self.num_nodes)) * 0.1

    def _select_next_node(self, current: int, visited: List[int]) -> Optional[int]:
        """
        Mevcut düğümden (şehirden) sonraki düğümü
        feromon ve mesafe ağırlıklı olasılıkla seçer.
        Args:
          - current: Bulunulan düğüm (indeks).
          - visited: Şu ana kadar ziyaret edilen düğümler listesi.
        Returns:
          - Seçilen bir sonraki düğüm indeksi veya None (ziyaret edilecek kalmadıysa).
        """
        unvisited = [i for i in range(self.num_nodes) if i not in visited]
        if not unvisited:
            return None

        # Feromon ** alpha ve (1 / mesafe) ** beta hesapları
        pher_vals = self.pheromone[current, unvisited] ** self.alpha
        heur_vals = (1.0 / self.distances[current, unvisited]) ** self.beta
        probs = pher_vals * heur_vals
        total = probs.sum()
        if total <= 0:
            # Tüm olasılıklar sıfırsa rastgele bir düğüm seç
            return random.choice(unvisited)

        probs = probs / total
        return np.random.choice(unvisited, p=probs)

    def _update_pheromones(self, all_routes: List[List[int]], all_lengths: List[float]) -> None:
        """
        Tüm karıncaların yollarına göre feromonları günceller:
          1. Buharlaşma: pheromone *= (1 - rho)
          2. Her rota için Q / yol_uzunluğu kadar feromon ekle
        """
        # 1) Feromon buharlaşması
        self.pheromone *= (1 - self.rho)

        # 2) Yeni feromon ekleme
        for route, length in zip(all_routes, all_lengths):
            delta = self.Q / length
            for i in range(len(route) - 1):
                a, b = route[i], route[i + 1]
                self.pheromone[a, b] += delta
                self.pheromone[b, a] += delta

    def run(self, iterations: int = 100) -> Tuple[List[int], float, List[Dict]]:
        """
        ACO algoritmasını belirtilen iterasyon sayısı kadar çalıştırır.
        Args:
          - iterations: Toplam iterasyon (tur) sayısı.
        Returns:
          - best_route: En iyi rota (şehir/nokta indeksleri, başlangıca dönüş dahil).
          - best_length: En iyi rotanın toplam mesafesi (kilometre).
          - history: Her iterasyondaki istatistikler listesi (dict içinde
                     iteration, best_distance, average_distance, worst_distance).
        """
        best_route: List[int] = []
        best_length: float = float("inf")
        history: List[Dict] = []

        for it in range(1, iterations + 1):
            all_routes: List[List[int]] = []
            all_lengths: List[float] = []

            # Her karınca için bir rota oluştur
            for _ in range(self.ant_count):
                start = random.randint(0, self.num_nodes - 1)
                route = [start]

                # Tüm düğümleri ziyaret et (sonra start’a dönüş)
                while len(route) < self.num_nodes:
                    nxt = self._select_next_node(route[-1], route)
                    if nxt is None:
                        break
                    route.append(nxt)
                route.append(route[0])  # Başlangıca geri dönüş

                # Toplam mesafeyi hesapla
                length = sum(
                    self.distances[route[i], route[i + 1]]
                    for i in range(len(route) - 1)
                )
                all_routes.append(route)
                all_lengths.append(length)

                # En iyi çözümü güncelle
                if length < best_length:
                    best_length = length
                    best_route = route.copy()

            # Her iterasyonda feromonları güncelle
            self._update_pheromones(all_routes, all_lengths)

            avg_length = float(np.mean(all_lengths))
            worst_length = float(np.max(all_lengths))
            history.append({
                "iteration": it,
                "best_distance": best_length,
                "average_distance": avg_length,
                "worst_distance": worst_length
            })

            logger.info(
                f"[Iterasyon {it}/{iterations}] "
                f"En İyi={best_length:.2f} km, "
                f"Ortalama={avg_length:.2f} km, "
                f"En Kötü={worst_length:.2f} km"
            )

        return best_route, best_length, history
