from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Bir önceki adımda yazdığımız veritabanı dosyasından fonksiyonumuzu çağırıyoruz
from database import verileri_getir

def tahmin_yap(kullanici_sorusu):
    """
    Kullanıcının metnini alır, TF-IDF ile vektörleştirir ve 
    Kosinüs Benzerliği kullanarak veritabanındaki en uygun yanıtı bulur.
    """
    # 1. Veritabanından mevcut bilgileri çek (Pandas DataFrame olarak gelir)
    df = verileri_getir()
    
    if df.empty:
        return {"hata": "Veritabanı şu an boş!"}

    # 2. NLP Hazırlığı: Veritabanındaki belirtileri ve kullanıcının sorusunu bir listeye koy
    tum_metinler = df['belirti'].tolist()
    tum_metinler.append(kullanici_sorusu) # Kullanıcının sorusunu en sona ekliyoruz

    # 3. Metinleri Sayısallaştırma (Vektörizasyon)
    # analyzer='char_wb' kelimeleri harf öbeklerine ayırır. Türkçe için hayat kurtarır!
    vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5))
    tfidf_matrix = vectorizer.fit_transform(tum_metinler)

    # 4. Benzerlik Hesaplama
    # tfidf_matrix[-1] -> En sondaki metin yani kullanıcının sorusu
    # tfidf_matrix[:-1] -> Veritabanındaki tüm belirtiler
    benzerlik_skorlari = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    
    # En yüksek benzerlik skoruna sahip olan satırın indeksini bul
    en_iyi_eslesme_index = benzerlik_skorlari.argmax()
    en_yuksek_skor = benzerlik_skorlari[0][en_iyi_eslesme_index]

    # 5. Sonuç Kararı (Eşik Değeri Kontrolü)
    # Eğer benzerlik %15'ten (0.15) büyükse mantıklı bir cevap bulmuşuz demektir
    if en_yuksek_skor > 0.15:
        bulunan_kayit = df.iloc[en_iyi_eslesme_index]
        return {
            "id": int(bulunan_kayit['id']),
            "belirti": bulunan_kayit['belirti'],
            "neden": bulunan_kayit['neden'],
            "oneri": bulunan_kayit['oneri'],
            "benzerlik_skoru": round(en_yuksek_skor, 3) # Virgülden sonra 3 hane
        }
    else:
        return {"hata": "Üzgünüm, sorunuzu tam anlayamadım veya veritabanımda buna uygun bir bilgi yok."}

# Sadece bu dosya çalıştırıldığında test etmek için:
if __name__ == "__main__":
    print("--- Zeka Modeli Testi ---")
    test_sorusu ="Sınav stresinden dolayı mideme kramplar giriyor ve ağrıyor"
    print(f"Soru: {test_sorusu}\n")
    
    sonuc = tahmin_yap(test_sorusu)
    
    if "hata" in sonuc:
        print(sonuc["hata"])
    else:
        print(f"Eşleşen Belirti: {sonuc['belirti']} (Skor: {sonuc['benzerlik_skoru']})")
        print(f"Olası Neden: {sonuc['neden']}")
        print(f"Öneri: {sonuc['oneri']}")