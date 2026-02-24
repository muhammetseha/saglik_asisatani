import sqlite3

DB_NAME = 'saglik_asistani.db'

def tam_kapasite_doldur():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Eski tabloyu temizle ve sıfırdan oluştur
    cursor.execute('DROP TABLE IF EXISTS bilgi_tabani')
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

    # Tam Kapasite Veri Seti (Tez için özenle kategorize edilmiştir)
    dev_liste = [
        # --- UYKU VE YORGUNLUK ---
        ("Sabah yorgun uyanmak", "Uyku kalitesinin düşüklüğü veya geç yatma.", "Yatmadan 3 saat önce yemeyi kesin, aynı saatte uyumaya çalışın.", "Uyku"),
        ("Gece sık uyanmak", "Odadaki ışık/ses kirliliği veya akşam içilen sıvılar.", "Karanlık ve sessiz bir ortam sağlayın, sıvı alımını azaltın.", "Uyku"),
        ("Gece terlemesi", "Sentetik çarşaflar veya odanın aşırı sıcak olması.", "Pamuklu pijama kullanın, oda sıcaklığını 18-20 derece yapın.", "Uyku"),
        ("Uyumakta zorlanmak", "Mavi ışığa maruz kalma (telefon/TV) veya zihinsel meşguliyet.", "Yatmadan 1 saat önce ekran kullanımını bırakın.", "Uyku"),
        ("Sabah baş ağrısı ile uyanmak", "Diş sıkma (bruksizm) veya havasız oda.", "Odayı iyice havalandırın, geçmezse diş hekimine danışın.", "Uyku"),
        ("Çok uyumama rağmen yorgunluk", "Uyku apnesi veya kalitesiz derin uyku evresi.", "Uyku düzeninizi sabitleyin, horlama varsa uzman yardımı alın.", "Uyku"),
        ("Uyku sırasında ağız açık kalması", "Burun tıkanıklığı veya yanlış yastık seçimi.", "Burun bandı deneyin veya yastık yüksekliğini ayarlayın.", "Uyku"),
        ("Rüya görerek sık uyanma", "REM uykusunun bölünmesi veya ağır akşam yemeği.", "Akşam yemeklerini hafifletin, stresten uzaklaşın.", "Uyku"),
        ("Horlama", "Sırt üstü yatış pozisyonu veya fazla kilo.", "Yan yatmayı deneyin ve yüksek yastık kullanın.", "Uyku"),
        ("Uykuda diş sıkma", "Günlük stres ve kaygı birikimi.", "Yatmadan önce gevşeme egzersizleri (meditasyon) yapın.", "Uyku"),
        ("Gece bacak huzursuzluğu", "Uzun süre hareketsiz kalma veya magnezyum eksikliği.", "Yatmadan önce bacaklara hafif masaj veya esneme yapın.", "Uyku"),
        
        # --- SİNDİRİM VE MİDE ---
        ("Şişkinlik", "Gaz yapan gıdalar (baklagiller) veya hızlı yemek.", "Yemekleri yavaş çiğneyin, rezene veya papatya çayı deneyin.", "Sindirim"),
        ("Gaz problemi", "Hareketsizlik veya laktoz hassasiyeti.", "Yemekten sonra 15 dakikalık kısa yürüyüşler yapın.", "Sindirim"),
        ("Yemekten sonra mide yanması", "Mide asidinin yükselmesi (Reflü başlangıcı).", "Yemekten hemen sonra uzanmayın, porsiyonları küçültün.", "Sindirim"),
        ("Sabah mide bulantısı", "Uzun süreli açlık veya akşamki ağır yemekler.", "Sabahları tuzlu bir kraker veya leblebi atıştırın.", "Sindirim"),
        ("Kabızlık", "Lifli gıda eksikliği veya yetersiz su tüketimi.", "Kuru kayısı, incir gibi lifli gıdalar tüketin, bol su için.", "Sindirim"),
        ("İshal (hafif)", "Bozulmuş gıda, üşütme veya aşırı meyve tüketimi.", "Haşlanmış patates ve muz tüketin, bol su içerek sıvı açığını kapatın.", "Sindirim"),
        ("Sürekli geğirme", "Yemek yerken hava yutma veya asitli içecekler.", "Sessiz ve yavaş yemek yiyin, gazlı içecekleri bırakın.", "Sindirim"),
        ("Karında guruldama", "Açlık veya sindirim sisteminin aktif çalışması.", "Düzenli öğünlerle beslenin, aşırı kafeinden kaçının.", "Sindirim"),
        ("Hazımsızlık", "Yağlı/baharatlı yiyecekler veya stres.", "Öğünleri küçültün, nane çayı içerek mideyi rahatlatın.", "Sindirim"),
        ("Yemekten sonra uyku basması", "Kan şekerinin ani yükselmesi (İnsülin tepkisi).", "Karbonhidratı azaltıp protein dengesine dikkat edin.", "Sindirim"),
        ("Stres kaynaklı mide ağrısı", "Duygusal gerginliğin sindirim sistemine etkisi.", "Nefes egzersizleri yapın, ılık bitki çayları tüketin.", "Sindirim"),

        # --- AĞIZ, BOĞAZ VE BURUN ---
        ("Sabah ağız kokusu", "Gece azalan tükürük salgısı ve bakteri birikimi.", "Dilinizi de fırçalayın ve akşamdan ağız gargarası yapın.", "Ağız/Boğaz"),
        ("Dil üzerinde beyaz tabaka", "Ağız florasının bozulması veya susuzluk.", "Dil temizleyici aparat kullanın ve su tüketimini artırın.", "Ağız/Boğaz"),
        ("Ağız kuruluğu", "Ağızdan nefes alma veya tuzlu akşam yemeği.", "Yatmadan önce su için ve burundan nefes almaya odaklanın.", "Ağız/Boğaz"),
        ("Boğazda gıcık hissi", "Kuru hava veya hafif geniz akıntısı.", "Bulunduğunuz odayı nemlendirin, ılık ballı su tüketin.", "Ağız/Boğaz"),
        ("Yutkunurken hafif ağrı", "Boğaz kuruluğu veya soğuk içecek tüketimi.", "Tuzlu su ile gargara yapın ve boğazınızı sıcak tutun.", "Ağız/Boğaz"),
        ("Diş eti kanaması", "Sert fırçalama veya diş taşı birikimi.", "Yumuşak fırça kullanın ve diş ipi alışkanlığı edinin.", "Ağız/Boğaz"),
        ("Ağız içinde aft çıkması", "Bağışıklık düşüklüğü veya sert yiyecek tahrişi.", "B vitamini içeren gıdalar tüketin, asitli içeceklerden kaçının.", "Ağız/Boğaz"),
        ("Sürekli susama hissi", "Aşırı tuzlu beslenme veya şekerli içecek tüketimi.", "Saf su tüketimini artırın, tuzu ve şekeri azaltın.", "Ağız/Boğaz"),
        ("Boğazda balgam hissi", "Sigara dumanı, alerji veya süt ürünleri tüketimi.", "Bol ılık su için, bulunduğunuz ortamı sık sık havalandırın.", "Ağız/Boğaz"),
        ("Sabah burun tıkanıklığı", "Toz akarlarına karşı alerji veya kuru hava.", "Yastık kılıflarını sık değiştirin ve odayı nemlendirin.", "Ağız/Boğaz"),
        ("Sürekli hapşırma", "Ev tozu, polen veya hayvan tüyü duyarlılığı.", "Ortamı sık havalandırın ve tozlu yerlerden kaçının.", "Ağız/Boğaz"),

        # --- KAS, EKLEM VE İSKELET ---
        ("Boyun tutulması", "Yanlış yatış pozisyonu, ters hareket veya klima çarpması.", "Boyun bölgenizi sıcak tutun ve hafif esneme hareketleri yapın.", "Kas/Eklem"),
        ("Bel ağrısı (hafif)", "Uzun süre yanlış pozisyonda oturma.", "Bel desteği kullanın ve her saat başı ayağa kalkıp gerinin.", "Kas/Eklem"),
        ("Diz çıtırtısı", "Hareketsizlik sonucu eklem sıvısının yer değiştirmesi.", "Dizleri zorlamayan basit egzersizler ve yürüyüş yapın.", "Kas/Eklem"),
        ("Kas seğirmesi", "Magnezyum eksikliği, aşırı kafein veya yorgunluk.", "Muz ve kuruyemiş gibi mineralli gıdalar tüketin, dinlenin.", "Kas/Eklem"),
        ("Sabah eklem sertliği", "Gece boyunca hareketsiz kalma veya hafif kireçlenme.", "Sabahları yatakta 5 dakika hafif esneme ve gerinme yapın.", "Kas/Eklem"),
        ("Omuz ağrısı", "Ağır çanta taşıma, stres veya masa başı çalışma.", "Dik durmaya çalışın, omuzları geriye doğru çevirerek rahatlatın.", "Kas/Eklem"),
        ("Ayakta yanma hissi", "Sinir sıkışması, yorgunluk veya yanlış ayakkabı.", "Ayaklarınızı ılık suda dinlendirin, rahat ayakkabılar seçin.", "Kas/Eklem"),
        ("El uyuşması (kısa süreli)", "Sinir sıkışması (karpal tünel) veya yanlış uyuma pozisyonu.", "El bileği egzersizleri yapın, klavye kullanırken bilek desteği alın.", "Kas/Eklem"),
        ("Bacak krampı", "Mineral (Potasyum/Magnezyum) kaybı veya kas yorgunluğu.", "Bol su için, esneme yapın ve potasyum içeren gıdalar tüketin.", "Kas/Eklem"),
        ("Spor sonrası kas ağrısı", "Kaslarda laktik asit birikimi (Gecikmiş kas ağrısı).", "Hafif tempolu yürüyüş yapın, protein alın ve sıcak duş alın.", "Kas/Eklem"),

        # --- ZİHİNSEL VE GENEL DURUM ---
        ("Sürekli halsizlik", "Yetersiz sıvı tüketimi (dehidrasyon), kansızlık veya hareketsizlik.", "Günlük su tüketiminizi artırın ve kan değerlerinize baktırın.", "Genel"),
        ("Baş dönmesi (hafif)", "Ani ayağa kalkma, uzun süre aç kalma veya tansiyon oynaması.", "Pozisyon değiştirirken yavaş hareket edin, öğün atlamayın.", "Genel"),
        ("Ani göz kararması", "Ortostatik hipotansiyon (ani tansiyon düşüşü) veya açlık.", "Oturur pozisyondan yavaşça ayağa kalkın, ani hareketlerden kaçının.", "Genel"),
        ("El titremesi", "Aşırı kafein alımı, kan şekeri düşüklüğü veya yoğun heyecan.", "Kahve tüketimini sınırlayın ve düzenli aralıklarla beslenin.", "Genel"),
        ("Odaklanma problemi", "Dijital yorgunluk, çoklu görev (multitasking) veya düzensiz uyku.", "25 dk çalışma 5 dk mola (Pomodoro) tekniğini uygulayın.", "Zihinsel"),
        ("Beyin sisi (brain fog)", "Zihinsel aşırı yüklenme, B12 eksikliği veya kronik yorgunluk.", "Ekran süresini azaltın, açık havada vakit geçirin ve ceviz tüketin.", "Zihinsel"),
        ("Çabuk yorulma", "Düşük kondisyon, demir eksikliği veya kalitesiz uyku.", "Günlük hareket miktarını kademeli olarak artırın (örn. merdiven çıkma).", "Genel"),
        ("Hafif çarpıntı hissi", "Yoğun kaygı, stres, panik veya aşırı çay/kahve tüketimi.", "Sakinleşmek için derin nefes alın ve uyarıcı içecekleri kesin.", "Genel"),
        ("Soğuk el ve ayaklar", "Düşük kan dolaşımı, hareketsizlik veya kansızlık belirtisi.", "Kan dolaşımı için hareket edin, sıkı giyinin ve sıcak içecekler tüketin.", "Genel"),
        ("Kulak çınlaması (geçici)", "Yüksek sese maruz kalma, stres veya kan basıncı değişimi.", "Sessiz bir ortamda dinlenin, yüksek sesli kulaklık kullanımını bırakın.", "Genel"),
        ("Göz seğirmesi", "Göz yorgunluğu, aşırı ekran kullanımı, uykusuzluk veya stres.", "Ekrana bakmaya ara verin, gözlerinizi kapatıp dinlendirin.", "Göz"),
        ("Aşırı esneme ihtiyacı", "Ortamda oksijen azlığı, sıkıntı veya uyku eksikliği.", "Bulunduğunuz ortamı havalandırın ve derin, temiz nefesler alın.", "Genel"),
        ("Gün içinde ani üşüme", "Kan şekerinin düşmesi, yorgunluk veya ince giyinme.", "Sıcak bir bitki çayı için ve enerjinizi dengeleyecek bir atıştırmalık yiyin.", "Genel"),

        # --- CİLT, SAÇ VE TIRNAK ---
        ("Ani sivilce çıkması", "Yüksek şekerli/yağlı beslenme, stres veya kirli yastık kılıfı.", "Yüzünüzü uygun temizleyiciyle yıkayın, şekeri azaltın.", "Cilt/Saç"),
        ("Ciltte kaşıntı", "Cilt kuruluğu, sıcak suyla duş veya deterjan alerjisi.", "Duştan sonra parfümsüz nemlendiriciler kullanın, ılık suyla yıkanın.", "Cilt/Saç"),
        ("Ellerde kuruluk", "Sık sabun kullanımı, soğuk hava veya kimyasal teması.", "Ellerinizi yıkadıktan sonra nemlendirici krem sürün, soğukta eldiven takın.", "Cilt/Saç"),
        ("Dudak çatlaması", "Soğuk hava, nemsizlik veya dudakları yalama alışkanlığı.", "Dudak nemlendiricisi (balm) kullanın ve bol su için.", "Cilt/Saç"),
        ("Saç dökülmesi", "Mevsim geçişi, stres, vitamin eksikliği veya yanlış şampuan.", "Saç derisine masaj yapın, protein ve çinko ağırlıklı beslenin.", "Cilt/Saç"),
        ("Kepek problemi", "Saç derisinin kuruması, mantar veya saçları çok sık/seyrek yıkama.", "Ilık suyla yıkayın ve çinko pirition içeren şampuan seçin.", "Cilt/Saç"),
        ("Tırnak kırılması", "Kalsiyum/Biotin eksikliği, kimyasalla temas veya aşırı oje kullanımı.", "Temizlik yaparken eldiven kullanın, tırnakları dinlendirin.", "Cilt/Saç"),
        ("Ter kokusu artışı", "Baharatlı/sarımsaklı beslenme veya sentetik kıyafetler.", "Pamuklu kıyafet seçin, bol su için ve karbonatlı deodorantlar deneyin.", "Cilt/Saç")
    ]

    cursor.executemany('''
        INSERT INTO bilgi_tabani (belirti, neden, oneri, kategori) 
        VALUES (?, ?, ?, ?)
    ''', dev_liste)

    conn.commit()
    conn.close()
    print(f"BÜYÜK GÜNCELLEME TAMAMLANDI! {len(dev_liste)} adet hastalık/belirti veritabanına işlendi.")

if __name__ == "__main__":
    tam_kapasite_doldur()