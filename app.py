import streamlit as st
import time # Yükleme animasyonu için gerekli
from model import tahmin_yap
from database import puan_ekle

# 1. SAYFA AYARLARI (Geniş mod ve sekme ismi)
st.set_page_config(page_title="Yapay Zeka Sağlık Asistanı", page_icon="🩺", layout="centered")

# --- SOL MENÜ (SIDEBAR) ---
with st.sidebar:
    st.title("🧠 Proje Hakkında")
    st.info("Bu sistem, **TF-IDF Vektörizasyonu** ve **Kosinüs Benzerliği** (Karakter N-Gram) algoritmaları kullanılarak geliştirilmiş bir NLP projesidir.")
    
    st.write("---")
    st.write("📊 **Veritabanı:** 71 Farklı Belirti (şimdilik:))")
    st.write("🔄 **Öğrenme Modeli:** Kullanıcı Geri Bildirimi")
    st.write("🎓 **Geliştirici:** Muhammet Seha Çebi")
    
    # Uyarı metni
    st.warning("⚠️ Sorumluluk Reddi: Bu bir bitirme projesidir, kesin tıbbi teşhis koymaz. Lütfen ciddi durumlarda doktora başvurun.")

# --- ANA SAYFA ---
st.title("🩺 Akıllı Sağlık Asistanı")
st.markdown("*Günlük sağlık şikayetlerinizi yazın, istatistiksel modelimiz olası nedenleri bulsun.*")

# Oturum (Session) Yönetimi
if 'sonuc' not in st.session_state:
    st.session_state.sonuc = None
if 'puanlandi' not in st.session_state:
    st.session_state.puanlandi = False

# Kullanıcı Girişi
kullanici_girdisi = st.text_input("Şikayetiniz nedir?", placeholder="Örn: Sınav stresinden midem ağrıyor, uyuyamıyorum...")

# Tahmin Butonu ve Animasyon
if st.button("🔍 Yapay Zekaya Sor", type="primary", use_container_width=True):
    if kullanici_girdisi:
        # Yapay zeka düşünüyormuş gibi şık bir bekleme efekti
        with st.spinner('Doğal Dil İşleme modeli veritabanını tarıyor...'):
            time.sleep(1) # Ekranda 1 saniye kalması için (Sunumda çok havalı durur)
            sonuc = tahmin_yap(kullanici_girdisi)
            st.session_state.sonuc = sonuc
            st.session_state.puanlandi = False
    else:
        st.error("Lütfen önce bir şikayet yazın.")

# --- SONUÇLARI GÖSTERME ---
if st.session_state.sonuc:
    sonuc = st.session_state.sonuc
    st.write("---")
    
    if "hata" in sonuc:
        st.warning("😕 " + sonuc["hata"])
    else:
        # Sonucu daha şık kutularda gösterme
        st.success("✅ Sizin için en uygun istatistiksel eşleşmeyi buldum!")
        
        # Streamlit Metric ile skoru janjanlı gösterme
        st.metric(label="Yapay Zeka Güven Skoru", value=f"%{int(sonuc['benzerlik_skoru'] * 100)}")
        
        # Sonuç Kartı
        with st.container(border=True):
            st.markdown(f"**🔬 Eşleşen Kategori:** `{sonuc.get('kategori', 'Genel')}`")
            st.markdown(f"**📌 Algılanan Belirti:** {sonuc['belirti']}")
            st.markdown(f"**⚠️ Olası Neden:** {sonuc['neden']}")
            st.markdown(f"**💡 Önerimiz:** {sonuc['oneri']}")
        
        # --- PUANLAMA SİSTEMİ ---
        if not st.session_state.puanlandi:
            st.write("")
            st.markdown("### 🌟 Bu tahmin ne kadar doğruydu?")
            st.caption("Vereceğiniz puan sistemin doğruluğunu (Ağırlık Puanını) artıracaktır.")
            
            # Yıldızları şık bir şekilde yan yana dizme
            cols = st.columns(5)
            for i in range(1, 6):
                if cols[i-1].button(f"{i} ⭐", key=f"star_{i}", use_container_width=True):
                    puan_ekle(sonuc["id"], i)
                    st.session_state.puanlandi = True
                    st.rerun()
        else:
            st.info("💖 Geri bildiriminiz veritabanına işlendi. Teşekkürler!")

# Sayfanın en altına gizli bilgi kutusu
st.write("---")
with st.expander("❓ Sistem Nasıl Çalışır?"):
    st.write("""
    1. Yazdığınız metin TF-IDF algoritması ile matematiksel vektörlere dönüştürülür.
    2. Türkçe sondan eklemeli bir dil olduğu için kelimeler N-Gram (harf öbekleri) mantığıyla parçalanır.
    3. Kosinüs Benzerliği (Cosine Similarity) kullanılarak veritabanındaki 71 hastalıkla açısı hesaplanır.
    4. En yakın açıya sahip olan sonuç size sunulur.
    """)
