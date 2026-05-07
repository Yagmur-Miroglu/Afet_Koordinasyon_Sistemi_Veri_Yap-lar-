import sys
import time
import networkx as nx
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from yonetici import SistemYoneticisi
from rota_gorsel import RotaGorsellestirici  
from performans import PerformansAnalizi  
from modeller import Urun, Gonullu   

class ModernAcikTema:
    STIL = """
    QMainWindow { background-color: #EBF2FA; } /* Soğuk Açık Mavi (Ice Blue) Arka Plan */
    QWidget { color: #1E293B; font-family: 'Segoe UI', Arial; font-size: 14px; }
    
    QTabWidget::pane { border: 1px solid #94A3B8; background: #FFFFFF; border-radius: 6px; }
    
    QTabBar::tab { 
        background: #D1D9E6; 
        color: #334155; 
        padding: 12px 30px; 
        border-top-left-radius: 6px; 
        border-top-right-radius: 6px; 
        margin-right: 2px; 
        border: 1px solid #94A3B8;
    }
    QTabBar::tab:selected { 
        background: #1E3A8A; /* Lacivert */
        color: #FFFFFF; 
        font-weight: bold; 
        border-bottom-color: #1E3A8A;
    }
    QTabBar::tab:hover:!selected {
        background: #B9C6D9;
    }

    QPushButton { 
        background-color: #1D4ED8; /* Koyu Mavi */
        color: white; 
        border: none; 
        padding: 10px; 
        border-radius: 6px; 
        font-weight: bold; 
    }
    QPushButton:hover { background-color: #1E3A8A; } /* Üzerine gelince Lacivert */
    QPushButton:pressed { background-color: #172554; }

    QLineEdit, QComboBox { 
        background-color: #FFFFFF; 
        color: #0F172A; 
        border: 1px solid #64748B; 
        padding: 8px; 
        border-radius: 5px; 
    }
    QLineEdit:focus, QComboBox:focus { border: 2px solid #1D4ED8; }

    QTableWidget { 
        background-color: #FFFFFF; 
        gridline-color: #CBD5E1; 
        border: 1px solid #94A3B8; 
        color: #1E293B; 
        selection-background-color: #DBEAFE;
        selection-color: #1E3A8A;
    }
    QHeaderView::section { 
        background-color: #1E3A8A; 
        color: white; 
        padding: 6px; 
        border: 1px solid #0F172A; 
        font-weight: bold; 
    }

    QListWidget { 
        background-color: #FFFFFF; 
        border: 1px solid #94A3B8; 
        border-radius: 5px; 
        color: #1E293B; 
    }
    QListWidget::item:selected { background-color: #DBEAFE; color: #1E3A8A; font-weight: bold; }

    QGroupBox { 
        border: 2px solid #1E3A8A; 
        border-radius: 8px; 
        margin-top: 15px; 
        font-weight: bold; 
        color: #1E3A8A; 
    }
    QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; }
    
    QScrollBar:vertical {
        border: none;
        background: #F1F5F9;
        width: 10px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #94A3B8;
        min-height: 20px;
        border-radius: 5px;
    }
    """

class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.yonetici = SistemYoneticisi()
        
        self.kategori_sozlugu = {
            "Arama Kurtarma Ekipmanı": ["Hilti", "Jeneratör", "Termal Kamera", "Enkaz Dinleme Cihazı", "Demir Kesme Makası", "Diğer"],
            "Barınma": ["Çadır (Kışlık)", "Konteyner", "Uyku Tulumu", "Isıtıcı (Elektrikli)", "Isıtıcı (Tüplü)", "Battaniye", "Mat", "Diğer"],
            "Gıda ve Su": ["Su (5 Lt)", "Konserve Gıda", "Bebek Maması", "Bebek Bisküvisi", "Ekmek", "Diğer"],
            "Sağlık ve İlk Yardım": ["İlk Yardım Çantası", "Sargı Bezi", "Ağrı Kesici", "Turnike", "Sedye", "Diğer"],
            "Hijyen": ["Bebek Bezi", "Kadın Pedi", "Islak Mendil", "Tuvalet Kağıdı", "Sabun", "Dezenfektan", "Diğer"],
            "Lojistik ve Enerji": ["Jeneratör", "El Feneri", "Pil", "Powerbank", "Aydınlatma Kulesi", "Diğer"],
            "Personel/Gönüllü": ["Arama Kurtarma Uzmanı", "Sağlık Personeli (Paramedik)", "Çevirmen", "Gönüllü (Lojistik)", "Psikososyal Destek Ekibi", "Diğer"],
            "Araç/İş Makinesi": ["Ekskavatör", "Vinç", "Ambulans", "İtfaiye Arazözü", "Kamyon", "Diğer"],
            "Diğer Kategori": ["Diğer"]
        }
        self.kategoriler = list(self.kategori_sozlugu.keys())
        self.aktif_ihtiyac_listesi = []

        self.init_ui()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.donenleri_kontrol_et)
        self.timer.start(2000)

    def init_ui(self):
        self.setWindowTitle("ADAKS - Kapsamlı Afet Koordinasyon Merkezi")
        self.setGeometry(50, 50, 1300, 850)
        self.setStyleSheet(ModernAcikTema.STIL)

        merkez_widget = QWidget()
        self.setCentralWidget(merkez_widget)
        ana_duzen = QVBoxLayout(merkez_widget)

        baslik = QLabel("ADAKS Koordinasyon Merkezi")
        baslik.setFont(QFont("Segoe UI", 22, QFont.Bold))
        baslik.setStyleSheet("color: #1E3A8A; margin-bottom: 10px;")
        baslik.setAlignment(Qt.AlignCenter)
        ana_duzen.addWidget(baslik)

        self.sekmeler = QTabWidget()
        ana_duzen.addWidget(self.sekmeler)

        self.sekme_saha_olustur()
        self.sekme_lojistik_olustur()
        self.sekme_harita_olustur()
        self.sekme_kaynak_gorev_olustur() 
        self.sekme_raporlama_olustur()

    def sekme_saha_olustur(self):
        sekme = QWidget()
        duzen = QHBoxLayout(sekme)

        sol_panel = QVBoxLayout()
        talep_grup = QGroupBox("Sahadaki Ekiplerden İhtiyaç İhbarı")
        talep_duzen = QVBoxLayout()
        
        self.ekip_cb = QComboBox()
        self.ekip_cb.setEditable(True)
        self.ekip_cb.lineEdit().setPlaceholderText("Ekip Seçiniz...")
        self.ekip_cb.addItems(self.yonetici.tum_ekipler)
        self.ekip_cb.setCurrentText("")
        self.ekip_cb.editTextChanged.connect(lambda t: self.trie_filtrele(t, self.ekip_cb, self.yonetici.tum_ekipler))
        
        self.kat_cb = QComboBox()
        self.kat_cb.setEditable(True)
        self.kat_cb.lineEdit().setPlaceholderText("Kategori Seçiniz...")
        self.kat_cb.addItems(self.kategoriler)
        self.kat_cb.setCurrentText("")
        self.kat_cb.currentTextChanged.connect(self.ihtiyac_seceneklerini_guncelle)
        self.kat_cb.editTextChanged.connect(lambda t: self.trie_filtrele(t, self.kat_cb, self.kategoriler))
        
        self.diger_ihtiyac_input = QLineEdit()
        self.diger_ihtiyac_input.setPlaceholderText("Lütfen özel ihtiyacı yazınız...")
        self.diger_ihtiyac_input.hide() 

        self.diger_oncelik_input = QLineEdit()
        self.diger_oncelik_input.setPlaceholderText("Manuel Öncelik Sırası (1: Kritik - 5: Normal)")
        self.diger_oncelik_input.hide() 

        self.ihtiyac_cb = QComboBox()
        self.ihtiyac_cb.setEditable(True)
        self.ihtiyac_cb.lineEdit().setPlaceholderText("İhtiyaç Seçiniz...")
        self.ihtiyac_cb.currentTextChanged.connect(self.diger_durumunu_kontrol_et)
        self.ihtiyac_seceneklerini_guncelle(self.kat_cb.currentText()) 
        self.ihtiyac_cb.setCurrentText("")
        self.ihtiyac_cb.editTextChanged.connect(lambda t: self.trie_filtrele(t, self.ihtiyac_cb, self.aktif_ihtiyac_listesi))
        
        self.talep_miktar = QLineEdit()
        self.talep_miktar.setPlaceholderText("Miktar (Örn: 10)")
        
        self.talep_adres = QComboBox()
        self.talep_adres.setEditable(True)
        self.talep_adres.lineEdit().setReadOnly(True)
        self.talep_adres.lineEdit().setPlaceholderText("Adres (Enkaz) Seçiniz...")
        enkaz_listesi = [dugum for dugum in self.yonetici.sehir_grafi.nodes if "Enkaz" in dugum]
        self.talep_adres.addItems(enkaz_listesi)
        self.talep_adres.setCurrentText("")
        
        btn_talep = QPushButton("Talebi Heap'e (Sıraya) Gönder")
        btn_talep.clicked.connect(self.talep_olustur_gui)

        btn_geri_al = QPushButton("Son Talebi Geri Al")
        btn_geri_al.setStyleSheet("background-color: #EF4444; color: white;")
        btn_geri_al.clicked.connect(self.talep_geri_al_gui)
        
        for w in [QLabel("Ekip Seçimi:"), self.ekip_cb, QLabel("Kategori:"), self.kat_cb, QLabel("İhtiyaç:"), self.ihtiyac_cb, 
                  self.diger_ihtiyac_input, self.diger_oncelik_input, QLabel("Miktar:"), self.talep_miktar, QLabel("Adres:"), self.talep_adres, btn_talep, btn_geri_al]:
            talep_duzen.addWidget(w)
        
        talep_duzen.addStretch()
        talep_grup.setLayout(talep_duzen)
        sol_panel.addWidget(talep_grup)

        sag_panel = QVBoxLayout()
        sag_panel.addWidget(QLabel("📜 Canlı Müdahale Geçmişi (Linked List)"))
        self.log_listesi = QListWidget()
        sag_panel.addWidget(self.log_listesi)
        
        duzen.addLayout(sol_panel, 1)
        duzen.addLayout(sag_panel, 1)
        self.sekmeler.addTab(sekme, "Saha İhbar")
        self.loglari_guncelle()

    def trie_filtrele(self, metin, combobox, tam_liste):
        if not metin:
            combobox.blockSignals(True)
            combobox.clear()
            combobox.addItems(tam_liste)
            combobox.setCurrentIndex(-1)
            combobox.blockSignals(False)
            return
            
        oneriler = self.yonetici.arama_trie.oneri_getir(metin)
        gecerli_oneriler = []
        for oneri in oneriler:
            for orj_veri in tam_liste:
                if orj_veri.lower() == oneri:
                    if orj_veri not in gecerli_oneriler:
                        gecerli_oneriler.append(orj_veri)
                        
        if not gecerli_oneriler:
            gecerli_oneriler = [item for item in tam_liste if metin.lower() in item.lower()]

        if gecerli_oneriler:
            combobox.blockSignals(True)
            combobox.clear()
            combobox.addItems(gecerli_oneriler)
            combobox.setEditText(metin)
            combobox.blockSignals(False)

    def ihtiyac_seceneklerini_guncelle(self, kategori):
        self.ihtiyac_cb.blockSignals(True)
        self.ihtiyac_cb.clear()
        
        if kategori in self.kategori_sozlugu:
            self.aktif_ihtiyac_listesi = self.kategori_sozlugu[kategori]
        else:
            self.aktif_ihtiyac_listesi = ["Diğer"]
            
        self.ihtiyac_cb.addItems(self.aktif_ihtiyac_listesi)
        self.ihtiyac_cb.setCurrentIndex(-1)
        self.ihtiyac_cb.blockSignals(False)
        self.diger_durumunu_kontrol_et() 

    def diger_durumunu_kontrol_et(self, text=""):
        if not hasattr(self, 'diger_ihtiyac_input') or not hasattr(self, 'diger_oncelik_input'):
            return

        kat = self.kat_cb.currentText()
        ihtiyac = self.ihtiyac_cb.currentText()
        
        if kat == "Diğer Kategori" or ihtiyac == "Diğer":
            self.diger_ihtiyac_input.show()
            self.diger_oncelik_input.show()
        else:
            self.diger_ihtiyac_input.hide()
            self.diger_oncelik_input.hide()

    def talep_olustur_gui(self):
        ekip = self.ekip_cb.currentText()
        kat = self.kat_cb.currentText()
        ihtiyac = self.ihtiyac_cb.currentText()
        adres = self.talep_adres.currentText()

        if not ekip or not kat or not ihtiyac or not adres:
            QMessageBox.warning(self, "Hata", "Lütfen tüm seçimleri yapınız!")
            return
        
        oncelik = None
        
        if kat == "Diğer Kategori" or ihtiyac == "Diğer":
            ihtiyac = self.diger_ihtiyac_input.text()
            if not ihtiyac:
                QMessageBox.warning(self, "Hata", "Lütfen diğer ihtiyacınızı detaylı belirtin!")
                return
            try:
                oncelik = int(self.diger_oncelik_input.text())
                if oncelik < 1 or oncelik > 5: raise ValueError
            except ValueError:
                QMessageBox.warning(self, "Hata", "Öncelik sırası 1 ile 5 arasında bir sayı olmalıdır!")
                return

        try:
            miktar = int(self.talep_miktar.text())
            if miktar <= 0: raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Hata", "Geçerli bir miktar girin!")
            return

        self.yonetici.ekip_talep_ekle(ekip, adres, kat, ihtiyac, miktar, oncelik, "") 
        QMessageBox.information(self, "Eklendi", "Talep sıraya alındı! Koordinasyon sekmesinden depoyu belirleyip karşılayın.")
        
        self.talep_miktar.clear()
        
        self.ekip_cb.blockSignals(True)
        self.ekip_cb.clear()
        self.ekip_cb.addItems(self.yonetici.tum_ekipler)
        self.ekip_cb.clearEditText()
        self.ekip_cb.setCurrentIndex(-1)
        self.ekip_cb.blockSignals(False)

        self.kat_cb.blockSignals(True)
        self.kat_cb.clear()
        self.kat_cb.addItems(list(self.yonetici.tedarikci_verileri.keys()))
        self.kat_cb.clearEditText()
        self.kat_cb.setCurrentIndex(-1)
        self.kat_cb.blockSignals(False)
        self.ihtiyac_seceneklerini_guncelle("") 

        self.ihtiyac_cb.blockSignals(True)
        self.ihtiyac_cb.clearEditText()
        self.ihtiyac_cb.setCurrentIndex(-1)
        self.ihtiyac_cb.blockSignals(False)

        self.talep_adres.blockSignals(True)
        self.talep_adres.clear()
        enkazlar_sadece = [d for d in self.yonetici.sehir_grafi.nodes if "Enkaz" in d]
        self.talep_adres.addItems(enkazlar_sadece)
        self.talep_adres.clearEditText()
        self.talep_adres.setCurrentIndex(-1)
        self.talep_adres.blockSignals(False)
        
        if hasattr(self, 'diger_ihtiyac_input') and self.diger_ihtiyac_input.isVisible():
            self.diger_ihtiyac_input.clear()
            self.diger_oncelik_input.clear()

        self.harita_taleplerini_guncelle()
        self.loglari_guncelle()

    def talep_geri_al_gui(self):
        basarili, mesaj = self.yonetici.talep_geri_al()
        if basarili:
            QMessageBox.information(self, "Geri Alındı", mesaj)
            self.harita_taleplerini_guncelle()
            self.loglari_guncelle()
        else:
            QMessageBox.warning(self, "Hata", mesaj)

    def loglari_guncelle(self):
        self.log_listesi.clear()
        for log in self.yonetici.mudahale_gecmisi.listele():
            self.log_listesi.addItem(f"[{log.zaman_damgasi}] {log.mesaj}")

    def sekme_lojistik_olustur(self):
        sekme = QWidget()
        ana_yatay = QHBoxLayout(sekme)

        # SOL PANEL: Depo Listesi ve Tedarik
        sol_panel = QVBoxLayout()

        # TEDARİK BÖLÜMÜ (SOL ALT, ŞİMDİ YUKARI ÇEKİLDİ)
        tedarik_grup = QGroupBox("📦 Ürün Tedarik (AFAD Büyük Tedarikçiler)")
        tedarik_duzen = QVBoxLayout()
        self.secili_urun_lbl = QLabel("Seçili Ürün: -")
        self.tedarikci_cb = QComboBox()
        self.tedarik_miktar_input = QLineEdit()
        self.tedarik_miktar_input.setPlaceholderText("Alınacak Miktar")
        btn_tedarik_et = QPushButton("Tedarikçi Üzerinden Stok Güncelle")
        btn_tedarik_et.clicked.connect(self.tedarik_islemi_yap)

        tedarik_duzen.addWidget(self.secili_urun_lbl)
        tedarik_duzen.addWidget(QLabel("Tedarikçi:"))
        tedarik_duzen.addWidget(self.tedarikci_cb)
        tedarik_duzen.addWidget(self.tedarik_miktar_input)
        tedarik_duzen.addWidget(btn_tedarik_et)
        tedarik_grup.setLayout(tedarik_duzen)
        sol_panel.addWidget(tedarik_grup)

        sol_panel.addWidget(QLabel("🏢 Depolar"))
        self.depo_listesi_widget = QListWidget()
        self.depo_listesi_widget.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.depo_listesi_widget.addItems(self.yonetici.depolar)
        self.depo_listesi_widget.currentTextChanged.connect(self.lojistik_tablo_guncelle)
        sol_panel.addWidget(self.depo_listesi_widget)

        # SAĞ PANEL: Tablo ve Ürün Ekle/Sil
        sag_panel = QVBoxLayout()
        
        # Ürün Yönetim Araçları (Üst Kısım)
        yonetim_duzen = QHBoxLayout()
        self.yeni_urun_ad = QLineEdit(); self.yeni_urun_ad.setPlaceholderText("Ürün Adı")
        self.yeni_urun_kat = QComboBox(); self.yeni_urun_kat.addItems(self.kategoriler)
        self.yeni_urun_mik = QLineEdit(); self.yeni_urun_mik.setPlaceholderText("Miktar")
        btn_ekle = QPushButton("Ekle"); btn_ekle.clicked.connect(self.urun_ekle_gui)
        btn_sil = QPushButton("Seçiliyi Sil"); btn_sil.clicked.connect(self.urun_sil_gui)
        
        for w in [self.yeni_urun_ad, self.yeni_urun_kat, self.yeni_urun_mik, btn_ekle, btn_sil]:
            yonetim_duzen.addWidget(w)
        
        sag_panel.addLayout(yonetim_duzen)
        sag_panel.addWidget(QLabel("📦 Seçili Depo Envanteri (BST ile Sıralı)"))
        self.envanter_tablosu = QTableWidget(0, 3)
        self.envanter_tablosu.setHorizontalHeaderLabels(["Ürün", "Kategori", "Miktar"])
        self.envanter_tablosu.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.envanter_tablosu.itemClicked.connect(self.urun_secildi_tedarik_guncelle)
        self.envanter_tablosu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        sag_panel.addWidget(self.envanter_tablosu)

        ana_yatay.addLayout(sol_panel, 1)
        ana_yatay.addLayout(sag_panel, 2)
        self.sekmeler.addTab(sekme, "Lojistik (BST)")
        self.depo_listesi_widget.setCurrentRow(0)

    def lojistik_tablo_guncelle(self, secili_depo=None):
        if not secili_depo:
            secili_depo = self.depo_listesi_widget.currentItem().text() if self.depo_listesi_widget.currentItem() else self.yonetici.depolar[0]
            
        urunler = self.yonetici.depo_envanterleri[secili_depo].tum_urunler()
        self.envanter_tablosu.setRowCount(len(urunler))
        for satir, urun in enumerate(urunler):
            self.envanter_tablosu.setItem(satir, 0, QTableWidgetItem(urun.ad))
            self.envanter_tablosu.setItem(satir, 1, QTableWidgetItem(urun.kategori))
            self.envanter_tablosu.setItem(satir, 2, QTableWidgetItem(str(urun.miktar)))

    def urun_secildi_tedarik_guncelle(self, item):
        satir = item.row()
        ad = self.envanter_tablosu.item(satir, 0).text()
        kat = self.envanter_tablosu.item(satir, 1).text()
        self.secili_urun_lbl.setText(f"Seçili Ürün: {ad}")
        
        self.tedarikci_cb.clear()
        tedarikciler = self.yonetici.tedarikci_verileri.get(kat, ["Yerel Tedarikçi"])
        self.tedarikci_cb.addItems(tedarikciler)

    def tedarik_islemi_yap(self):
        depo = self.depo_listesi_widget.currentItem().text()
        ad = self.secili_urun_lbl.text().replace("Seçili Ürün: ", "")
        if ad == "-": return
        
        try:
            miktar = int(self.tedarik_miktar_input.text())
            self.yonetici.envantere_yeni_urun_ekle(depo, Urun(999, ad, "", miktar))
            self.lojistik_tablo_guncelle(depo)
            self.tedarik_miktar_input.clear()
            QMessageBox.information(self, "Başarılı", f"{ad} ürünü {self.tedarikci_cb.currentText()} üzerinden güncellendi.")
        except:
            QMessageBox.warning(self, "Hata", "Geçerli bir miktar girin.")

    def urun_ekle_gui(self):
        depo = self.depo_listesi_widget.currentItem().text()
        ad, kat = self.yeni_urun_ad.text(), self.yeni_urun_kat.currentText()
        try:
            mik = int(self.yeni_urun_mik.text())
            self.yonetici.envantere_yeni_urun_ekle(depo, Urun(100, ad, kat, mik))
            self.lojistik_tablo_guncelle(depo)
        except: QMessageBox.warning(self, "Hata", "Girişleri kontrol edin.")

    def urun_sil_gui(self):
        depo = self.depo_listesi_widget.currentItem().text()
        satir = self.envanter_tablosu.currentRow()
        if satir >= 0:
            ad = self.envanter_tablosu.item(satir, 0).text()
            self.yonetici.envanterden_urun_sil(depo, ad)
            self.lojistik_tablo_guncelle(depo)

    def sekme_harita_olustur(self):
        sekme = QWidget()
        duzen = QHBoxLayout(sekme)
        
        sol_panel = QVBoxLayout()
        sol_panel.addWidget(QLabel("🗺️ Şehir İçi Rota (Graf/Dijkstra)"))
        
        self.baslangic_cb = QComboBox()
        self.bitis_cb = QComboBox()
        dugumler = list(self.yonetici.sehir_grafi.nodes)
        self.baslangic_cb.addItems(dugumler)
        self.bitis_cb.addItems(dugumler)
        sol_panel.addWidget(QLabel("Başlangıç:")); sol_panel.addWidget(self.baslangic_cb)
        sol_panel.addWidget(QLabel("Hedef:")); sol_panel.addWidget(self.bitis_cb)
        btn_rota = QPushButton("Kısa Rotayı Çiz"); btn_rota.clicked.connect(self.rota_ciz)
        sol_panel.addWidget(btn_rota)
        self.rota_sonuc_etiketi = QLabel("")
        sol_panel.addWidget(self.rota_sonuc_etiketi)
        
        # Seçilen Enkazın Taleplerini Gösterme Alanı
        sol_panel.addWidget(QLabel("📍 Seçili Enkazın Talepleri:"))
        self.enkaz_detay_alani = QTextEdit()
        self.enkaz_detay_alani.setReadOnly(True)
        self.enkaz_detay_alani.setStyleSheet("background-color: #F8FAFC; border: 1px solid #94A3B8; color: #1E293B;")
        sol_panel.addWidget(self.enkaz_detay_alani)
        
        sol_panel.addStretch()

        self.fig = Figure(figsize=(8, 8), dpi=100)
        self.fig.patch.set_facecolor('#EBF2FA')
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.canvas.mpl_connect('pick_event', self.haritada_dugum_secildi)

        # SAĞ PANEL
        sag_panel = QVBoxLayout()
        self.durum_lbl = QLabel() 
        self.durum_lbl.setStyleSheet("font-weight: bold; color: #1E3A8A; font-size: 13px;")
        self.durum_lbl.setWordWrap(True) 
        sag_panel.addWidget(self.durum_lbl)
        
        sag_panel.addWidget(QLabel("🚩 İhtiyaç Listesi (Heap)"))
        self.heap_tablosu = QTableWidget(0, 6) 
        self.heap_tablosu.setHorizontalHeaderLabels(["ID", "Öncelik", "Ekip", "İhtiyaç", "Miktar", "Adres"])
        self.heap_tablosu.hideColumn(0) 
        self.heap_tablosu.setSelectionBehavior(QAbstractItemView.SelectRows) 
        self.heap_tablosu.setSelectionMode(QAbstractItemView.SingleSelection) 
        self.heap_tablosu.itemClicked.connect(self.harita_tablo_secimi) 
        sag_panel.addWidget(self.heap_tablosu)
        
        self.harita_depo_cb = QComboBox()
        self.harita_depo_cb.setPlaceholderText("Karşılayacak Depoyu Seçin")
        sag_panel.addWidget(QLabel("Sevkiyat İçin Kaynak Depo:"))
        sag_panel.addWidget(self.harita_depo_cb)

        btn_talep_karsila = QPushButton("⚡ Seçili Talebi Karşıla") 
        btn_talep_karsila.clicked.connect(self.talep_karsila_gui)
        sag_panel.addWidget(btn_talep_karsila)

        duzen.addLayout(sol_panel, 1)
        duzen.addWidget(self.canvas, 3)
        duzen.addLayout(sag_panel, 1)
        
        self.sekmeler.addTab(sekme, "Harita ve İhtiyaçlar")
        self.haritayi_yenile()
        self.harita_taleplerini_guncelle()

    def harita_taleplerini_guncelle(self):
        talepler = sorted(self.yonetici.ekip_talepleri_heap)
        self.heap_tablosu.setRowCount(len(talepler))
        for i, t in enumerate(talepler):
            self.heap_tablosu.setItem(i, 0, QTableWidgetItem(t.talep_id)) 
            self.heap_tablosu.setItem(i, 1, QTableWidgetItem(f"Derece {t.priority}"))
            self.heap_tablosu.setItem(i, 2, QTableWidgetItem(t.ekip_adi))
            self.heap_tablosu.setItem(i, 3, QTableWidgetItem(t.ihtiyac_adi))
            self.heap_tablosu.setItem(i, 4, QTableWidgetItem(str(t.miktar)))
            self.heap_tablosu.setItem(i, 5, QTableWidgetItem(t.adres))
        
        gorevdekiler = [b for b, info in self.yonetici.mesgul_birimler.items() if info["durum"] == "Görevde"]
        cooldowndakiler = [b for b, info in self.yonetici.mesgul_birimler.items() if info["durum"] == "Cooldown"]
        
        ambulans_say = sum(1 for a in self.yonetici.musait_araclar if "Ambulans" in a)
        itfaiye_say = sum(1 for a in self.yonetici.musait_araclar if "İtfaiye" in a)
        is_makinesi_say = sum(1 for a in self.yonetici.musait_araclar if "Makine" in a or "Vinç" in a or "Ekskavatör" in a)
        diger_arac_say = len(self.yonetici.musait_araclar) - (ambulans_say + itfaiye_say + is_makinesi_say)
        
        detayli_arac_metni = (
            f"<div style='font-size: 14px; margin-bottom: 5px;'>"
            f"<span style='color: #10B981; font-weight: bold;'>🟢 Müsait Araçlar ({len(self.yonetici.musait_araclar)}):</span> "
            f"Ambulans: <b>{ambulans_say}</b> | İtfaiye: <b>{itfaiye_say}</b> | İş Makinesi: <b>{is_makinesi_say}</b> | Diğer: <b>{diger_arac_say}</b><br>"
            f"<span style='color: #EF4444; font-weight: bold;'>🔴 Görevde Olan Araçlar: {len(gorevdekiler)}</span>"
            f"</div>"
        )
        self.durum_lbl.setText(detayli_arac_metni)

        self.harita_depo_cb.clear() 

    def harita_tablo_secimi(self, item):
        satir = item.row()
        talep_id = self.heap_tablosu.item(satir, 0).text()
        
        secilen_talep = next((t for t in self.yonetici.ekip_talepleri_heap if t.talep_id == talep_id), None)
        
        self.harita_depo_cb.clear()
        if secilen_talep:
            if secilen_talep.kategori in ["Arama Kurtarma Ekipmanı", "Barınma", "Gıda ve Su", "Sağlık ve İlk Yardım", "Hijyen", "Lojistik ve Enerji", "Malzeme"]:
                uygunlar = self.yonetici.uygun_depolari_bul(secilen_talep.adres, secilen_talep.kategori, secilen_talep.ihtiyac_adi, secilen_talep.miktar)
                for depo, mesafe in uygunlar:
                    self.harita_depo_cb.addItem(f"{depo} (Mesafe: {mesafe})", depo)
                if not uygunlar:
                    for depo in self.yonetici.depolar:
                        try:
                            mesafe = nx.dijkstra_path_length(self.yonetici.sehir_grafi, depo, secilen_talep.adres, weight='weight')
                            self.harita_depo_cb.addItem(f"{depo} (Stok Yok! Acil Tedarik Edilecek, Mesafe: {mesafe})", depo)
                        except nx.NetworkXNoPath: pass
            else:
                musait_birim_var_mi = False
                if secilen_talep.kategori == "Personel/Gönüllü":
                    self.harita_depo_cb.addItem(f"Gönüllü Kuyruğundan Gönder ({secilen_talep.miktar} Kişi)", "Gönüllü Kuyruğu")
                    musait_birim_var_mi = True
                elif secilen_talep.kategori == "Araç/İş Makinesi" or any(x in secilen_talep.ihtiyac_adi for x in ["Ambulans", "İtfaiye", "Makine", "Vinç", "Kamyon"]):
                    eslesenler = []
                    for arac in self.yonetici.musait_araclar:
                        if "Ambulans" in secilen_talep.ihtiyac_adi and "Ambulans" in arac: eslesenler.append(arac)
                        elif "İtfaiye" in secilen_talep.ihtiyac_adi and "İtfaiye" in arac: eslesenler.append(arac)
                        elif "Makine" in secilen_talep.ihtiyac_adi and ("Makine" in arac or "Ekskavatör" in arac): eslesenler.append(arac)
                        elif "Vinç" in secilen_talep.ihtiyac_adi and "Vinç" in arac: eslesenler.append(arac)
                        elif "Kamyon" in secilen_talep.ihtiyac_adi and "Kamyon" in arac: eslesenler.append(arac)
                        elif secilen_talep.kategori == "Araç/İş Makinesi" and not any(x in secilen_talep.ihtiyac_adi for x in ["Ambulans", "İtfaiye", "Vinç", "Kamyon"]):
                             if "Makine" in arac or "Ekskavatör" in arac or "Kamyon" in arac:
                                 eslesenler.append(arac)
                                 
                    if eslesenler:
                        self.harita_depo_cb.addItem(f"Yönlendir: {eslesenler[0]}", eslesenler[0])
                        musait_birim_var_mi = True
                
                if not musait_birim_var_mi:
                     self.harita_depo_cb.addItem("Uygun Birim Bulunamadı / Atama Yapılamıyor", "")

    def talep_karsila_gui(self):
        satir = self.heap_tablosu.currentRow()
        if satir < 0:
            QMessageBox.warning(self, "Dikkat", "Lütfen tablodan karşılamak istediğiniz talebi seçin.")
            return

        talep_id = self.heap_tablosu.item(satir, 0).text()
        
        hedef_adres = None
        for t in self.yonetici.ekip_talepleri_heap:
             if t.talep_id == talep_id:
                  hedef_adres = t.adres
                  break

        secilen_veri = self.harita_depo_cb.currentData()

        # DEPO OTOMATİK SEÇİM MANTIĞI
        talep = next((t for t in self.yonetici.ekip_talepleri_heap if t.talep_id == talep_id), None)
        if talep and not secilen_veri:
            malzeme_kategorileri = ["Arama Kurtarma Ekipmanı", "Barınma", "Gıda ve Su", "Sağlık ve İlk Yardım", "Hijyen", "Lojistik ve Enerji", "Malzeme"]
            if talep.kategori in malzeme_kategorileri:
                uygunlar = self.yonetici.uygun_depolari_bul(hedef_adres, talep.kategori, talep.ihtiyac_adi, talep.miktar)
                if uygunlar:
                    secilen_veri = uygunlar[0][0] # Stoku olan en yakın depo
                else:
                    # Stoku yoksa bile mesafeye göre en yakını bul
                    mesafeler = []
                    for depo in self.yonetici.depolar:
                        try:
                            m = nx.dijkstra_path_length(self.yonetici.sehir_grafi, depo, hedef_adres, weight='weight')
                            mesafeler.append((depo, m))
                        except: pass
                    if mesafeler:
                        mesafeler.sort(key=lambda x: x[1])
                        secilen_veri = mesafeler[0][0]

        basarili, mesaj = self.yonetici.talep_karsila(talep_id, secilen_veri)
        if basarili:
            QMessageBox.information(self, "Başarılı", mesaj)
            
            if secilen_veri and secilen_veri in self.yonetici.depolar:
                self.baslangic_cb.setCurrentText(secilen_veri)
                self.bitis_cb.setCurrentText(hedef_adres)
                self.rota_ciz()
                
            self.lojistik_tablo_guncelle() 
            self.harita_taleplerini_guncelle() 
            self.loglari_guncelle()
            self.gorevleri_guncelle()
            self.gonullu_listesini_tazele()
        else:
            QMessageBox.warning(self, "Dikkat", mesaj)

    def haritayi_yenile(self, yol=None):
        RotaGorsellestirici.harita_ciz(self.yonetici.sehir_grafi, self.ax, yol)
        self.canvas.draw()

    def rota_ciz(self):
        bas, bit = self.baslangic_cb.currentText(), self.bitis_cb.currentText()
        yol, mesafe = self.yonetici.rota_hesapla(bas, bit)
        if yol:
            self.rota_sonuc_etiketi.setText(f"✅ Rota: {' ➔ '.join(yol)}\nMesafe: {mesafe}")
            self.haritayi_yenile(yol)
            self.loglari_guncelle()

    def haritada_dugum_secildi(self, event):
        ind = event.ind[0]
        dugum_adi = list(self.yonetici.sehir_grafi.nodes)[ind]
        
        if "Enkaz" in dugum_adi:
            talepler = [t for t in self.yonetici.ekip_talepleri_heap if t.adres == dugum_adi]
            if not talepler:
                self.enkaz_detay_alani.setText(f"✅ {dugum_adi} için bekleyen talep yok.")
            else:
                metin = f"📋 {dugum_adi} Bekleyen Talepler:\n" + "-"*30 + "\n"
                for t in sorted(talepler):
                    metin += f"• [Öncelik {t.priority}] {t.kategori} - {t.ihtiyac_adi} ({t.miktar} adet)\n"
                self.enkaz_detay_alani.setText(metin)
        else:
            self.enkaz_detay_alani.setText(f"🏢 {dugum_adi} seçildi. Bu bir depodur.")

    def donenleri_kontrol_et(self):
        donenler = self.yonetici.durumlari_guncelle()
        if donenler:
            self.harita_taleplerini_guncelle()
            self.loglari_guncelle() 

    def sekme_kaynak_gorev_olustur(self):
        sekme = QWidget()
        duzen = QHBoxLayout(sekme)

        sol_panel = QVBoxLayout()
        sol_panel.addWidget(QLabel("📋 Görev Yönetimi (Stack)"))
        self.gorev_tablosu = QTableWidget(0, 6)
        self.gorev_tablosu.setHorizontalHeaderLabels(["ID", "Açıklama", "Durum", "Uzmanlık", "Kişi", "Atananlar"])
        sol_panel.addWidget(self.gorev_tablosu)
        
        btn_tamamla = QPushButton("Seçili Görevi Tamamla (Kişi Ata)")
        btn_tamamla.clicked.connect(self.gorevi_tamamla)
        btn_undo = QPushButton("Geri Al (Undo)")
        btn_undo.clicked.connect(self.gorev_geri_al)
        sol_panel.addWidget(btn_tamamla)
        sol_panel.addWidget(btn_undo)

        sag_panel = QVBoxLayout()
        sag_panel.addWidget(QLabel("👥 Gönüllü Kuyruğu (Queue)"))
        
        self.gonullu_tablosu = QTableWidget(0, 3)
        self.gonullu_tablosu.setHorizontalHeaderLabels(["ID/TC", "Ad Soyad", "Uzmanlık"])
        self.gonullu_tablosu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        sag_panel.addWidget(self.gonullu_tablosu)

        ekle_grup = QGroupBox("Yeni Gönüllü Kaydı")
        ekle_duzen = QGridLayout()
        
        self.gon_id = QLineEdit(); self.gon_id.setPlaceholderText("Kimlik No")
        self.gon_ad = QLineEdit(); self.gon_ad.setPlaceholderText("Ad Soyad")
        self.gon_kat = QComboBox()
        self.gon_kat.addItems(["Arama-Kurtarma", "Sağlık/Tıp", "Lojistik", "Psikososyal Destek", "Mutfak/Gıda"])
        
        btn_ekle = QPushButton("Kuyruğa Ekle")
        btn_ekle.clicked.connect(self.kuyruga_ekle)
        
        ekle_duzen.addWidget(QLabel("Kimlik:"), 0, 0); ekle_duzen.addWidget(self.gon_id, 0, 1)
        ekle_duzen.addWidget(QLabel("İsim:"), 1, 0); ekle_duzen.addWidget(self.gon_ad, 1, 1)
        ekle_duzen.addWidget(QLabel("Kategori:"), 2, 0); ekle_duzen.addWidget(self.gon_kat, 2, 1)
        ekle_duzen.addWidget(btn_ekle, 3, 0, 1, 2)
        ekle_grup.setLayout(ekle_duzen)
        
        sag_panel.addWidget(ekle_grup)
        duzen.addLayout(sol_panel, 1)
        duzen.addLayout(sag_panel, 1)
        self.sekmeler.addTab(sekme, "Görev/Gönüllü")
        self.gonullu_listesini_tazele()
        self.gorevleri_guncelle()
    def gorevleri_guncelle(self):
        gorevler = list(self.yonetici.gorev_yonetimi.values())
        self.gorev_tablosu.setRowCount(len(gorevler))
        for i, g in enumerate(gorevler):
            item_id = QTableWidgetItem(g.gorev_id)
            item_ac = QTableWidgetItem(g.aciklama)
            item_durum = QTableWidgetItem(g.durum)
            item_uz = QTableWidgetItem(g.gereken_uzmanlik)
            item_kisi = QTableWidgetItem(str(g.kisi_sayisi))
            item_atanan = QTableWidgetItem(g.atanan_kisiler)
            
            if g.durum == "Tamamlandı":
                from PyQt5.QtGui import QColor
                renk = QColor("#dcfce7") # Açık yeşil
                item_id.setBackground(renk)
                item_ac.setBackground(renk)
                item_durum.setBackground(renk)
                item_uz.setBackground(renk)
                item_kisi.setBackground(renk)
                item_atanan.setBackground(renk)

            self.gorev_tablosu.setItem(i, 0, item_id)
            self.gorev_tablosu.setItem(i, 1, item_ac)
            self.gorev_tablosu.setItem(i, 2, item_durum)
            self.gorev_tablosu.setItem(i, 3, item_uz)
            self.gorev_tablosu.setItem(i, 4, item_kisi)
            self.gorev_tablosu.setItem(i, 5, item_atanan)

    def gorevi_tamamla(self):
        satir = self.gorev_tablosu.currentRow()
        if satir >= 0:
            g_id = self.gorev_tablosu.item(satir, 0).text()
            basarili, mesaj = self.yonetici.gorev_tamamla(g_id)
            if basarili:
                QMessageBox.information(self, "Başarılı", mesaj)
            else:
                QMessageBox.warning(self, "Uyarı", mesaj)
            self.gorevleri_guncelle()
            self.gonullu_listesini_tazele()
            self.loglari_guncelle()

    def gorev_geri_al(self):
        self.yonetici.gorev_geri_al()
        self.gorevleri_guncelle()
        self.loglari_guncelle()

    def kuyruga_ekle(self):
        kid, ad, kat = self.gon_id.text(), self.gon_ad.text(), self.gon_kat.currentText()
        if kid and ad:
            yeni_g = Gonullu(kid, ad, kat)
            self.yonetici.gonullu_siraya_al(yeni_g)
            self.gon_id.clear(); self.gon_ad.clear()
            self.gonullu_listesini_tazele()
            self.loglari_guncelle()

    def gonullu_listesini_tazele(self):
        tum_gonulluler = []
        for kuyruk in self.yonetici.gonullu_kuyruklari.values():
            tum_gonulluler.extend(kuyruk.kuyruk)
            
        self.gonullu_tablosu.setRowCount(len(tum_gonulluler))
        for i, g in enumerate(tum_gonulluler):
            self.gonullu_tablosu.setItem(i, 0, QTableWidgetItem(g.kimlik))
            self.gonullu_tablosu.setItem(i, 1, QTableWidgetItem(g.ad_soyad))
            self.gonullu_tablosu.setItem(i, 2, QTableWidgetItem(g.kategori))

    def sekme_raporlama_olustur(self):
        sekme = QWidget()
        duzen = QVBoxLayout(sekme)
        
        btn_test = QPushButton("CRUD Performans Testini Başlat")
        btn_test.clicked.connect(self.dinamik_performans_ciz)
        duzen.addWidget(btn_test)

        self.perf_fig = Figure(figsize=(10, 4), dpi=100)
        self.perf_fig.patch.set_facecolor('#EBF2FA')
        self.perf_canvas = FigureCanvas(self.perf_fig)
        duzen.addWidget(self.perf_canvas)
        
        self.sekmeler.addTab(sekme, "Akademik Rapor (CRUD)")

    def dinamik_performans_ciz(self):
        QMessageBox.information(self, "Bilgi", "CRUD Testi Başlıyor, bekleyin...")
        QApplication.processEvents()
        PerformansAnalizi.crud_testi_ciz(self.perf_fig)
        self.perf_canvas.draw()