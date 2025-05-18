import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from interfaceGraphique.MainApplication import MainApplication

# Créer le dossier data s'il n'existe pas
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Initialiser l'application
app = QApplication(sys.argv)
main_app = MainApplication()
main_app.start()
sys.exit(app.exec_())