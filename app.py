import streamlit as st
from model import tahmin_yap
from database import puan_ekle

# Sayfa ayarları
st.set_page_config(page_title="Akıllı Sağlık Asistanı", page_icon="🩺", layout="centered")

st.title("🩺 Akıllı Sağlık Asistanı")
st.write("Günlük sağlık şikayetlerinizi yazın, yapay zeka olası nedenleri ve önerileri bulsun.")
st.info("💡 İpucu: Sistem, verdiğiniz puanlarla kendini geliştirmektedir.")

# Oturum (Session) Yönetimi: Sayfa yenilendiğinde verilerin kaybolmaması için
if 'sonuc' not in st.session_state:
    st.session_state.sonuc = None
if 'puanlandi' not in st.session_state:
    st.session_state.puanlandi = False

# Kullanıcıdan girdi alma
st.write("---")
kullanici_girdisi = st.text_input("Şikayetiniz nedir? (Örn: Sınav stresinden midem ağrıyor)")

# Tahmin Butonu
if st.button("Nedenini Bul", type="primary"):
    if kullanici_girdisi:
        # model.py'deki fonksiyonumuzu çağırıyoruz
        sonuc = tahmin_yap(kullanici_girdisi)
        st.session_state.sonuc = sonuc
        st.session_state.puanlandi = False # Yeni arama yapıldığında puan durumunu sıfırla
    else:
        st.warning("Lütfen önce bir şikayet yazın.")

# Sonucu Gösterme ve Puanlama Ekranı
if st.session_state.sonuc:
    sonuc = st.session_state.sonuc
    st.write("---")
    
    # Hata varsa (eşik değerinin altında kalmışsa)
    if "hata" in sonuc:
        st.error(sonuc["hata"])
    
    # Başarılı eşleşme varsa
    else:
        st.success("Sizin için en uygun tahmini buldum!")
        
        # Sonuçları kutucuklar içinde şık bir şekilde gösterme
        st.markdown(f"**🔍 Eşleşen Belirti:** {sonuc['belirti']}")
        st.markdown(f"**⚠️ Olası Neden:** {sonuc['neden']}")
        st.markdown(f"**✅ Öneri:** {sonuc['oneri']}")
        st.caption(f"Yapay Zeka Benzerlik Skoru: %{int(sonuc['benzerlik_skoru'] * 100)}")
        
        # --- Takviyeli Öğrenme (Puanlama) Kısmı ---
        if not st.session_state.puanlandi:
            st.write("---")
            st.subheader("Bu tahmini nasıl değerlendirirsiniz?")
            st.write("Puanınız, sistemin gelecekteki tahminlerini iyileştirmek için kullanılacaktır.")
            
            # 5 adet yan yana yıldız butonu oluşturma
            cols = st.columns(5)
            for i in range(1, 6):
                # Butona basıldığında...
                if cols[i-1].button(f"{i} ⭐", key=f"star_{i}"):
                    # database.py'deki fonksiyonu çağırıp puanı veritabanına yaz
                    puan_ekle(sonuc["id"], i)
                    st.session_state.puanlandi = True # Puan verildi olarak işaretle
                    st.rerun() # Arayüzü güncellemek için sayfayı yeniden yükle
        else:
            # Puan verildikten sonra gösterilecek mesaj
            st.info("🌟 Geri bildiriminiz için teşekkürler! Veritabanı başarıyla güncellendi.")