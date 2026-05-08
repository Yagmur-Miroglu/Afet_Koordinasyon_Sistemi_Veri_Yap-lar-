# ADAKS - Afet ve Deprem Acil Yardım Koordinasyon Sistemi

## Projenin Amaci
ADAKS (Afet ve Deprem Acil Yardım Koordinasyon Sistemi), dogal afetler ve acil durumlar aninda kritik kaynaklarin, lojistik aglarin, gonullu yonetiminin ve arama-kurtarma ekiplerinin en verimli sekilde koordine edilmesini saglamak amaciyla gelistirilmis kapsamli bir masaustu uygulamasidir. Sistem, karmasik kriz anlarinda insan hatasini en aza indirmeyi, sinirli kaynaklari en cok ihtiyac duyulan bolgelere hizlica ulastirmayi ve saha operasyonlarini veriye dayali, analitik bir sekilde yonetmeyi hedefler.

## Nasil Calisir?
Sistem, arkaplanda calisan gelismis veri yapilari ve algoritmalar sayesinde sahadan gelen ihbarlari toplar, onceliklendirir ve merkez depolar ile enkaz bolgeleri arasindaki en optimal ag baglantilarini kurar. 

Kullanici arayuzu ana olarak 5 sekmeden olusur:
1. Saha Ihbar Formu: Sahadaki ekiplerin ihtiyaclarini ve durumlarini sisteme hizlica girdigi, otomatik tamamlama destekli form alanidir.
2. Lojistik ve Tedarik: Merkez depolarin anlik stok durumlarini ve tedarikci zincirlerini yoneten, azalan stoklari gosteren paneldir.
3. Harita ve Ihtiyaclar: Sehirdeki mevcut enkaz bolgeleri ve depolar arasindaki baglantiyi interaktif bir graf uzerinde gosteren, en kisa yol algoritmasini calistirarak araclari ve malzemeleri sevk eden sistemdir.
4. Gorev ve Gonullu Yonetimi: Sisteme kayitli gonullulerin uzmanlik alanlarina gore kuyruga alindigi ve sahadaki spesifik gorevlere atandigi moduldur.
5. Raporlama: Gerceklesmis tum islemlerin, sevkiyatlarin ve geri alinan adimlarin zaman damgali log kayitlarinin tutuldugu yonetici ekranidir.

## Temel Ozellikler
- Dinamik Harita Gorsellestirme: Depolar ve enkazlar arasi yol agini, mesafeleriyle birlikte gercek zamanli gosterir ve sevk edilen aracin rotasini cizer.
- Akilli En Yakin Depo Secimi: Bir enkaz bolgesi icin malzeme talebi karsilanmak istendiginde, sistem yalnizca elinde stok bulunan depolari tarar ve enkaza en kisa surede ulasabilecek depoyu otomatik atayarak rotayi cizer.
- Arac Durum Takibi: Goreve gonderilen araclar (Ambulans, Itfaiye, Is Makinesi vb.) listeden duserek "Gorevde" statune gecer, belirli bir sure sonra bakim asamasina (Cooldown) girer ve ardindan tekrar musait hale gelir.
- Uzmanlik Bazli Gonullu Atamasi: Olusturulan gorevlerin gerektirdigi uzmanlik tipine gore (ornegin Saglik/Tip), o alanda kayitli gonulluler sirasiyla (ilk gelen ilk cikar) goreve atanir.
- Geri Alma (Undo) Sistemi: Yapilan gorev atamalarinin ve operasyonlarin hatali olmasi durumunda islemi son yapilandan baslayarak geri alma imkani sunar.
- Hızlı Arama ve Filtreleme: On binlerce satir malzeme listesi arasinda aninda arama yapabilen otomatik tamamlama filtresi bulunur.

## Kullanilan Veri Yapilari ve Algoritmalar
Sistem performansini artirmak amaciyla modern bilgisayar bilimleri veri yapilari kullanilmistir:

1. Graf (Graph) Veri Yapisi ve Dijkstra Algoritmasi:
Sehir haritasi bir Ag (Network) olarak modellenmistir. Dugumler (Nodes) depolari ve enkazlari, Kenarlar (Edges) ise yollari temsil eder. Belirli bir enkaza malzeme gonderilecegi zaman, "Dijkstra En Kisa Yol" algoritmasi kullanilarak en az maliyetli/mesafeli rota hesaplanir.

2. Oncelik Kuyrugu (Priority Queue / Max-Heap):
Sahadan gelen ihbarlarin islenme sirasi gelis zamanina gore degil, "Kritiklik Seviyesi"ne gore belirlenir. Heap agaci kullanilarak, en yuksek oncelige sahip acil talepler her zaman listenin en basina alinir ve ilk once karsilanir.

3. Ikili Arama Agaci (Binary Search Tree - BST):
Lojistik depolarindaki binlerce farkli tur urunun (Ilac, Gida, Cadir vb.) envanter takibi ve stok arama islemleri icin BST kullanilir. Bu yapi sayesinde yeni urun ekleme, silme ve arama islemleri O(log N) karmasikliginda, cok yuksek hizlarda gerceklestirilir.

4. On Ek Agaci (Trie):
Ihbar formu doldurulurken kullanicinin yazdigi her harfte, sistemdeki mevcut binlerce ihtiyac listesinden eslesme yapan otomatik tamamlama ozelligi (Autocomplete) Trie veri yapisi uzerine insa edilmistir.

5. Kuyruk (Queue / Strict FIFO):
Gonullu yonetimi ve saha ekiplerinin siralanmasi islemleri "Ilk Giren Ilk Cikar" prensibiyle kuyruklar uzerinden yonetilir. Her uzmanlik alani (Saglik, Lojistik, Kurtarma) icin ayri bagimsiz kuyruklar kullanilir.

6. Yigin (Stack / LIFO):
Kullanicinin yaptigi kritik atamalari ve yonetimsel kararlari hatirlamak, "Geri Al" (Undo) butonuna basildiginda en son yapilan islemi tespit edip iptal edebilmek amaciyla "Son Giren Ilk Cikar" mantigiyla calisan Stack veri yapisi kullanilmistir.

7. Hash Haritalari (Dictionaries/Sets):
Birimlerin durumlarini (Gorevde/Musait/Bakimda), arac filosu takiplerini ve aktif loglarin saklanmasini O(1) sabit zaman karmasikligi ile gerceklestirmek icin Python'in yerlesik sozluk ve kume yapilari yogun olarak kullanilmistir.
