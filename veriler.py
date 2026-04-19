import sqlite3
import os

DB_NAME = 'saglik_asistani.db'

def birlesik_veritabanini_kur():
    # Eğer eski veritabanı varsa, çakışma olmaması için siliyoruz (Temiz kurulum)
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"🗑️ Eski {DB_NAME} silindi, temiz kurulum başlatılıyor...")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. TEMEL BİLGİ TABLOSU
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bilgi_tabani (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            belirti TEXT,
            neden TEXT,
            oneri TEXT,
            kategori TEXT
        )
    ''')

    # 2. GERİ BİLDİRİM (LOG) TABLOSU (Uygulamanın hata vermemesi için bunu da baştan kuruyoruz)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS geri_bildirimler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_metni TEXT,
            durum TEXT,
            yapay_zeka_cevabi TEXT,
            tarih DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # --- VERİ SETİ 1: GÜNLÜK ŞİKAYETLER (Senin hazırladığın dev liste) ---
    gunluk_hastaliklar = [
        ("Sabah kalp çarpıntısı", "Kortizol artışı", "Yataktan yavaş kalkmak, derin nefes almak", "Dolaşım"),
        ("Sürekli esneme isteği", "Yorgunluk", "Odayı havalandırmak", "Genel"),
        ("Sabah hafif titreme", "Kan şekeri düşüşü", "Proteinli kahvaltı", "Sindirim"),
        ("Sıcak duş sonrası baş dönmesi", "Tansiyon düşmesi", "Ilık duş almak", "Dolaşım"),
        ("Gün içinde ani üşüme", "Kan şekeri dalgalanması", "Ara öğün yapmak", "Sindirim"),
        ("Sürekli iç çekme", "Anksiyete", "Nefes egzersizi", "Psikolojik"),
        ("Sabah bulanık görme", "Göz kuruluğu", "Suni gözyaşı", "Baş/Göz/Kulak"),
        ("Uzun ekran sonrası baş basıncı", "Göz yorgunluğu", "20-20-20 kuralı", "Baş/Göz/Kulak"),
        ("Göz kenarında kas atması", "Kafein, yorgunluk", "Uyku artırmak", "Baş/Göz/Kulak"),
        ("Sabah göz kuruluğu", "Düşük nem", "Oda nemlendirmek", "Baş/Göz/Kulak"),
        ("Kulakta basınç hissi", "Basınç değişimi", "Sakız çiğnemek", "Baş/Göz/Kulak"),
        ("Yataktan kalkınca uğultu", "Ani tansiyon değişimi", "Yavaş kalkmak", "Dolaşım"),
        ("Sabah ağızda kötü tat", "Ağız kuruluğu", "Dil temizliği", "Ağız/Boğaz"),
        ("Sabah çene sertliği", "Diş sıkma", "Gece plağı", "Kas/İskelet"),
        ("Uzun konuşunca boğaz yorulması", "Ses zorlanması", "Ilık su", "Ağız/Boğaz"),
        ("Sabah mide ekşimesi", "Gece geç yemek", "Erken akşam yemeği", "Sindirim"),
        ("Yemekten sonra uyku hali", "Kan şekeri artışı", "Kısa yürüyüş", "Sindirim"),
        ("Aç kalınca el titremesi", "Hipoglisemi", "Ara öğün", "Sindirim"),
        ("Yemek sonrası göğüs yanması", "Reflü", "Yağlı gıda azaltmak", "Sindirim"),
        ("Sabah mide boşluk hissi", "Asit üretimi", "Hafif kahvaltı", "Sindirim"),
        ("Boyunda çıtırtı", "Eklem gazı", "Germe egzersizi", "Kas/İskelet"),
        ("Uzun oturunca sırt yanması", "Postür bozukluğu", "Saat başı kalkmak", "Kas/İskelet"),
        ("Omuzda yanma", "Kas gerilimi", "Sıcak kompres", "Kas/İskelet"),
        ("Sabah kas gevşekliği", "Hareketsizlik", "Esneme", "Kas/İskelet"),
        ("Yatarken bacak atması", "Uyku refleksi", "Magnezyumlu besin", "Uyku"),
        ("Soğukta parmak renk değişimi", "Damar daralması", "Eldiven", "Dolaşım"),
        ("Sabah yüz şişliği", "Tuz", "Tuz azaltmak", "Genel"),
        ("Akşam ayak ısınması", "Dolaşım", "Ayakları yükseltmek", "Dolaşım"),
        ("Yüzde ani sıcaklık", "Stres", "Nefes egzersizi", "Psikolojik"),
        ("Gece terleme", "Oda sıcaklığı", "Serin ortam", "Uyku"),
        ("Gece yön şaşırma", "Derin uyku", "Düzenli uyku", "Uyku"),
        ("Sabah baş basıncı", "Sinüs doluluğu", "Buhar", "Baş/Göz/Kulak"),
        ("Gün içinde halsizlik", "Susuzluk", "Su içmek", "Genel"),
        ("Sabah ellerde şişlik", "Sıvı birikimi", "Tuz azaltmak", "Genel"),
        ("Akşam göz yanması", "Ekran", "Mola vermek", "Baş/Göz/Kulak"),
        ("Sabah boğaz kuruluğu", "Ağız açık uyuma", "Oda nemi", "Solunum"),
        ("Sabah burun tıkanıklığı", "Alerji", "Odayı temizlemek", "Solunum"),
        ("Sabah ses kısıklığı", "Reflü", "Gece geç yememek", "Ağız/Boğaz"),
        ("Kafada hafif zonklama", "Yorgunluk", "Dinlenmek", "Baş/Göz/Kulak"),
        ("Gün içinde ani açlık", "Kan şekeri düşüşü", "Dengeli beslenme", "Sindirim"),
        ("Sabah mide bulantısı", "Açlık", "Küçük atıştırmalık", "Sindirim"),
        ("Gece bacak huzursuzluğu", "Dolaşım", "Hafif yürüyüş", "Dolaşım"),
        ("El ayak soğukluğu", "Dolaşım", "Hareket etmek", "Dolaşım"),
        ("Sabah diş hassasiyeti", "Diş sıkma", "Yumuşak fırça", "Ağız/Boğaz"),
        ("Uzun süre aç kalınca baş dönmesi", "Düşük şeker", "Ara öğün", "Sindirim"),
        ("Sabah boyun sertliği", "Yanlış yastık", "Uygun yastık", "Kas/İskelet"),
        ("Gün içinde hafif baş dönmesi", "Susuzluk", "Su içmek", "Genel"),
        ("Akşamları ayak şişliği", "Uzun süre ayakta kalma", "Dinlenmek", "Dolaşım"),
        ("Sabah cilt kuruluğu", "Nem eksikliği", "Nemlendirici", "Cilt/Saç"),
        ("Gün içinde hafif mide gurultusu", "Açlık", "Atıştırmalık", "Sindirim"),
        ("Sabah omuz sertliği", "Uyku pozisyonu", "Esneme", "Kas/İskelet"),
        ("Uzun yazı yazınca bilek ağrısı", "Tekrarlayan hareket", "Mola", "Kas/İskelet"),
        ("Gün içinde göz sulanması", "Rüzgar veya kuruluk", "Göz koruma", "Baş/Göz/Kulak"),
        ("Sabah hafif baş ağrısı", "Susuzluk", "Su içmek", "Genel"),
        ("Gece ağız kuruluğu", "Ağız açık uyuma", "Nemli ortam", "Solunum"),
        ("Sabah hafif kas ağrısı", "Hareketsizlik", "Germe", "Kas/İskelet"),
        ("Gün içinde çarpıntı hissi", "Kafein", "Kahve azaltmak", "Dolaşım"),
        ("Sabah mide yanması", "Asit", "Asitli içecek azaltmak", "Sindirim"),
        ("Gün içinde ani yorgunluk", "Uykusuzluk", "Uyku düzeni", "Uyku"),
        ("Sabah hafif göz şişliği", "Tuz", "Soğuk kompres", "Baş/Göz/Kulak"),
        ("Uzun süre ayakta kalınca bel ağrısı", "Kas yorgunluğu", "Dinlenme", "Kas/İskelet"),
        ("Sabah hafif sersemlik", "Ani kalkma", "Yavaş hareket", "Genel"),
        ("Gün içinde hafif titreme", "Açlık", "Ara öğün", "Sindirim"),
        ("Sabah burun kuruluğu", "Klima/Kuru hava", "Nem artırmak", "Solunum"),
        ("Akşam omuz düşüklüğü hissi", "Yorgunluk", "Dinlenmek", "Kas/İskelet"),
        ("Sabah kulak dolgunluğu", "Basınç", "Yutkunmak", "Baş/Göz/Kulak"),
        ("Gün içinde mide şişkinliği", "Gaz", "Yavaş yemek", "Sindirim"),
        ("Sabah boğaz gıcığı", "Kuruluk", "Ilık su", "Solunum"),
        ("Gün içinde halsiz hissetme", "Düzensiz beslenme", "Dengeli öğün", "Genel"),
        ("Sabah hafif nefes darlığı hissi", "Anksiyete", "Derin nefes", "Solunum"),
        ("Uzun süre oturunca bacak karıncalanması", "Sinir basısı", "Pozisyon değiştirmek", "Sinir Sistemi"),
        ("Sabah el sertliği", "Gece hareketsizlik", "Parmak egzersizi", "Kas/İskelet"),
        ("Gün içinde mide kazınması", "Açlık", "Atıştırmalık", "Sindirim"),
        ("Sabah göz çapaklanması", "Kuruluk", "Ilık su ile temizlemek", "Baş/Göz/Kulak"),
        ("Gün içinde yüz kızarması", "Stres", "Nefes egzersizi", "Psikolojik"),
        ("Sabah hafif sırt ağrısı", "Yanlış yatak", "Uygun yatak", "Kas/İskelet"),
        ("Gün içinde ağız kuruluğu", "Az su", "Su tüketimi", "Genel"),
        ("Sabah hafif baş dönmesi", "Düşük tansiyon", "Yavaş kalkmak", "Dolaşım"),
        ("Gün içinde ani enerji düşüşü", "Şeker dalgalanması", "Dengeli beslenme", "Sindirim"),
        ("Sabah mide gurultusu", "Açlık", "Kahvaltı", "Sindirim"),
        ("Gün içinde omuz kasılması", "Stres", "Omuz gevşetme", "Psikolojik"),
        ("Sabah hafif göz yanması", "Kuruluk", "Göz damlası", "Baş/Göz/Kulak"),
        ("Gün içinde hafif sersemlik", "Susuzluk", "Su içmek", "Genel"),
        ("Sabah parmak sertliği", "Hareketsizlik", "El egzersizi", "Kas/İskelet"),
        ("Gün içinde çene sıkma", "Stres", "Farkındalık", "Psikolojik"),
        ("Sabah hafif mide rahatsızlığı", "Açlık", "Küçük kahvaltı", "Sindirim"),
        ("Gün içinde kulak çınlaması kısa süreli", "Yorgunluk", "Dinlenmek", "Baş/Göz/Kulak"),
        ("Sabah ayak tabanı ağrısı", "Sert zemin", "Esneme", "Kas/İskelet"),
        ("Gün içinde hafif göğüs baskısı hissi", "Stres", "Derin nefes", "Psikolojik"),
        ("Sabah hafif titrek his", "Kan şekeri", "Kahvaltı", "Sindirim"),
        ("Gün içinde boyun kasılması", "Telefon kullanımı", "Postür düzeltmek", "Kas/İskelet"),
        ("Sabah hafif cilt kaşıntısı", "Kuruluk", "Nemlendirici", "Cilt/Saç"),
        ("Gün içinde kısa süreli bulanıklık", "Yorgunluk", "Dinlenmek", "Baş/Göz/Kulak"),
        ("Sabah hafif baş zonklaması", "Susuzluk", "Su", "Genel"),
        ("Gün içinde mide ekşimesi", "Asit", "Yağlı yiyecek azaltmak", "Sindirim"),
        ("Sabah hafif halsizlik", "Uykusuzluk", "Uyku düzeni", "Uyku"),
        ("Gün içinde el terlemesi", "Stres", "Rahatlama teknikleri", "Psikolojik"),
        ("Sabah hafif sırt sertliği", "Uyku pozisyonu", "Germe", "Kas/İskelet"),
        ("Gün içinde kısa süreli nefes daralması hissi", "Anksiyete", "Kontrollü nefes", "Psikolojik"),
        ("Sabah hafif serinlik hissi", "Metabolik değişim", "Hafif hareket", "Genel")
    ]

    # --- VERİ SETİ 2: VİTAMİN VE MİNERAL EKSİKLİKLERİ ---
    vitamin_mineral = [
        ("Aşırı yorgunluk, sinirlilik, hafıza zayıflığı, bacaklarda şişlik", "B1 Vitamini (Tiamin) Eksikliği", "Tam tahıllar, fındık ve baklagiller tüketin.", "Vitamin Eksikliği"),
        ("Gözlerde kanlanma, dudak kenarlarında yaralar, ışığa hassasiyet", "B2 Vitamini (Riboflavin) Eksikliği", "Süt, mantar, ıspanak ve badem tüketin.", "Vitamin Eksikliği"),
        ("Ciltte simetrik kızarıklık, ishal, zihinsel bulanıklık (Pellegra benzeri)", "B3 Vitamini (Niasin) Eksikliği", "Tavuk, balık, yer fıstığı ve esmer pirinç tüketin.", "Vitamin Eksikliği"),
        ("Ayaklarda yanma hissi, kronik yorgunluk, sinirlilik, uyku bozukluğu", "B5 Vitamini (Pantotenik Asit) Eksikliği", "Avokado, yoğurt, mantar ve tatlı patates tüketin.", "Vitamin Eksikliği"),
        ("Sürekli depresif ruh hali, kafa karışıklığı, zayıf bağışıklık", "B6 Vitamini (Piridoksin) Eksikliği", "Nohut, somon, muz ve tavuk tüketin.", "Vitamin Eksikliği"),
        ("Saç dökülmesi, yüz çevresinde kırmızı döküntüler, kırılgan tırnaklar", "B7 Vitamini (Biotin) Eksikliği", "Yumurta sarısı, badem, tatlı patates ve ceviz tüketin.", "Vitamin Eksikliği"),
        ("Dilde şişme ve kızarıklık, aşırı yorgunluk, ağız içinde aftlar", "B9 Vitamini (Folik Asit) Eksikliği", "Koyu yeşil yapraklı sebzeler, mercimek ve kuşkonmaz tüketin.", "Vitamin Eksikliği"),
        ("Denge kaybı, ellerde uyuşma, hafıza kaybı, dilde pürüzsüzleşme", "B12 Vitamini (Kobalamin) Eksikliği", "Kırmızı et ve hayvansal gıdalar tüketin. Sinir hasarı riskine karşı doktora görünün.", "Vitamin Eksikliği"),
        ("Gece körlüğü, gözde kuruluk, ciltte kaz derisi görünümü", "A Vitamini Eksikliği", "Havuç, ıspanak ve ciğer tüketin.", "Vitamin Eksikliği"),
        ("Sık hastalanma, diş eti kanaması, yavaş iyileşen yaralar", "C Vitamini Eksikliği", "Turunçgiller, kırmızı biber ve kivi tüketin.", "Vitamin Eksikliği"),
        ("Kemik ağrısı, kas zayıflığı, terleyen baş, sık kemik kırılmaları", "D Vitamini Eksikliği", "Güneş ışığı alın. Kan tahlili ile seviyenize baktırıp takviye kullanın.", "Vitamin Eksikliği"),
        ("Yürüme zorluğu, kas zayıflığı, titreme, görme sorunları", "E Vitamini Eksikliği", "Ayçiçeği çekirdeği, badem ve zeytinyağı tüketin.", "Vitamin Eksikliği"),
        ("Sebepsiz morarmalar, kanayan diş etleri, küçük kesiklerin uzun süre kanaması", "K Vitamini Eksikliği", "Brokoli, ıspanak, lahana ve brüksel lahanası tüketin.", "Vitamin Eksikliği"),
        ("Toprak, buz veya tebeşir yeme isteği (Pika), huzursuz bacaklar, solgunluk", "Demir Eksikliği (Anemi)", "Kırmızı et, pekmez ve C vitamini ile birlikte yeşillik tüketin.", "Mineral Eksikliği"),
        ("Göz kapağı seğirmesi, gece giren bacak krampları, çikolata krizleri", "Magnezyum Eksikliği", "Kabak çekirdeği, bitter çikolata ve ıspanak tüketin.", "Mineral Eksikliği"),
        ("Tat ve koku duyusunda azalma, saç incelmesi, tırnaklarda beyaz lekeler", "Çinko Eksikliği", "Kabak çekirdeği, kırmızı et ve baklagiller tüketin.", "Mineral Eksikliği"),
        ("Boyunda şişlik hissi, anlamsız kilo alma, sürekli üşüme, kuru cilt", "İyot Eksikliği", "İyotlu tuz, deniz ürünleri ve yumurta tüketin.", "Mineral Eksikliği"),
        ("Kas krampları, diş çürümeleri, tırnak zayıflığı, kemik erimesi", "Kalsiyum Eksikliği", "Süt, peynir, chia tohumu ve badem tüketin.", "Mineral Eksikliği"),
        ("Kalp çarpıntısı, kas yorgunluğu, kabızlık, sürekli susama", "Potasyum Eksikliği", "Muz, patates, fasulye ve avokado tüketin.", "Mineral Eksikliği"),
        ("Zihinsel sis, saç dökülmesi, kas zayıflığı, kısırlık sorunları", "Selenyum Eksikliği", "Brezilya cevizi, balık ve tavuk tüketin.", "Mineral Eksikliği"),
        ("Erken saç beyazlaması, sürekli yorgunluk, solgun cilt, eklem ağrıları", "Bakır Eksikliği", "Karaciğer, istiridye, kaju ve bitter çikolata tüketin.", "Mineral Eksikliği"),
        ("Sürekli tatlı krizi, kan şekeri dalgalanmaları, yemek sonrası ani uyku", "Krom Eksikliği", "Brokoli, tam buğday ve üzüm suyu tüketin.", "Mineral Eksikliği"),
        ("Kemik ağrısı, iştahsızlık, eklem sertliği", "Fosfor Eksikliği", "Süt ürünleri, et ve fındık tüketin.", "Mineral Eksikliği"),
        ("Baş ağrısı, mide bulantısı, zihinsel bulanıklık, kas spazmları", "Sodyum Eksikliği (Hiponatremi)", "Aşırı su tüketimini dengeleyin, kontrollü tuz ve zeytin tüketin.", "Mineral Eksikliği")
    ]

    # İki listeyi birleştiriyoruz
    tum_veriler = gunluk_hastaliklar + vitamin_mineral

    # Veritabanına toplu kayıt yapıyoruz
    cursor.executemany('''
        INSERT INTO bilgi_tabani (belirti, neden, oneri, kategori) 
        VALUES (?, ?, ?, ?)
    ''', tum_veriler)

    conn.commit()
    conn.close()
    
    toplam_kayit = len(tum_veriler)
    print(f"✅ MUAZZAM! Yeni Merkez Veritabanı başarıyla oluşturuldu.")
    print(f"📊 Toplam Kayıt Sayısı: {toplam_kayit} (Günlük Hastalıklar + Vitamin/Mineral)")

if __name__ == "__main__":
    birlesik_veritabanini_kur()
