from collections import defaultdict, deque
import heapq
from typing import Dict, List, Tuple, Optional

class Istasyon:
    """Bir metro istasyonunu temsil eden sınıf."""
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        """İstasyona komşu bir istasyon ekler."""
        self.komsular.append((istasyon, sure))

class MetroAgi:
    """Metro ağını temsil eden sınıf."""
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        """Yeni bir istasyon ekler."""
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        """İki istasyon arasında bağlantı ekler."""
        if istasyon1_id in self.istasyonlar and istasyon2_id in self.istasyonlar:
            istasyon1 = self.istasyonlar[istasyon1_id]
            istasyon2 = self.istasyonlar[istasyon2_id]
            istasyon1.komsu_ekle(istasyon2, sure)
            istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[str]]:
        """BFS algoritması ile en az aktarmalı rotayı bulur."""
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        
        kuyruk = deque([(self.istasyonlar[baslangic_id], [baslangic_id])])
        ziyaret_edildi = set()
        
        while kuyruk:
            mevcut, yol = kuyruk.popleft()
            
            if mevcut.idx == hedef_id:
                return yol
            
            ziyaret_edildi.add(mevcut.idx)
            
            for komsu, _ in mevcut.komsular:
                if komsu.idx not in ziyaret_edildi:
                    kuyruk.append((komsu, yol + [komsu.idx]))
        
        return None
    
    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[str], int]]:
        """A* algoritması ile en hızlı rotayı bulur."""
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        
        pq = [(0, id(self.istasyonlar[baslangic_id]), self.istasyonlar[baslangic_id], [baslangic_id])]
        ziyaret_edildi = {}
        
        while pq:
            toplam_sure, _, mevcut, yol = heapq.heappop(pq)
            
            if mevcut.idx == hedef_id:
                return yol, toplam_sure
            
            if mevcut.idx in ziyaret_edildi and ziyaret_edildi[mevcut.idx] <= toplam_sure:
                continue
            
            ziyaret_edildi[mevcut.idx] = toplam_sure
            
            for komsu, sure in mevcut.komsular:
                heapq.heappush(pq, (toplam_sure + sure, id(komsu), komsu, yol + [komsu.idx]))
        
        return None

if __name__ == "__main__":
    metro = MetroAgi()

    # İstanbul Metro Hatları

    # M1 Hattı Durakları
    stations_M1 = [
        "Yenikapı", "Aksaray", "Emniyet-Fatih", "Topkapı-Ulubatlı", "Bayrampaşa-Maltepe", "Sağmalcılar",
        "Kocatepe", "Otogar", "Terazidere", "Davutpaşa–YTÜ", "Merter", "Zeytinburnu", "Bakırköy-İncirli", 
        "Bahçelievler", "Ataköy-Şirinevler", "Yenibosna", "DTM–İstanbul", "Atatürk Havalimanı", 
        "Esenler", "Menderes", "Üçyüzlü", "Bağcılar Meydan", "Kirazlı"
    ]

    # Durakları ekleme
    for idx, station in enumerate(stations_M1, start=1):
        metro.istasyon_ekle(f"M1A{idx}", station, "M1")

    # Bağlantıları ekleme
    for i in range(len(stations_M1) - 1):
        connection_time = 2 if i % 2 == 0 else 3
        metro.baglanti_ekle(f"M1A{i+1}", f"M1A{i+2}", connection_time)

    # M2 Hattı Durakları
    stations_M2 = [
        "Yenikapı", "Vezneciler-İstanbul Ü.", "Haliç", "Şişhane", "Taksim", "Osmanbey", 
        "Şişli-Mecidiyeköy", "Gayrettepe", "Levent", "4.Levent", "Sanayi Mahalles", "Seyrantepe", 
        "İTÜ-Ayazağa", "Atatürk Oto Sanayi", "Darüşşafaka", "Hacıosman"
    ]

    for idx, station in enumerate(stations_M2, start=1):
        metro.istasyon_ekle(f"M2A{idx}", station, "M2")

    for i in range(len(stations_M2) - 1):
        connection_time = 2 if i % 2 == 0 else 3
        metro.baglanti_ekle(f"M2A{i+1}", f"M2A{i+2}", connection_time)

    # M3 Hattı Durakları
    stations_M3 = [
        "Bakırköy Sahil", "Özgürlük Meydanı", "İncirli", "Haznedar", "İlkyuva", "Molla Gürani", 
        "Kirazlı-Bağcılar", "Yenimahalle", "Mahmutbey", "İSTOÇ", "İkitelli Sanayi", "Turgut Özal", 
        "Siteler", "Başak Konutları", "Başakşehir-Metrokent", "Onurkent", "Şehir Hastanesi", 
        "Toplu Konutlar", "Kayaşehir Merkez"
    ]

    for idx, station in enumerate(stations_M3, start=1):
        metro.istasyon_ekle(f"M3A{idx}", station, "M3")

    for i in range(len(stations_M3) - 1):
        connection_time = 2 if i % 2 == 0 else 3
        metro.baglanti_ekle(f"M3A{i+1}", f"M3A{i+2}", connection_time)


    # M4 Hattı Durakları
    stations_M4 = [
        "Kadıköy", "Ayrılık Çeşmesi", "Acıbadem", "Ünalan", "Göztepe", "Yenisahra", 
        "Pegasus-Kozyatağı", "Bostancı", "Küçükyalı", "Maltepe", "Huzurevi", "Gülsuyu", 
        "Esenkent", "Hastane-Adliye", "Soğanlık", "Kartal", "Yakacık-Adnan Kahveci", 
        "Pendik", "Tavşantepe", "Fevzi Çakmak-Hastane", "Yayalar-Şeyhli", "Kurtköy", 
        "Sabiha Gökçen Havalimanı"
    ]

    for idx, station in enumerate(stations_M4, start=1):
        metro.istasyon_ekle(f"M4A{idx}", station, "M4")

    for i in range(len(stations_M4) - 1):
        metro.baglanti_ekle(f"M4A{i+1}", f"M4A{i+2}", 2 if i % 2 == 0 else 3)

    # M5 Hattı Durakları
    stations_M5 = [
        "Üsküdar", "Fıstıkağacı", "Bağlarbaşı", "Altunizade", "Kısıklı", "Bulgurlu", 
        "Ümraniye", "Çarşı", "Yamanevler", "Çakmak", "Ihlamurkuyu", "Altınşehir", 
        "İmam Hatip Lisesi", "Dudullu", "Necip Fazıl", "Çekmeköy", "Meclis", "Sarıgazi", 
        "Sancaktepe", "Samandıra Merkez"
    ]

    for idx, station in enumerate(stations_M5, start=1):
        metro.istasyon_ekle(f"M5A{idx}", station, "M5")

    for i in range(len(stations_M5) - 1):
        connection_time = 2 if i % 2 == 0 else 3  # Alternating connection time (for example)
        metro.baglanti_ekle(f"M5A{i+1}", f"M5A{i+2}", connection_time)


    # M6 Hattı Durakları
    metro.istasyon_ekle("M6A1", "Levent", "M6")
    metro.istasyon_ekle("M6A2", "Nispetiye", "M6")
    metro.istasyon_ekle("M6A3", "Etiler", "M6")
    metro.istasyon_ekle("M6A4", "Boğaziçi Ü.-Hisarüstü", "M6")

    metro.baglanti_ekle("M6A1", "M6A2", 2)   # Levent -> Nispetiye
    metro.baglanti_ekle("M6A2", "M6A3", 3)   # Nispetiye -> Etiler
    metro.baglanti_ekle("M6A3", "M6A4", 2)   # Etiler -> Boğaziçi Ü.-Hisarüstü


    # M7 Hattı Durakları
    stations_M7 = [
        "Yıldız", "Fulya", "Mecidiyeköy", "Çağlayan", "Kağıthane", "Nurtepe", 
        "Alibeyköy", "Çırçır Mahallesi", "Veysel Karani-Akşemsettin", "Yeşilpınar", 
        "Kazım Karabekir", "Yenimahalle", "Karadeniz Mahallesi", "Tekstilkent-Giyimkent", 
        "Oruç Reis", "Göztepe Mahallesi", "Mahmutbey"
    ]

    for idx, station in enumerate(stations_M7, start=1):
        metro.istasyon_ekle(f"M7A{idx}", station, "M7")

    for i in range(len(stations_M7) - 1):
        metro.baglanti_ekle(f"M7A{i+1}", f"M7A{i+2}", 2 if i % 2 == 0 else 3)


    # M8 Hattı Durakları
    stations_M8 = [
        "Bostancı", "Emin Ali Paşa", "Ayşekadın", "Kozyatağı", "Küçükbakkalköy", "İçerenköy",
        "Kayışdağı", "Mevlana", "İMES", "MODOKO-KEYAP", "Dudullu", "Huzur", "Parseller"
    ]

    for idx, station in enumerate(stations_M8, start=1):
        metro.istasyon_ekle(f"M8A{idx}", station, "M8")

    for i in range(len(stations_M8) - 1):
        metro.baglanti_ekle(f"M8A{i+1}", f"M8A{i+2}", 2 if i % 2 == 0 else 3)


    # M9 Hattı Durakları
    stations_M9 = [
        "Ataköy", "Yenibosna", "Çobançeşme", "29 Ekim Cumhuriyet", "Doğu Sanayi", "Mimar Sinan",
        "15 Temmuz", "Halkalı Caddesi", "Atatürk Mahallesi", "Bahariye", "MASKO", "İkitelli Sanayi",
        "Ziya Gökalp Mahallesi", "Olimpiyat"
    ]

    for idx, station in enumerate(stations_M9, start=1):
        metro.istasyon_ekle(f"M9A{idx}", station, "M9")

    for i in range(len(stations_M9) - 1):
        metro.baglanti_ekle(f"M9A{i+1}", f"M9A{i+2}", 2 if i % 2 == 0 else 3)


    # T1 Hattı
    stations_T1 = [
        "Kabataş", "Fındıklı-Mimar Sinan Ü.", "Tophane", "Karaköy", "Eminönü", "Sirkeci", 
        "Gülhane", "Sultanahmet", "Çemberlitaş", "Beyazıt-Kapalıçarşı", "Laleli-İstanbul Ü.", 
        "Aksaray", "Yusufpaşa", "Haseki", "Fındıkzade", "Çapa-Şehremini", "Pazartekke", 
        "Topkapı", "Cevizlibağ-AÖY", "Merkezefendi", "Seyitnizam-Akşemsettin", "Mithatpaşa", 
        "Zeytinburnu", "Mehmet Akif", "Merter Tekstil Merkezi", "Güngören", "Akıncılar", 
        "Soğanlı", "Yavuzselim", "Güneştepe", "Bağcılar"
    ]

    for idx, station in enumerate(stations_T1, start=1):
        metro.istasyon_ekle(f"T1A{idx}", station, "T1")

    for i in range(len(stations_T1) - 1):
        metro.baglanti_ekle(f"T1A{i+1}", f"T1A{i+2}", 2 if i % 2 == 0 else 3)


    # T3 Hattı
    stations_T3 = [
        "Kadıköy İDO", "Damga Sokak", "Mühürdar", "Rızapaşa", "Moda Caddesi", 
        "Moda İlkokulu", "Kilise", "Bahariye", "Altıyol", "Çarşı", "İskele Cami"
    ]

    for idx, station in enumerate(stations_T3, start=1):
        metro.istasyon_ekle(f"T3A{idx}", station, "T3")

    for i in range(len(stations_T3) - 1):
        metro.baglanti_ekle(f"T3A{i+1}", f"T3A{i+2}", 2 if i % 2 == 0 else 3)


    # T4 Hattı
    stations_T4 = [
        "Topkapı", "Fetihkapı", "Vatan", "Edirnekapı", "Şehitlik", "Demirkapı", 
        "Topçular", "Rami", "Uluyol Bereç", "Sağmalcılar", "Bosna Çukurçeşme", 
        "Ali Fuat Başgil", "Taşköprü", "Karadeniz", "Kiptaş-Venezia", "Cumhuriyet Mahallesi", 
        "50.Yıl-Baştabya", "Hacı Şükrü", "Yenimahalle", "Sultançiftliği", "Cebeci", "Mescid-i Selam"
    ]

    for idx, station in enumerate(stations_T4, start=1):
        metro.istasyon_ekle(f"T4A{idx}", station, "T4")

    for i in range(len(stations_T4) - 1):
        metro.baglanti_ekle(f"T4A{i+1}", f"T4A{i+2}", 2 if i % 2 == 0 else 3)


    # T5 Hattı
    stations_T5 = [
        "Eminönü", "Küçükpazar", "Cibali", "Fener", "Balat", "Ayvansaray", "Feshane",
        "Eyüpsultan Teleferik", "Eyüpsultan Devlet Hastanesi", "Silahtarağa Mahallesi", 
        "Üniversite", "Alibeyköy Merkez", "Alibeyköy Metro", "Alibeyköy Cep Otogarı"
    ]

    for idx, station in enumerate(stations_T5, start=1):
        metro.istasyon_ekle(f"T5A{idx}", station, "T5")

    for i in range(len(stations_T5) - 1):
        metro.baglanti_ekle(f"T5A{i+1}", f"T5A{i+2}", 2 if i % 2 == 0 else 3)


    # F1
    metro.istasyon_ekle("F1A1", "Taksim", "F1")
    metro.istasyon_ekle("F1A2", "Kabataş", "F1")
    metro.baglanti_ekle("F1A1", "F1A2", 2)   # Taksim -> Kabataş

    # TF2
    metro.istasyon_ekle("TF2A1", "Eyüp", "TF2")
    metro.istasyon_ekle("TF2A2", "Piyer Loti", "TF2")
    metro.baglanti_ekle("TF2A1", "TF2A2", 3)   # Eyüp -> Piyer Loti

    # TF1
    metro.istasyon_ekle("TF1A1", "Maçka", "TF1")
    metro.istasyon_ekle("TF1A2", "Taşkışla", "TF1")
    metro.baglanti_ekle("TF1A1", "TF1A2", 3)   # Maçka -> Taşkışla

    # F4
    metro.istasyon_ekle("F4A1", "Boğaziçi Ü.-Hisarüstü", "F4")
    metro.istasyon_ekle("F4A2", "Aşiyan", "F4")
    metro.baglanti_ekle("F4A1", "F4A2", 4)   # Hisarüstü -> Aşiyan


    # Marmaray - B1
    stations_Marmaray = [
    "Halkalı", "Mustafa Kemal", "Küçükçekmece", "Florya", "Florya Akvaryum", "Yeşilköy", 
    "Yeşilyurt", "Ataköy", "Bakırköy", "Yenimahalle", "Zeytinburnu", "Kazlıçeşme", "Yenikapı", 
    "Sirkeci", "Üsküdar", "Ayrılık Çeşmesi", "Söğütlüçeşme", "Feneryolu", "Göztepe", 
    "Erenköy", "Suadiye", "Bostancı", "Küçükyalı", "İdealtepe", "Süreyya Plajı", "Maltepe", 
    "Cevizli", "Atalar", "Başak", "Kartal", "Yunus", "Pendik", "Kaynarca", "Tersane", "Güzelyalı", 
    "Aydıntepe", "İçmeler", "Tuzla", "Çayırova", "Fatih", "Osmangazi", "Darıca", "Gebze"
    ]

    for idx, station in enumerate(stations_Marmaray, start=1):
        metro.istasyon_ekle(f"B1A{idx}", station, "B1")

    for i in range(len(stations_Marmaray) - 1):
        metro.baglanti_ekle(f"B1A{i+1}", f"B1A{i+2}", 2)


    # Aktarma noktaları
    metro.baglanti_ekle("M1A1", "B1A13", 2)  # Yenikapı (M1 - MR)
    metro.baglanti_ekle("M2A1", "B1A13", 2)  # Yenikapı (M2 - MR)
    metro.baglanti_ekle("M1A1", "M2A1", 2)  # Yenikapı (M1 - M2)
    metro.baglanti_ekle("M1A2", "T1A12", 2)  # Aksaray (M1 - T1)
    metro.baglanti_ekle("M1A4", "T4A1", 4)  # Topkapı-Ulubatlı (M1) -> Topkapı (T4)
    metro.baglanti_ekle("M1A22", "T1A1", 6)  # Bağcılar Meydan (M1) -> Bağcılar (T1)
    metro.baglanti_ekle("M1A23", "M3A1", 1)  # Kirazlı (M1 - M3)
    metro.baglanti_ekle("M1A12", "T1A23", 1)  # Zeytinburnu (M1 - T1)
    metro.baglanti_ekle("M2A5", "F1A1", 1)  # Taksim (M2 - F1)
    metro.baglanti_ekle("M2A7", "M7A3", 1)  # Şişli-Mecidiyeköy (M2 - M7)
    metro.baglanti_ekle("M2A9", "M6A1", 1)  # Levent (M2 - M6)
    metro.baglanti_ekle("M3A9", "M7A17", 1)  # Mahmutbey (M3 - M7)
    metro.baglanti_ekle("M1A13", "M3A3", 1)  # Bakırköy-İncirli (M1) -> İncirli (M3)
    metro.baglanti_ekle("M3A2", "B1A9", 1)  # Özgürlük Meydanı (M3) -> Bakırköy (MR)
    metro.baglanti_ekle("M4A2", "B1A16", 1)  # Ayrılık Çeşmesi (M4 - MR)
    metro.baglanti_ekle("M4A1", "T3A1", 1)  # Kadıköy (M4 - T3)
    metro.baglanti_ekle("M5A1", "B1A15", 1)  # Üsküdar (M5 - MR)
    metro.baglanti_ekle("M5A14", "M8A11", 1)  # Dudullu (M5 - M8)
    metro.baglanti_ekle("M6A4", "F4A1", 1)  # Boğaziçi Ü.-Hisarüstü (M6 - F4)
    metro.baglanti_ekle("M7A7", "T5A13", 1)  # Alibeyköy (M7 - T5)
    metro.baglanti_ekle("M7A13", "T4A14", 1)  # Karadeniz Mahallesi (M7 - T4)
    metro.baglanti_ekle("M4A7", "M8A4", 1)  # Kozyatağı (M4 - M8)
    metro.baglanti_ekle("M9A12", "M3A11", 1)  # İkitelli Sanayi (M9 - M3)
    metro.baglanti_ekle("M1A16", "M9A2", 1)  # Yenibosna (M1 - M9)
    metro.baglanti_ekle("M9A1", "B1A8", 1)  # Ataköy (M9 - MR)

# Test Senaryoları
print("\nİstanbul Raylı Sistemler Haritasına buradan ulaşabilirsiniz:\nhttps://www.metro.istanbul/Content/assets/uploaded/%C4%B0stanbul%20Rayl%C4%B1%20Sistemler%20Haritas%C4%B1.pdf")

# Kullanıcıdan başlangıç ve varış istasyonlarını al
baslangic = input("Başlangıç istasyonunu girin: ")
varis = input("Varış istasyonunu girin: ")

# En az aktarmalı rota
rota = metro.en_az_aktarma_bul(baslangic, varis)
if rota:
    print("En az aktarmalı rota:", " -> ".join(rota))
else:
    print("Rota bulunamadı.")

# En hızlı rota
sonuc = metro.en_hizli_rota_bul(baslangic, varis)
if sonuc:
    rota, sure = sonuc
    print(f"En hızlı rota ({sure} dakika):", " -> ".join(rota))
else:
    print("Rota bulunamadı.")
