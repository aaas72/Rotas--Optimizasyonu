# Elâzığ Şehir İçi Teslimat Rotası Optimizasyonu (ACO Projesi)

Bu proje, **Elâzığ** ilinde birden fazla nokta arasındaki en kısa teslimat rotasını bulmak için **Karınca Kolonisi Optimizasyonu (Ant Colony Optimization, ACO)** algoritmasını kullanır. Aşağıda proje yapısı, kurulumu ve kullanım adımları, algoritmanın işleyişi ve sonuçların değerlendirilmesi ayrıntılı olarak açıklanmıştır.

---

## İçindekiler

1. [Proje Yapısı](#proje-yapısı)  
2. [Gereksinimler ve Kurulum](#gereksinimler-ve-kurulum)  
3. [Başlangıç Adımları](#başlangıç-adımları)  
   - 3.1 [Sanal Ortam Oluşturma (Opsiyonel)](#sanalo-ortam-oluşturma-opsiyonel)  
   - 3.2 [Gerekli Paketlerin Yüklenmesi](#gerekli-paketlerin-yüklenmesi)  
   - 3.3 [OSM GraphML Dosyasının Oluşturulması (Bir Kez)](#osm-graphml-dosyasının-oluşturulması-bir-kez)  
   - 3.4 [Uygulamanın Çalıştırılması](#uygulamanın-çalıştırılması)  
4. [Arayüz ve Kullanım](#arayüz-ve-kullanım)  
   - 4.1 [Nokta Seçim Yöntemi](#nokta-seçim-yöntemi)  
   - 4.2 [ACO Parametre Ayarları](#aco-parametre-ayarları)  
   - 4.3 [Sonuçların Görüntülenmesi](#sonuçların-görüntülenmesi)  
5. [ACO Algoritmasının İşleyişi](#aco-algoritmasının-işleyişi)  
6. [Mesafe Matrisi Hesaplama](#mesafe-matrisi-hesaplama)  
7. [Sonuçların Değerlendirilmesi](#sonuçların-değerlendirilmesi)  
8. [Gelecek Geliştirmeler](#gelecek-geliştirmeler)  

---

## Proje Yapısı

```
ACO_Project/
├── generate_graphml.py         # Elâzığ OSM yol ağını indirip src/data/elazig_osm.graphml dosyasına kaydeder
├── requirements.txt            # Proje için gerekli Python paketlerinin listesi
├── README.md                   # Bu dosya: Projenin genel tanıtımı ve kullanım kılavuzu
└── src/
    ├── aco/
    │   ├── __init__.py
    │   ├── algorithm.py        # Karınca Kolonisi Optimizasyonu algoritması
    │   └── utils.py            # Yardımcı fonksiyonlar (Örneğin Haversine mesafesi)
    │
    ├── data/
    │   ├── __init__.py
    │   ├── osm_data.py         # OSM GraphML dosyasını yükler ve mesafe matrisini oluşturur
    │   └── location_data.py    # Varsayılan nokta listesi (20+ nokta) veya CSV’den yükleme
    │
    ├── ui/
    │   ├── __init__.py
    │   ├── map_visualization.py    # Folium ile rota haritası gösterimi
    │   ├── plots.py                # Plotly ile konverjans grafiği ve ısı haritası
    │   └── app.py                  # Streamlit arayüzü: nokta seçimi, ACO çalıştırma, sonuç gösterimi
    │
    └── main.py                  # `python src/main.py` ile Streamlit uygulamasını başlatır
```

---

## Gereksinimler ve Kurulum

Proje, Python 3.8 veya üzeri sürümlerde çalışır. Aşağıdaki Python paketlerine ihtiyaç vardır:

- `streamlit`  
- `streamlit-folium`  
- `folium`  
- `plotly`  
- `pandas`  
- `numpy`  
- `osmnx`  
- `networkx`  
- `shapely`  

Tüm bağımlılıkları yüklemek için:

```bash
pip install -r requirements.txt
```

---

## Başlangıç Adımları

### 3.1 Sanal Ortam Oluşturma (Opsiyonel)

Projenin bağımlılıklarını izole etmek için bir sanal ortam (venv) oluşturabilirsiniz:

```bash
# Windows (CMD)
python -m venv .venv
.venv\Scripts\activate.bat

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3.2 Gerekli Paketlerin Yüklenmesi

```bash
pip install -r requirements.txt
```

### 3.3 OSM GraphML Dosyasının Oluşturulması (Bir Kez)

Elâzığ ilinin yol ağını OpenStreetMap’ten indirip yerel olarak kaydetmek için:

```bash
python generate_graphml.py
```

- Bu işlem birkaç dakika sürebilir.  
- Çıktı olarak `src/data/elazig_osm.graphml` dosyası oluşturulur.  
- "Başarıyla kaydedildi: elazig_osm.graphml" mesajını gördüğünüzde işlem tamamlanmıştır.

### 3.4 Uygulamanın Çalıştırılması

```bash
cd src
streamlit run ui/app.py
```

veya

```bash
python main.py
```

Tarayıcınızda otomatik olarak Streamlit arayüzü açılacaktır.

---

## Arayüz ve Kullanım

### 4.1 Nokta Seçim Yöntemi

1. **Varsayılan Liste**  
   - “Varsayılan Liste” seçeneğini işaretleyin.  
   - Aşağıya “Veri Kaynağı” başlığı altında “Varsayılan Noktalar” veya “CSV Yükle” seçenekleri çıkar.  
   - **Varsayılan Noktalar**:  
     - `location_data.py` içinde tanımlı 20’den fazla popüler nokta listesi görünür.  
     - “Nokta Ara” alanına yazı yazarak listeyi filtreleyin.  
     - Birden fazla noktayı seçmek için kutucuğu işaretleyin (en az 2 nokta).  
   - **CSV Yükle**:  
     - CSV dosyanızda “name, latitude, longitude” sütunları bulunmalıdır.  
     - Yükleme başarılı olduğunda yüklenen nokta adedi ekranda gösterilir.

2. **Haritadan Tıkla**  
   - “Haritadan Tıkla” seçeneğini işaretleyin.  
   - Ekranın yan panelinde Folium tabanlı bir harita açılır.  
   - Haritaya tıklayıp en az 2 nokta seçin. Her fare tıklaması yeni bir nokta ekler.  
   - Seçilen noktaların listesi haritanın altında “Seçilen Noktalar” başlığıyla gösterilir.  
   - İstediğiniz zaman “Noktaları Temizle” butonuna basarak seçtiğiniz tüm noktaları sıfırlayabilirsiniz.  
   - En az 2 nokta seçildiğinde “Optimizasyonu Başlat” butonu aktif hale gelir.

### 4.2 ACO Parametre Ayarları

- “Karınca Sayısı”: Her iterasyonda kaç karınca çalıştırılacağı (min 2, max 100; varsayılan 20).  
- “Iterasyon Sayısı”: Kaç tur çalıştırılacağı (min 10, max 1000; varsayılan 100).  
- “Rastgele Tohum”: RNG için opsiyonel seed değeri (min 0, max 999999; varsayılan 42).  

**Gelişmiş Ayarlar** altında:  
- “Alpha (Feromon Etkisi)” (0.1 – 5.0; varsayılan 1.0)  
- “Beta (Mesafe Etkisi)” (0.1 – 5.0; varsayılan 3.0)  
- “Rho (Feromon Buharlaşma Oranı)” (0.01 – 1.0; varsayılan 0.3)  
- “Q (Feromon Sabiti)” (1 – 500; varsayılan 100)

### 4.3 Sonuçların Görüntülenmesi

“Optimizasyonu Başlat” butonuna bastığınızda:  
1. **OSM GraphML yüklenir** (`load_osm_graph()`) ve **mesafe matrisi hesaplanır** (`compute_distance_matrix()`).  
2. **Karınca Kolonisi Optimizasyonu (ACO)** çalıştırılır ve en iyi rota ile mesafe bulunur.  
3. Üç farklı **sekme (Tab)** altında sonuçlar sunulur:

#### a) Harita

- Folium kullanılarak interaktif bir harita gösterilir.  
- **Rota çizgisi (PolyLine)**: Kırmızı renkle en iyi rota gösterilir.  
- **Markerlarda Numara ve Renk**: 
  - İlk nokta (Başlangıç) koyu yeşil.  
  - Geri kalan ziyaret noktaları mavi.  
  - Rotaya dahil edilmeyen noktalar (gri).  
- Harita üstünde yakınlaştırma/uzaklaştırma yapılabilir.

#### b) Konverjans Grafiği

- Plotly tabanlı bir çizgi grafiği:  
  - **best_distance** (en iyi mesafe)  
  - **average_distance** (ortalama mesafe)  
  - **worst_distance** (en kötü mesafe)  
- Her iterasyonda bu değerler güncellenir ve grafik üzerinde izlenir.  
- Altında açılabilir bölümde **Mesafe Matrisi Isı Haritası (Heatmap)** gösterilir.

#### c) Detaylar

- **DataFrame Tablosu**:  
  - “Sıra” (1,2,3,…)  
  - “Nokta” (isim veya “Nokta X”)  
  - “Enlem, Boylam” (koordinatlar)  
  - “Bir Sonraki Noktaya Mesafe (km)”  
- Tablo altında:  
  - **Tam Rota**: Nokta isimleri sırasıyla aralarında → olarak listelenir.  
  - **Toplam Mesafe**: En iyi rotanın toplam kilometresi.  
- **CSV İndir Butonu**: Tabloyu CSV olarak indirmenizi sağlar.

---

## ACO Algoritmasının İşleyişi

1. **Başlangıç:**  
   - Kullanıcı tarafından seçilen `n` nokta (en az 2).  
   - Mesafe matrisi `dist_matrix` oluşturulur: `n×n` boyutlu ve her çift (i,j) arasındaki yol mesafesi km cinsinden.  
   - `ant_count` kadar karınca, `iterations` kadar tur çalışacak.

2. **Pheromone Matrisinin Oluşturulması:**  
   - `pheromone = np.ones((n,n)) * 0.1` ile ilk değerler atanır.

3. **Her Iterasyonda:**  
   - **Her karınca**: 
     - Rastgele bir başlangıç noktası seçer (`start`).  
     - Geçerli rotayı inşa eder: her adımda `unvisited` (ziyaret edilmeyen) noktalar listesinden, `pheromone[current, next]^alpha * (1/dist[current, next])^beta` olasılığına göre bir sonraki noktayı seçer.  
     - Tüm noktalar ziyaret edildikten sonra başlangıç noktasına döner (`route.append(route[0])`).  
     - Rotanın toplam mesafesi hesaplanır (`sum(distances[path[i], path[i+1]] for i in ..)`).  
     - Eğer bu mesafe `best_length`’den küçükse, `best_length` ve `best_route` güncellenir.  
   - **Tur (Iteration) Sonunda:**  
     - **Feromon Buharlaşması:** `pheromone *= (1 - rho)`  
     - **Feromon Ekleme:** Her karıncanın rotasında kullanılan her kenara `delta = Q / length` kadar feromon eklenir (`pheromone[a,b] += delta`).  
   - **İstatistik:** O tur için en iyi, ortalama ve en kötü mesafe değerleri toplanıp `history` listesine eklenir.

4. **Sonuç:**  
   - `best_route` ve `best_length` döner.  
   - `history` listesi, iterasyon bazlı performansı gösterir.

---

## Mesafe Matrisi Hesaplama

1. **OSM GraphML Dosyası Yükleme** (`load_osm_graph`):  
   - `src/data/elazig_osm.graphml` dosyası `ox.load_graphml(...)` kullanılarak yüklenir.  
   - `ox.project_graph(graph)` ile **projeksiyon** uygulanır (UTM gibi bir CRS’e), bu sayede `ox.distance.nearest_nodes` hızlı çalışır.

2. **Noktaların Projeksiyonu:**  
   - Kullanıcının seçtiği her `(latitude, longitude)` koordinatı şunlarla işlenir:  
     ```python
     geom = Point(lon, lat)
     geom_proj = ox.projection.project_geometry(geom, to_crs=graph_proj.graph["crs"])[0]
     projected_points.append((geom_proj.x, geom_proj.y))
     ```

3. **En Yakın Node Bulma:**  
   - `for (x,y) in projected_points:`  
     ```python
     node = ox.distance.nearest_nodes(graph_proj, X=x, Y=y)
     nodes.append(node)
     ```

4. **Dijkstra ile Kısa Yol Hesaplama:**  
   - `nx.shortest_path_length(graph_proj, source=node_i, target=node_j, weight="length")`  
   - Sonucu metre cinsinden alır, km’ye çevrilir (`km = length_m / 1000`), `dist_matrix[i][j] = km` ve `dist_matrix[j][i] = km`.

5. **Diyagonal (i == i):**  
   - `dist_matrix[i][i] = 1e-10` (`0` olmadığı için **ACI** algoritmasında sorun çıkmaz).

---

## Sonuçların Değerlendirilmesi

1. **Gerçekçi Mesafeler:**  
   - Seçilen noktalar arasındaki mesafeler (0.3 – 6 km) Elâzığ şehir içi gerçeğine yakın.  
   - Örneğin “Forum AVM ↔ Otobüs Terminali” ≈ 0.31 km, “Üniversite ↔ Harput Kalesi” ≈ 6.08 km.  
   - Bu doğruluk, ACO algoritmasının mantıklı rotalar üretmesini sağlar.

2. **Matrisin Simetrik Olması:**  
   - `dist[i][j] == dist[j][i]` tutarlılığı korunmuş.  
   - Sadece `dist[i][i]` kendi kendine mesafe için 1e-10 olarak ayarlanmış.

3. **ACO Performansı ve Grafikler:**  
   - **Karınca Sayısı = 20**, **Iterasyon Sayısı = 100** için 5–15 saniye içinde sonuç alınır.  
   - “Konverjans Grafiği”nde ilk 10–20 iterasyonda hızlı düşüş, sonrasında denge hâline gelir.  
   - Ortalama (average) ve en kötü (worst) mesafeler, algoritmanın ne kadar çeşitli yollar denediğini gösterir.

4. **Uygulama Alanları:**  
   - **Teslimat Lojistiği**: Elâzığ içindeki şirketler, restoranlar, kuryeler bu aracı kullanarak en kısa güzergâhı belirleyebilir.  
   - **Saha Çalışmaları**: Teknik ekiplerin saha ziyaret sırasını optimize etmesi.  
   - **Turistik Rotalar**: Ziyaretçilerin önemli noktaları en verimli şekilde ziyaret edebilmesi.

---

## Gelecek Geliştirmeler

1. **Zaman Pencereli Rotalama (Time Windows)**  
   - Noktaların sadece belirli saatlerde ziyaret edilebildiği senaryolar.  
   - Bu, aracı **Vehicle Routing Problem with Time Windows (VRPTW)** çözücülere ihtiyaç duyacak doğrultuda genişletir.

2. **Trafik Verileri ve Süre Temelli Hesaplama**  
   - Google Maps API veya OpenRouteService ile gerçek zamanlı trafik verisi entegre edilerek, **mesafe yerine süre (duration)** üzerinden optimizasyon yapılabilir.

3. **Harita Üzerinde Nokta Silme ve Yeniden Konumlandırma**  
   - Mevcut “Haritadan Tıkla” yöntemini geliştirerek, harita üzerinde seçilen noktaları sürükleme (drag & drop) veya silmeye (remove) imkân veren fonksiyonlar eklenebilir.

4. **Paralel İşleme (Parallelization)**  
   - ACO algoritmasında “karıncaların rotaları oluşturma” ve “feromon güncelleme” adımları **çok çekirdekli (multi-core)** olarak çalıştırılıp hız kazanılabilir.

5. **Bölge Seçimi (Bounding Box)**  
   - Kullanıcıya haritada bir dikdörtgen çizme (kutu seçme) imkânı verilip, sadece o bölgede rastgele/otomatik nokta oluşturulabilir veya mevcut nokta listesi o bölgede filtrelenebilir.

---

## Özet

Bu proje, Elâzığ içindeki çeşitli nokta kümelerini (alışveriş merkezleri, hastaneler, üniversite, tarihi mekanlar vb.) kullanarak:

1. **OSM’den yerel GraphML** (Elâzığ yolları) dosyası oluşturur.  
2. **Mesafe Matrisi** hesaplar (Dijkstra + OSM).  
3. **Ant Colony Optimization** (Karınca Kolonisi) algoritmasını çalıştırarak en iyi rotayı bulur.  
4. **Streamlit Arayüzü** sunarak:
   - Nokta seçimi (liste veya harita)  
   - ACO parametre ayarı  
   - Harita, konverjans grafiği ve detay tablosu gösterimi  
   - CSV formatında sonuç indirme  

Sonuçlar, gerçekçi mesafelere dayanmakta ve ACO’nun hızlıca anlamlı rotalar üretmesine imkân tanımaktadır. Gelecekte ek özelliklerle (zaman penceresi, gerçek zamanlı trafik, paralel işlem vb.) daha kapsamlı lojistik çözümler sunmak mümkündür.
#
