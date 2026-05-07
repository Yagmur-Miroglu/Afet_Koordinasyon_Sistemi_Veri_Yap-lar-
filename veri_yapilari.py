class TrieDugumu:
    def __init__(self):
        self.cocuklar = {}
        self.kelime_sonu_mu = False

class GenelTrie:
    def __init__(self):
        self.kok = TrieDugumu()

    def ekle(self, metin):
        aktif = self.kok
        for harf in metin.lower():
            if harf not in aktif.cocuklar:
                aktif.cocuklar[harf] = TrieDugumu()
            aktif = aktif.cocuklar[harf]
        aktif.kelime_sonu_mu = True

    def oneri_getir(self, on_ek):
        aktif = self.kok
        on_ek = on_ek.lower()
        for harf in on_ek:
            if harf not in aktif.cocuklar: return []
            aktif = aktif.cocuklar[harf]
        
        sonuclar = []
        self._kelimeleri_bul(aktif, on_ek, sonuclar)
        return sonuclar

    def _kelimeleri_bul(self, dugum, anlik_kelime, sonuclar):
        if dugum.kelime_sonu_mu: sonuclar.append(anlik_kelime)
        for harf, cocuk_dugum in dugum.cocuklar.items():
            self._kelimeleri_bul(cocuk_dugum, anlik_kelime + harf, sonuclar)

class BagliListeDugumu:
    def __init__(self, veri):
        self.veri = veri
        self.sonraki = None

class LogBagliListe:
    def __init__(self):
        self.bas = None
    def basa_ekle(self, veri):
        yeni_dugum = BagliListeDugumu(veri)
        yeni_dugum.sonraki = self.bas
        self.bas = yeni_dugum
    def listele(self):
        sonuclar, aktif = [], self.bas
        while aktif:
            sonuclar.append(aktif.veri)
            aktif = aktif.sonraki
        return sonuclar

class BSTAgaçDugumu:
    def __init__(self, urun):
        self.urun = urun
        self.sol = None
        self.sag = None

class EnvanterBST:
    def __init__(self):
        self.kok = None
    def ekle(self, urun):
        if self.kok is None: self.kok = BSTAgaçDugumu(urun)
        else: self._ekle_rekursif(self.kok, urun)
    def _ekle_rekursif(self, dugum, urun):
        if urun.ad < dugum.urun.ad:
            if dugum.sol is None: dugum.sol = BSTAgaçDugumu(urun)
            else: self._ekle_rekursif(dugum.sol, urun)
        elif urun.ad > dugum.urun.ad:
            if dugum.sag is None: dugum.sag = BSTAgaçDugumu(urun)
            else: self._ekle_rekursif(dugum.sag, urun)
        else: dugum.urun.miktar += urun.miktar
    def inorder_gezin(self, dugum, liste):
        if dugum:
            self.inorder_gezin(dugum.sol, liste)
            liste.append(dugum.urun)
            self.inorder_gezin(dugum.sag, liste)
    def tum_urunler(self):
        liste = []
        self.inorder_gezin(self.kok, liste)
        return liste
    def miktar_azalt(self, urun_adi, miktar):
        dugum = self._dugum_bul(self.kok, urun_adi)
        if dugum and dugum.urun.miktar >= miktar:
            dugum.urun.miktar -= miktar
            return True
        return False
    def _dugum_bul(self, dugum, urun_adi):
        if dugum is None: return None
        if urun_adi == dugum.urun.ad: return dugum
        if urun_adi < dugum.urun.ad: return self._dugum_bul(dugum.sol, urun_adi)
        return self._dugum_bul(dugum.sag, urun_adi)
    
    # veri_yapilari.py içindeki EnvanterBST sınıfına ekle:
    def sil(self, urun_adi):
        self.kok = self._sil_rekursif(self.kok, urun_adi)

    def _sil_rekursif(self, dugum, urun_adi):
        if dugum is None: return None
        
        if urun_adi < dugum.urun.ad:
            dugum.sol = self._sil_rekursif(dugum.sol, urun_adi)
        elif urun_adi > dugum.urun.ad:
            dugum.sag = self._sil_rekursif(dugum.sag, urun_adi)
        else:
            # Tek çocuklu veya çocuksuz düğüm
            if dugum.sol is None: return dugum.sag
            elif dugum.sag is None: return dugum.sol
            
            # İki çocuklu düğüm: Sağ alt ağaçtaki en küçük değeri bul
            gecici = self._min_deger_dugumu(dugum.sag)
            dugum.urun = gecici.urun
            dugum.sag = self._sil_rekursif(dugum.sag, gecici.urun.ad)
        return dugum

    def _min_deger_dugumu(self, dugum):
        aktif = dugum
        while aktif.sol is not None:
            aktif = aktif.sol
        return aktif

class Yigin:
    def __init__(self): self.yigin = []
    def push(self, islem): self.yigin.append(islem)
    def pop(self): return self.yigin.pop() if not self.bos_mu() else None
    def bos_mu(self): return len(self.yigin) == 0

class Kuyruk:
    def __init__(self): self.kuyruk = []
    def enqueue(self, kisi): self.kuyruk.append(kisi)
    def dequeue(self): return self.kuyruk.pop(0) if not self.bos_mu() else None
    def bos_mu(self): return len(self.kuyruk) == 0
    def boyut(self): return len(self.kuyruk)

class SabitDizi:
    def __init__(self, kapasite):
        self.kapasite = kapasite
        self.dizi = [None] * kapasite
    def eleman_ata(self, indeks, veri):
        if 0 <= indeks < self.kapasite: self.dizi[indeks] = veri
    def eleman_getir(self, indeks):
        if 0 <= indeks < self.kapasite: return self.dizi[indeks]
        return None