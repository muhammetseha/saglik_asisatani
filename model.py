from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from database import verileri_getir

def tahmin_yap(kullanici_sorusu):
    df = verileri_getir()
    
    if df.empty:
        return {"durum": "hata", "hata": "Veritabanı şu an boş!"}

    # YENİ KURAL 1: EKSİK BİLGİ KONTROLÜ
    # Eğer kullanıcı 2 kelimeden az yazdıysa veya çok kısa bir şey girdiyse:
    kelimeler = kullanici_sorusu.strip().split()
    if len(kelimeler) < 2 or len(kullanici_sorusu) < 6:
        return {
            "durum": "eksik_bilgi",
            "hata": f"Sadece '{kullanici_sorusu}' yazdınız. Size doğru yardımcı olabilmem için şikayetinizi biraz daha detaylı yazar mısınız? (Örn: Ayak tabanımda kaşıntı var)"
        }

    tum_metinler = df['belirti'].tolist()
    tum_metinler.append(kullanici_sorusu)

    vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5))
    tfidf_matrix = vectorizer.fit_transform(tum_metinler)

    benzerlik_skorlari = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]
    sirali_indexler = benzerlik_skorlari.argsort()[::-1]
    
    en_iyi_index = sirali_indexler[0]
    en_yuksek_skor = benzerlik_skorlari[en_iyi_index]

    # YENİ KURAL 2: BARAJ SKORLARINI GÜNCELLEDİK
    # Kesin sonuç için artık %25 (0.25) benzemesi lazım
    if en_yuksek_skor >= 0.25:
        bulunan_kayit = df.iloc[en_iyi_index]
        return {
            "durum": "kesin_sonuc",
            "id": int(bulunan_kayit['id']),
            "belirti": bulunan_kayit['belirti'],
            "neden": bulunan_kayit['neden'],
            "oneri": bulunan_kayit['oneri'],
            "kategori": bulunan_kayit['kategori'],
            "benzerlik_skoru": round(en_yuksek_skor, 3)
        }
        
    # Skor %5 ile %25 arasındaysa (Yani tam emin olamadıysa)
    elif en_yuksek_skor >= 0.05:
        oneriler = []
        for i in range(3):
            idx = sirali_indexler[i]
            if benzerlik_skorlari[idx] > 0.02: 
                oneriler.append(df.iloc[idx]['belirti'])
                
        return {
            "durum": "oneri_sun",
            "mesaj": "Tam emin olamadım ama şunlardan birini mi demek istediniz?",
            "oneriler": oneriler
        }
        
    # Skor %5'in bile altındaysa
    else:
        return {
            "durum": "hata", 
            "hata": "Üzgünüm, yazdığınızı veritabanımdaki hiçbir hastalıkla eşleştiremedim."
        }
