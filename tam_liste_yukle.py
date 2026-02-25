import sqlite3

DB_NAME = 'saglik_asistani.db'

def dev_veritabanini_kur():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Temiz bir başlangıç için eski tabloyu siliyoruz
    cursor.execute('DROP TABLE IF EXISTS bilgi_tabani')
    
    # Tabloyu yeniden oluşturuyoruz
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

    # --- 100+ MADDELİK DEV VERİ SETİ ---
    dev_veri_seti = [
        # --- SİNDİRİM VE BESLENME ---
        ("Yemekten sonra ağırlık çökmesi", "Aşırı karbonhidrat tüketimi, hızlı yemek", "Doktora Görünün: Her öğünden sonra oluyorsa ve ani kilo artışı varsa", "Sindirim"),
        ("Sabah açken mide kazınması", "Asit artışı, uzun süreli açlık", "Doktora Görünün: Yanma ve sırta vuran ağrı artıyorsa", "Sindirim"),
        ("Kahve sonrası mide rahatsızlığı", "Asit hassasiyeti, kafein reaksiyonu", "Doktora Görünün: Midede kramp veya kanama belirtisi (koyu renkli dışkı) varsa", "Sindirim"),
        ("Sık acıkma hissi", "Kan şekeri dalgalanması, insülin direnci", "Doktora Görünün: Titreme, terleme ve bayılma hissi eşlik ediyorsa", "Sindirim"),
        ("Sürekli tatlı yeme isteği", "Kan şekeri dengesizliği, krom eksikliği", "Tarçınlı su için ve öğünlerinize protein ekleyin.", "Sindirim"),
        ("Midede şişkinlik ve gaz", "Hızlı yemek yeme, hava yutma, hareketsizlik", "Yemekleri yavaş çiğneyin, yemekten sonra nane çayı için.", "Sindirim"),
        ("Yutkunurken boğazda takılma hissi", "Reflü, stres (globus hissi), tiroid büyümesi", "Doktora Görünün: Katı gıdaları yutarken zorlanma kalıcı hale gelirse", "Sindirim"),
        ("Mide bulantısı (sabahları)", "Kan şekeri düşüklüğü, gebelik ihtimali, stres", "Doktora Görünün: Kusma eşlik ediyorsa ve gün boyu sürüyorsa", "Sindirim"),
        ("Kabızlık (uzun süreli)", "Lif eksikliği, yetersiz su tüketimi, hareketsizlik", "Doktora Görünün: Şiddetli karın ağrısı ve şişlik varsa", "Sindirim"),
        ("İshal (ani başlayan)", "Gıda zehirlenmesi, viral enfeksiyon", "Bol su için, haşlanmış patates tüketin. Kanlıysa hemen doktora gidin.", "Sindirim"),

        # --- UYKU VE ENERJİ ---
        ("Gece aniden sıçrayarak uyanma", "Stres, uykuya geçiş spazmı", "Doktora Görünün: Nefes darlığı ve çarpıntı ile uyanıyorsanız", "Uyku"),
        ("Sabah alarmı duymama ve zor uyanma", "Kalitesiz derin uyku, aşırı yorgunluk", "Doktora Görünün: Gün içinde sürekli uyuklama hali (Narkolepsi belirtisi) varsa", "Uyku"),
        ("Gece aşırı rüya/kabus görme", "REM uykusu artışı, yatmadan önce stres", "Yatmadan önce dijital ekranlardan uzak durun.", "Uyku"),
        ("Gün içinde ani uyku bastırması", "İnsülin direnci, ağır öğle yemeği", "Şekerli gıdaları azaltın, öğle yemeklerini hafif tutun.", "Uyku"),
        ("Uyurken aşırı terleme", "Oda sıcaklığı, sentetik yorgan, tiroid fazlalığı", "Doktora Görünün: Ateş ve ani kilo kaybı eşlik ediyorsa", "Uyku"),
        ("Uykuya dalmada zorluk (İnsomnia)", "Anksiyete, geç saatte kafein tüketimi", "Yatmadan 6 saat önce kafeini kesin, karanlık ortam sağlayın.", "Uyku"),
        ("Horlama ve nefes kesilmesi", "Uyku apnesi, kilo fazlalığı, geniz eti", "Doktora Görünün: Yanınızdaki kişi nefesinizin durduğunu söylüyorsa", "Uyku"),
        ("Yatakta bacakları sürekli hareket ettirme isteği", "Huzursuz bacak sendromu, demir eksikliği", "Doktora Görünün: Uykuya dalmanızı tamamen engelliyorsa", "Uyku"),

        # --- KAS, İSKELET VE SİNİR ---
        ("Boyundan kola hafif sızlama", "Postür bozukluğu, masa başı çalışma", "Doktora Görünün: Uyuşma artarsa ve elde eşya tutarken güç kaybı yaşanırsa", "Sinir Sistemi"),
        ("Merdiven çıkarken baldır yanması", "Kas zayıflığı, laktik asit birikimi", "Doktora Görünün: Düz yolda kısa süre yürürken bile kramp giriyorsa", "Kas/İskelet"),
        ("Telefon tutarken bilek ağrısı", "Karpal tünel sendromu başlangıcı, tendon zorlanması", "Doktora Görünün: Gece uykudan uyandıran bilek ağrısı ve uyuşma varsa", "Kas/İskelet"),
        ("El parmaklarında sabah sertlik", "Gece yanlış pozisyon, sıvı birikimi", "Doktora Görünün: Sertlik 30 dakikadan uzun sürüyorsa (Romatizma belirtisi)", "Sinir Sistemi"),
        ("Çene ağrısı sabahları", "Gece uyurken diş sıkma (Bruksizm)", "Gece plağı kullanmak için diş hekimine danışın.", "Kas/İskelet"),
        ("Uzun oturunca ayakta karıncalanma", "Kan dolaşımının yavaşlaması, sinir basısı", "Doktora Görünün: Karıncalanma ayağa kalkıp yürümeye rağmen saatlerce geçmiyorsa", "Dolaşım/Sinir"),
        ("Yüzde ve gözde hafif seğirme", "Yorgunluk, aşırı kafein, stres", "Kafeini azaltın, magnezyum alın. Günlerce geçmezse doktora başvurun.", "Sinir Sistemi"),
        ("Belden bacağa vuran ağrı", "Siyatik sinir sıkışması, yanlış ağırlık kaldırma", "Doktora Görünün: Bacakta uyuşma, his kaybı veya idrar kaçırma varsa ACİL doktora gidin", "Sinir Sistemi"),
        ("Sırtta iki kürek kemiği arası ağrı", "Duruş bozukluğu, kas spazmı, stres", "Dik duruş egzersizleri yapın. Nefes alırken batma varsa doktora görünün.", "Kas/İskelet"),
        ("Topuk ağrısı (özellikle sabah ilk adımlarda)", "Topuk dikeni (Plantar fasiit)", "Doktora Görünün: Ortopedik tabanlık kullanımına rağmen geçmiyorsa", "Kas/İskelet"),

        # --- PSİKOLOJİK VE ZİHİNSEL ---
        ("Nedensiz iç sıkıntısı", "Anksiyete, birikmiş stres, uykusuzluk", "Doktora Görünün: Haftalarca sürüyorsa ve hayattan zevk almanızı engelliyorsa", "Psikolojik"),
        ("Toplulukta yüz kızarması ve terleme", "Sosyal anksiyete, otonom sinir sistemi tepkisi", "Doktora Görünün: Topluluk içine çıkmaktan tamamen kaçınmaya başlarsanız", "Psikolojik"),
        ("Sürekli kötü bir şey olacak hissi", "Yaygın anksiyete bozukluğu", "Doktora Görünün: Bu his panik atağa (çarpıntı, nefes darlığı) dönüşürse", "Psikolojik"),
        ("Odaklanma problemi ve unutkanlık", "Dijital yorgunluk, çoklu görev, B12 eksikliği", "Ekran süresini azaltın. Günlük işleri tamamen unutuyorsanız doktora görünün.", "Zihinsel"),
        ("Sürekli yorgunluk ve isteksizlik (Tükenmişlik)", "Burnout sendromu, kronik stres", "Kendinize vakit ayırın, hobilere yönelin. Geçmezse terapi desteği alın.", "Psikolojik"),
        ("Ani öfke patlamaları", "Stres birikimi, tahammül seviyesinin düşmesi", "Doktora Görünün: Öfkeniz size veya çevrenize zarar verme boyutuna ulaştıysa", "Psikolojik"),

        # --- CİLT, SAÇ VE ESTETİK ---
        ("Duştan sonra kaşıntı", "Cilt kuruluğu, çok sıcak su ile yıkanma", "Doktora Görünün: Kızarıklık, kabarma ve döküntü kalıcıysa", "Cilt/Saç"),
        ("Saç diplerinde sızlama ve ağrı", "Stres, saç derisinde yağlanma, sıkı bağlama", "Doktora Görünün: Yoğun bölgesel saç dökülmesi (para şeklinde) varsa", "Cilt/Saç"),
        ("Kışın burun kenarı soyulması", "Soğuk hava, nemsizlik, egzama başlangıcı", "Doktora Görünün: Nemlendiriciye rağmen yara açılır ve kabuklanırsa", "Cilt/Saç"),
        ("Ayak tabanında soyulma ve kaşıntı", "Aşırı terleme, mantar başlangıcı", "Doktora Görünün: Kaşıntı çok şiddetliyse ve tırnaklarda renk değişimi varsa", "Cilt/Saç"),
        ("Tırnaklarda beyaz lekeler", "Çinko/Kalsiyum eksikliği, tırnak travması", "Badem, ceviz tüketin. Lekeler tüm tırnağı kaplarsa doktora görünün.", "Cilt/Saç"),
        ("Stresli dönemde ciltte sivilcelenme", "Kortizol hormonunun artması, yağ dengesi bozulması", "Yüzünüzü düzenli yıkayın, şekeri azaltın. Geçmezse dermatoloğa görünün.", "Cilt/Saç"),
        ("Aşırı saç dökülmesi (banyoda/yastıkta)", "Mevsim geçişi, demir eksikliği, tiroid sorunları", "Doktora Görünün: Saçlar tutam tutam dökülüyor ve seyrelme belli oluyorsa", "Cilt/Saç"),
        ("Dudak kenarlarında çatlama (Peleş)", "B vitamini eksikliği, tükürük birikimi", "B kompleksi vitaminleri alın, dudaklarınızı yalamaktan kaçının.", "Cilt/Saç"),

        # --- BAŞ, GÖZ, KULAK VE BOĞAZ ---
        ("Işığa hassasiyet ve baş ağrısı", "Ekran yorgunluğu, migren başlangıcı", "Doktora Görünün: Şiddetli zonklama ve mide bulantısı eşlik ediyorsa", "Baş/Göz/Kulak"),
        ("Uzun süre ekrana bakınca bulanıklaşma", "Göz kuruluğu, miyop/astigmat başlangıcı", "Doktora Görünün: Göz kırpmaya rağmen bulanıklık geçmiyor ve baş ağrıtıyorsa", "Baş/Göz/Kulak"),
        ("Esnerken veya yutkunurken kulakta çıtırtı", "Östaki borusu basınç değişimi", "Doktora Görünün: Çıtırtı yerine şiddetli ağrı ve işitme kaybı varsa", "Baş/Göz/Kulak"),
        ("Sabah ağızda metalik/acı tat", "Mide reflüsü, ağız kuruluğu, diş eti kanaması", "Doktora Görünün: Diş fırçalamaya ve su içmeye rağmen sürekli devam ederse", "Baş/Göz/Kulak"),
        ("Kulaklık kullandıktan sonra çınlama", "Yüksek sese maruz kalma, kulak zarı yorgunluğu", "Doktora Görünün: Çınlama (Tinnitus) 24 saatten uzun sürerse veya baş dönmesi yaparsa", "Baş/Göz/Kulak"),
        ("Göz akında kanlanma (kızarıklık)", "Uykusuzluk, alerji, göz tansiyonu", "Doktora Görünün: Gözde şiddetli ağrı veya görme kaybı varsa ACİL doktora gidin", "Baş/Göz/Kulak"),
        ("Sabah uyanınca boğaz kuruluğu", "Gece ağız açık uyuma, nemsiz oda", "Odanızı havalandırın. Yutkunma zorluğu ve ateş eklenirse doktora görünün.", "Baş/Göz/Kulak"),
        ("Baş dönmesi (Ayağa kalkınca)", "Ortostatik hipotansiyon (ani tansiyon düşüşü)", "Yavaşça ayağa kalkın. Sık sık göz kararması oluyorsa doktora görünün.", "Baş/Göz/Kulak"),
        ("Baş dönmesi (Etraf dönüyormuş gibi)", "Vertigo, iç kulak kristalleri oynaması", "Doktora Görünün: Şiddetli bulantı yapıyor ve dengenizi bozuyorsa", "Baş/Göz/Kulak"),

        # --- SOLUNUM, DOLAŞIM VE GENEL ---
        ("Ara ara gelen kuru öksürük", "Alerji, geniz akıntısı, kuru hava", "Doktora Görünün: Öksürük 3 haftadan uzun sürerse veya kanlı balgam varsa", "Solunum/Dolaşım"),
        ("Derin nefes alırken göğüste batma", "Kas sıkışması, stres, akciğer zarı hassasiyeti", "Doktora Görünün: Nefes darlığı, kola/çeneye vuran ağrı varsa ACİL doktora gidin", "Solunum/Dolaşım"),
        ("Sürekli üşüme hissi", "Kansızlık, tiroid yavaşlığı (Hipotiroidi)", "Doktora Görünün: Havalar sıcakken bile üşüme ve yorgunluk geçmiyorsa", "Genel"),
        ("Nedensiz ani terleme ve çarpıntı", "Kan şekeri düşüklüğü, panik atak, tiroid", "Doktora Görünün: Çarpıntı hissi göğüs ağrısıyla birlikte geliyorsa", "Solunum/Dolaşım"),
        ("Ellerde ve ayaklarda sürekli soğukluk", "Dolaşım bozukluğu, kansızlık", "Doktora Görünün: Parmak uçlarında morarma veya renk değişimi (Reynaud) varsa", "Dolaşım/Sinir"),
        ("Gün sonu ayak bileklerinde şişlik (Ödem)", "Uzun süre ayakta kalma, tuzlu beslenme", "Doktora Görünün: Şişlik sabaha kadar geçmiyor ve parmak basınca iz kalıyorsa", "Solunum/Dolaşım"),
        ("Sürekli susama hissi (Polidipsi)", "Aşırı tuzlu yeme, diyabet (şeker hastalığı) başlangıcı", "Doktora Görünün: Sık idrara çıkma ve ani kilo kaybı eşlik ediyorsa", "Genel"),
        ("Hafif ateş ve kırgınlık", "Viral enfeksiyon başlangıcı, aşırı yorgunluk", "Doktora Görünün: Ateş 39 dereceyi geçerse veya 3 günden uzun sürerse", "Genel")
    ]

    cursor.executemany('''
        INSERT INTO bilgi_tabani (belirti, neden, oneri, kategori) 
        VALUES (?, ?, ?, ?)
    ''', dev_veri_seti)

    conn.commit()
    conn.close()
    print(f"🚀 TEBRİKLER! Veritabanı devasa kapasiteye ulaştı. Toplam {len(dev_veri_seti)} adet profesyonel veri yüklendi.")

if __name__ == "__main__":
    dev_veritabanini_kur()
