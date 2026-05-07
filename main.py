import sys
from PyQt5.QtWidgets import QApplication
from ana_pencere import AnaPencere

def main():
    # O(1) başlatma - Uygulama ana döngüsü
    app = QApplication(sys.argv)
    app.setStyle("Fusion") 
    
    pencere = AnaPencere()
    pencere.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()