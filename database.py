import sqlite3
import pandas as pd

DB_NAME = 'saglik_asistani.db'

def veritabanini_kur():
    """Veritabanını ve tablo yapısını sıfırdan oluşturur."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Eğer tablo zaten varsa silip yenisini oluşturuyoruz (temiz bir başlangıç için)
    cursor.execute('DROP TABLE IF EXISTS bilgi_tabani')
    
    # Tablo şemamız: İstatistiksel ağırlıklandırma için puan ve oy sayısı sütunları çok önemli
    cursor.execute('''
        CREATE TABLE bilgi_tabani (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            belirti TEXT NOT NULL,
            neden TEXT NOT NULL,
            oneri TEXT NOT NULL,
            kategori TEXT,
            puan_toplami REAL DEFAULT 0.0,
            oy_sayisi INTEGER DEFAULT 0
        )
    ''')

    # İlk uzman verilerimizi (Knowledge Base) hazırlıyoruz
    baslangic_verileri = [
        ("Sabah yorgun uyanmak", "Kalitesiz uyku döngüsü veya geç yatma.", "Yatmadan 3 saat önce yemeyi kesin, odayı havalandırın.", "Uyku"),
        ("Beyin sisi (brain fog)", "Yoğun stres veya uykusuzluk.", "Kısa molalar verin ve ekran süresini azaltın.", "Zihinsel"),
        ("Sabah ağız kokusu", "Gece ağızda biriken bakteriler.", "Yatmadan önce dilinizi de fırçalayın.", "Ağız"),
        ("Stres kaynaklı mide ağrısı", "Psikosomatik gerginlik.", "Nefes egzersizleri ve hafif bitki çayları deneyin.", "Sindirim"),
        ("Şişkinlik", "Hızlı yemek yeme veya gazlı içecek tüketimi.", "Yemekleri iyice çiğneyin ve porsiyonları küçültün.", "Sindirim"),
        ("Diz çıtırtısı", "Hareketsizlik veya eklem sıvısı hareketi.", "Düzenli hafif yürüyüşler ve esneme hareketleri yapın.", "Eklem"),
        ("Göz seğirmesi", "Aşırı kafein tüketimi veya uykusuzluk.", "Kafeini azaltın ve gözlerinizi dinlendirin.", "Göz"),
        ("El titremesi", "Kan şekeri düşüklüğü veya aşırı stres.", "Öğün atlamayın, sakinleşmeye çalışın.", "Genel")
        # İleride o 80 maddenin tamamını buraya ekleyebilirsin. Şimdilik test için bu kadarı yeterli.
    ]

    # Verileri tabloya toplu olarak ekliyoruz
    cursor.executemany('''
        INSERT INTO bilgi_tabani (belirti, neden, oneri, kategori) 
        VALUES (?, ?, ?, ?)
    ''', baslangic_verileri)

    conn.commit()
    conn.close()
    print("Veritabanı başarıyla kuruldu ve başlangıç verileri yüklendi!")

def verileri_getir():
    """Yapay zeka modelimizin kullanması için verileri Pandas DataFrame olarak çeker."""
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM bilgi_tabani", conn)
    conn.close()
    return df

# Eğer bu dosya doğrudan çalıştırılırsa kurulumu başlat
if __name__ == "__main__":
    veritabanini_kur()

def puan_ekle(kayit_id, verilen_puan):
    """
    Belirli bir kaydın puan toplamını ve oy sayısını günceller.
    verilen_puan: 1 ile 5 arasında bir tam sayı.
    """
    # Veritabanına bağlan
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # Mevcut puan_toplami ve oy_sayisi değerlerini veritabanından güncelle
        # id'si gelen kayit_id ile eşleşen satırı bulur
        cursor.execute('''
            UPDATE bilgi_tabani 
            SET puan_toplami = puan_toplami + ?, 
                oy_sayisi = oy_sayisi + 1 
            WHERE id = ?
        ''', (verilen_puan, kayit_id))
        
        # Değişiklikleri kaydet
        conn.commit()
        print(f"Kayıt {kayit_id} için {verilen_puan} puan başarıyla eklendi.")
        
    except Exception as e:
        print(f"Puan eklenirken bir hata oluştu: {e}")
        
    finally:
        # Bağlantıyı her durumda güvenle kapat
        conn.close()

# Test için (sadece bu dosya doğrudan çalıştırılırsa çalışır)
if __name__ == "__main__":
    # Veritabanını baştan kurduğumuz fonksiyon (eğer verileri sıfırlamak istersen yorumdan çıkar)
    # veritabanini_kur() 
    
    print("--- Puanlama Sistemi Testi ---")
    # Örnek: 4 numaralı id'ye (Stres kaynaklı mide ağrısı) 5 yıldız verelim
    puan_ekle(kayit_id=4, verilen_puan=5)    