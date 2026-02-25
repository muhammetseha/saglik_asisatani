import sqlite3
import pandas as pd

DB_NAME = 'saglik_asistani.db'

def verileri_getir():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM bilgi_tabani", conn)
    conn.close()
    return df

def puan_ekle(kayit_id, verilen_puan):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE bilgi_tabani 
            SET puan_toplami = puan_toplami + ?, 
                oy_sayisi = oy_sayisi + 1 
            WHERE id = ?
        ''', (verilen_puan, kayit_id))
        conn.commit()
    except Exception as e:
        print(f"Puan eklenirken hata: {e}")
    finally:
        conn.close()

def geri_bildirim_kaydet(kullanici_metni, durum, yapay_zeka_cevabi="Yok"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Eğer "geri_bildirimler" tablosu yoksa otomatik oluşturur (Sistemi bozmaz)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS geri_bildirimler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_metni TEXT NOT NULL,
            durum TEXT NOT NULL,
            yapay_zeka_cevabi TEXT,
            tarih DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        INSERT INTO geri_bildirimler (kullanici_metni, durum, yapay_zeka_cevabi) 
        VALUES (?, ?, ?)
    ''', (kullanici_metni, durum, yapay_zeka_cevabi))
    
    conn.commit()
    conn.close()

def geri_bildirimleri_getir():
    """Geliştirici paneli için kaydedilen hataları liste halinde çeker."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS geri_bildirimler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_metni TEXT NOT NULL,
            durum TEXT NOT NULL,
            yapay_zeka_cevabi TEXT,
            tarih DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    df = pd.read_sql_query("SELECT * FROM geri_bildirimler ORDER BY id DESC", conn)
    conn.close()
    return df


