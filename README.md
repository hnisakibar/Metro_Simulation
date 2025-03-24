# Metro_Simulation

Bu kod, İstanbul'daki metro sisteminin bir simülasyonunu oluşturan bir Python programıdır.

**Kodun Amacı**
Kod, İstanbul'un metro ağını modelleyerek istasyonlar ve hatlar arasındaki bağlantıları oluşturur. Kullanıcıya:
- En az aktarma yapan rotayı bulma (BFS - Breadth-First Search),
- En hızlı rotayı bulma (A* benzeri algoritma) imkanlarını sunar.


**Kodun Bileşenleri**
1. `Istasyon` Sınıfı
Her metro istasyonunu temsil eder.  
Özellikleri:
- `idx` → İstasyonun benzersiz kimliği
- `ad` → İstasyonun adı
- `hat` → Bağlı olduğu metro hattı
- `komsular` → Komşu istasyonlar ve aralarındaki süre bilgisi

Yöntemleri:
- `komsu_ekle(istasyon, sure)` → Komşu bir istasyon ekler.


2. `MetroAgi` Sınıfı
Tüm metro sistemini temsil eder.  
Özellikleri:
- `istasyonlar` → Tüm istasyonları içeren bir sözlük
- `hatlar` → Her hattaki istasyonları saklayan bir sözlük

Yöntemleri:
- `istasyon_ekle(idx, ad, hat)` → Yeni bir istasyon ekler.
- `baglanti_ekle(istasyon1_id, istasyon2_id, sure)` → İki istasyon arasında bağlantı ekler.
- `en_az_aktarma_bul(baslangic_id, hedef_id)` → BFS kullanarak en az aktarmalı rotayı bulur.
- `en_hizli_rota_bul(baslangic_id, hedef_id)` → A* benzeri bir algoritma ile en hızlı rotayı hesaplar.


3. Metro Hatlarının Tanımlanması
Kod, İstanbul’daki metro hatlarını manuel olarak oluşturur.  
Örneğin:

stations_M1 = ["Yenikapı", "Aksaray", "Emniyet-Fatih", "Topkapı-Ulubatlı", ...]
for idx, station in enumerate(stations_M1, start=1):
    metro.istasyon_ekle(f"M1A{idx}", station, "M1")Her hat için istasyonlar eklenir ve bağlantılar belirlenir.

Bağlantı süreleri şu kurala göre belirlenmiştir: connection_time = 2 if i % 2 == 0 else 3
Bu, bazı istasyonlar arasında 2, diğerleri arasında 3 dakika süre olduğunu gösterir.


4. Rota Bulma Algoritmaları
En Az Aktarma Yapan Rota (`BFS`)
- BFS (Genişlik Öncelikli Arama) algoritmasını kullanır.
- İlk bulunan rota en az aktarma yapan rota olduğu için verimli bir yöntemdir.

Örnek:  `metro.en_az_aktarma_bul("M1A1", "M2A5")`
- "Yenikapı"dan "Taksim"e en az aktarma ile nasıl gidileceğini bulur.


En Hızlı Rota (`A* Benzetimli Algoritma`)
- Dijkstra algoritmasına benzer bir yol kullanır.
- heapq (öncelikli kuyruk) kullanarak en kısa sürede ulaşılacak istasyonu seçer.
- Öncelikli olarak en kısa sürede ulaşılabilecek istasyonlar ziyaret edilir.

Örnek:  `metro.en_hizli_rota_bul("M1A1", "M2A5")`
- "Yenikapı"dan "Taksim"e en kısa sürede nasıl gidileceğini bulur.


Geliştirilebilecek Noktalar

- Aktarma arası geçiş süreleri ve duraklar arası geçiş süreleri daha gerçekçi şekilde ele alınabilir.
- İstenen durak kodlarını kullanıcı  görüntüleyebilir.
- Kullanıcıdan durakların kodları değil, direkt olarak durak isimleri alınarak kullanıcıya kolaylık oluşturulabilir.
- İstanbulda bulunan YHT ya da Deniz Hatları da eklenerek daha gerçekçi bir ulaşım hattı oluşturulabilir.
- Ulaşım boyunca toplam ulaşım ücreti hesaplanarak uygulamanın amacı genişletilebilir.
- Eklenmiş olan PDF linki farklı yöntemlerle direkt olarak kullanıcıya yansıtılabilir. 

**SONUÇ**
Bu kod, İstanbul metro sisteminin temel bir modelini oluşturur.  
Gerçek zamanlı yolculuk planlaması ve dinamik süreler için geliştirilebilir.
