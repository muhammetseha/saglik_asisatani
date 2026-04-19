import streamlit as st
import pandas as pd
import sqlite3
import time
from model import tahmin_yap
from database import puan_ekle, geri_bildirim_kaydet, geri_bildirimleri_getir

st.set_page_config(page_title="Yapay Zeka Sağlık Asistanı", page_icon="🩺", layout="centered")

# --- HAFIZA YÖNETİMİ ---
if 'sonuc' not in st.session_state:
    st.session_state.sonuc = None
if 'puanlandi' not in st.session_state:
    st.session_state.puanlandi = False
if 'aranan_kelime' not in st.session_state:
    st.session_state.aranan_kelime = ""

# --- YENİ: POP-UP (DIALOG) FONKSİYONU ---
@st.dialog("🌟 Yapay Zekayı Değerlendirin")
def puanlama_popup(sonuc_id, aranan_kelime, bulunan_belirti):
    st.markdown(f"**Sizin Şikayetiniz:** {aranan_kelime}")
    st.markdown(f"**Benim Tahminim:** {bulunan_belirti}")
    st.write("---")
    st.write("Bu tahmin sizin için ne kadar doğruydu? Lütfen 1 ile 5 arasında puan verin:")
    
    cols = st.columns(5)
    for i in range(1, 6):
        benzersiz_kimlik = f"popup_star_{i}_id_{sonuc_id}"
        if cols[i-1].button(f"{i} ⭐", key=benzersiz_kimlik, use_container_width=True):
            puan_ekle(sonuc_id, i)
            st.session_state.puanlandi = True
            
            # 1 Yıldız verilirse sisteme kaydet
            if i == 1:
                geri_bildirim_kaydet(
                    kullanici_metni=aranan_kelime, 
                    durum="1 Yıldız Aldı (Hatalı Tahmin)", 
                    yapay_zeka_cevabi=bulunan_belirti
                )
            st.rerun()

def verileri_kategoriye_gore_getir(secilen_kategori=None):
    conn = sqlite3.connect('saglik_asistani.db')
    df = pd.read_sql_query("SELECT * FROM bilgi_tabani", conn)
    conn.close()
    if secilen_kategori and secilen_kategori != "Tümü":
        df = df[df['kategori'] == secilen_kategori]
    return df

with st.sidebar:
    st.title("🧠 Proje Hakkında")
    st.info("Bu sistem, **TF-IDF Vektörizasyonu** ve **Kosinüs Benzerliği** algoritmaları kullanılarak geliştirilmiş bir NLP projesidir.")
    st.write("---")
    try:
        conn = sqlite3.connect('saglik_asistani.db')
        toplam_kayit = pd.read_sql_query("SELECT COUNT(id) FROM bilgi_tabani", conn).iloc[0,0]
        conn.close()
        st.write(f"📊 **Veritabanı:** {toplam_kayit} Farklı Belirti")
    except:
        st.write("📊 **Veritabanı:** Bağlanıyor...")
    st.write("🔄 **Öğrenme Modeli:** Kullanıcı Geri Bildirimi")
    st.write("🎓 **Geliştirici:** Muhammet Seha Çebi")
    st.warning("⚠️ Sorumluluk Reddi: Bu bir bitirme projesidir, kesin tıbbi teşhis koymaz. Lütfen ciddi durumlarda doktora başvurun.")

st.title("🩺 Akıllı Sağlık Asistanı")

tab1, tab2, tab3 = st.tabs(["🔍 Yapay Zekaya Sor", "📂 Kategorilere Göre İncele", "⚙️ Geliştirici Paneli"])

with tab1:
    st.markdown("*Günlük sağlık şikayetlerinizi yazın, istatistiksel modelimiz olası nedenleri bulsun.*")

    kullanici_girdisi = st.text_input("Şikayetiniz nedir?", placeholder="Örn: Yemekten sonra ağırlık çöküyor...")

    if st.button("🔍 Yapay Zekaya Sor", type="primary", use_container_width=True):
        if kullanici_girdisi:
            st.session_state.aranan_kelime = kullanici_girdisi 
            with st.spinner('Doğal Dil İşleme modeli veritabanını tarıyor...'):
                time.sleep(0.5)
                sonuc = tahmin_yap(kullanici_girdisi)
                st.session_state.sonuc = sonuc
                st.session_state.puanlandi = False
                
                if sonuc.get("durum") == "hata":
                    geri_bildirim_kaydet(kullanici_girdisi, "Bulunamadı - Veritabanında Yok")
        else:
            st.error("Lütfen önce bir şikayet yazın.")

    if st.session_state.sonuc:
        sonuc = st.session_state.sonuc
        st.write("---")
        
        if sonuc.get("durum") == "eksik_bilgi":
            st.warning("🧐 " + sonuc["hata"])
            
        elif sonuc.get("durum") == "hata":
            st.error("😕 " + sonuc["hata"])
            st.info("📝 *Bu arama, sistemin kendini geliştirmesi için Geliştirici Paneli'ne kaydedildi.*")
            
        elif sonuc.get("durum") == "oneri_sun":
            st.warning("🤔 " + sonuc["mesaj"])
            for i, oneri in enumerate(sonuc["oneriler"]):
                if st.button(f"👉 {oneri}", key=f"oneri_btn_{i}_{oneri}", use_container_width=True):
                    st.session_state.aranan_kelime = oneri
                    st.session_state.sonuc = tahmin_yap(oneri)
                    st.session_state.puanlandi = False
                    st.rerun()
                    
        elif sonuc.get("durum") == "kesin_sonuc":
            st.success("✅ Sizin için en uygun istatistiksel eşleşmeyi buldum!")
            st.metric(label="Yapay Zeka Güven Skoru", value=f"%{int(sonuc['benzerlik_skoru'] * 100)}")
            
            with st.container(border=True):
                st.markdown(f"**🔬 Kategori:** `{sonuc.get('kategori', 'Genel')}`")
                st.markdown(f"**📌 Algılanan Belirti:** {sonuc['belirti']}")
                st.markdown(f"**⚠️ Olası Neden:** {sonuc['neden']}")
                
                if "Doktora Görünün" in sonuc['oneri']:
                    st.error(f"🚨 **Uyarı:** {sonuc['oneri']}")
                else:
                    st.markdown(f"**💡 Önerimiz:** {sonuc['oneri']}")

# --- POP-UP TETİKLEYİCİ BUTON (DİKKAT ÇEKİCİ VERSİYON) ---
            if not st.session_state.puanlandi:
                # 1. TAKTİK: Ekranın sağ altından kayarak giren dinamik bildirim (Gözü aşağı çeker)
                st.toast("Lütfen tahmini değerlendirmeyi unutmayın! 👇", icon="🌟")
                st.toast("Geri bildiriminiz veritabanını geliştirecek. 🤖", icon="📈")
                
                # 2. TAKTİK: Gözden kaçması imkansız hale getirilmiş UI tasarımı
                st.write("")
                st.write("---")
                st.error("👇 **YAPAY ZEKANIN ÖĞRENMESİNE YARDIMCI OLUN** 👇")
                
                # Butonu devasa ve tamamen dikkat çekici hale getirdik
                if st.button("🚨 TAHMİNİ PUANLA VE SİSTEMİ GELİŞTİR 🚨", type="primary", use_container_width=True):
                    puanlama_popup(sonuc["id"], st.session_state.aranan_kelime, sonuc["belirti"])
            else:
                st.success("💖 Harika! Geri bildiriminiz veritabanına işlendi. Teşekkürler!")

# ==========================================
# 3. SEKME: GELİŞTİRİCİ PANELİ
# ==========================================
with tab3:
    st.markdown("### 🛠️ Geliştirici Geri Bildirim Paneli")
    st.write("Bu alan sadece sistem yöneticisi (geliştirici) içindir. Lütfen erişim sağlamak için şifrenizi girin.")
    
    girilen_sifre = st.text_input("Yönetici Şifresi:", type="password", key="admin_password_input")
    
    if girilen_sifre == "admin123":
        st.success("🔓 Giriş Başarılı! Veritabanı kayıtlarına erişildi.")
        
        try:
            df_bildirim = geri_bildirimleri_getir()
            if not df_bildirim.empty:
                st.dataframe(df_bildirim, use_container_width=True, hide_index=True)
            else:
                st.info("🎉 Harika! Henüz kaydedilmiş bir hata veya 1 yıldızlı şikayet yok.")
        except Exception as e:
            st.error(f"Tablo yüklenirken hata oluştu: {e}")
            
    elif girilen_sifre != "": 
        st.error("❌ Hatalı Şifre! Yetkisiz Erişim.")
