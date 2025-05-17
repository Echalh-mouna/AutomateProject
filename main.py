import sys

from PyQt5.QtWidgets import (
    QApplication
)

from interfaceGraphique.AcceuilWindow import AccueilWindow

app = QApplication(sys.argv)
accueil = AccueilWindow()
accueil.show()
sys.exit(app.exec_())