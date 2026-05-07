from dataclasses import dataclass, field

@dataclass(order=True)
class EkipTalebi:
    priority: int  # Heap sıralaması için en üstte
    talep_id: str = field(compare=False)
    ekip_adi: str = field(compare=False)
    adres: str = field(compare=False)
    kategori: str = field(compare=False)
    ihtiyac_adi: str = field(compare=False)
    miktar: int = field(compare=False)
    durum: str = field(compare=False)
    kaynak_depo: str = field(compare=False, default="") 

@dataclass
class Urun:
    urun_id: int
    ad: str
    kategori: str
    miktar: int

@dataclass
class MudahaleLog:
    log_id: int
    mesaj: str
    zaman_damgasi: str

@dataclass
class Gorev:
    gorev_id: str
    baslik: str
    aciklama: str
    durum: str
    gereken_uzmanlik: str = ""
    kisi_sayisi: int = 1
    atanan_kisiler: str = ""

@dataclass
class Gonullu:
    kimlik: str
    ad_soyad: str
    kategori: str