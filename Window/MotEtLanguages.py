import json
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap, QFont, QColor, QIcon
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel,
    QLineEdit, QTextEdit, QFileDialog, QInputDialog,
    QHBoxLayout, QFrame, QScrollArea, QSizePolicy,
    QGraphicsDropShadowEffect, QGroupBox, QGridLayout,
    QDesktopWidget
)

from model.automate import Automate

class ModernGroupBox(QGroupBox):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setStyleSheet("""
            QGroupBox {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                margin-top: 1em;
                padding: 15px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
                color: #3b82f6;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 25))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

class ModernLineEdit(QLineEdit):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                padding: 8px 15px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                background-color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
            }
        """)

class ModernButton(QPushButton):
    def __init__(self, text, is_primary=True, icon=None, parent=None):
        super().__init__(text, parent)
        color = "#3b82f6" if is_primary else "#64748b"
        hover_color = "#2563eb" if is_primary else "#475569"
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {hover_color};
                padding: 9px 15px 7px 15px;
            }}
        """)
        if icon:
            self.setText(f"{icon} {text}")
        self.setCursor(Qt.PointingHandCursor)

class ScrollableTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 15px;
                font-family: 'Consolas', monospace;
                font-size: 14px;
                line-height: 1.6;
                color: #1e293b;
            }
        """)
        self.setReadOnly(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

class MotEtLangages(QWidget):
    def __init__(self, automate, autres_automates: dict):
        super().__init__()
        self.automate = automate
        self.autre_automate = None
        self.autres_automates = autres_automates
        self.etat_initial = self.get_initial_state(self.automate.to_dict()) if self.automate else None
        
        self.init_ui()
        self.adjust_size()

    def adjust_size(self):
        # Get screen size
        screen = QDesktopWidget().screenGeometry()
        # Set window size to 80% of screen size
        self.resize(int(screen.width() * 0.8), int(screen.height() * 0.8))
        # Center window
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_ui(self):
        self.setWindowTitle("Opérations sur les Mots et Langages")
        self.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
                font-family: 'Segoe UI', Arial;
            }
            QLabel {
                color: #334155;
                font-size: 13px;
            }
        """)

        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Left Panel (Controls)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(15)

        # Automate Loading Group
        loading_group = ModernGroupBox("Chargement des Automates")
        loading_layout = QVBoxLayout(loading_group)
        
        btn_charger = ModernButton("Charger automate principal", True, "📂")
        btn_charger.clicked.connect(self.charger_automate_principal)
        loading_layout.addWidget(btn_charger)

        btn_charger_autre = ModernButton("Charger automate secondaire", True, "📥")
        btn_charger_autre.clicked.connect(self.charger_automate_secondaire)
        loading_layout.addWidget(btn_charger_autre)
        
        left_layout.addWidget(loading_group)

        # Word Recognition Group
        word_group = ModernGroupBox("Reconnaissance de Mots")
        word_layout = QVBoxLayout(word_group)
        
        self.input_mot = ModernLineEdit("Entrez un mot à tester")
        word_layout.addWidget(self.input_mot)
        
        btn_tester = ModernButton("Tester le mot", True, "🔍")
        btn_tester.clicked.connect(self.tester_mot)
        word_layout.addWidget(btn_tester)
        
        left_layout.addWidget(word_group)

        # Word Generation Group
        gen_group = ModernGroupBox("Génération de Mots")
        gen_layout = QVBoxLayout(gen_group)
        
        self.input_longueur = ModernLineEdit("Longueur maximale")
        gen_layout.addWidget(self.input_longueur)
        
        btn_gen = ModernButton("Générer mots acceptés", True, "✨")
        btn_gen.clicked.connect(self.generer_mots_acceptes)
        gen_layout.addWidget(btn_gen)
        
        btn_rejetes = ModernButton("Afficher mots rejetés", False, "❌")
        btn_rejetes.clicked.connect(self.mots_rejetes)
        gen_layout.addWidget(btn_rejetes)
        
        left_layout.addWidget(gen_group)

        # Binary Operations Group
        op_group = ModernGroupBox("Opérations Binaires")
        op_layout = QGridLayout(op_group)
        
        btn_equiv = ModernButton("Tester équivalence", True, "🔄")
        btn_equiv.clicked.connect(self.tester_equivalence)
        op_layout.addWidget(btn_equiv, 0, 0)
        
        btn_union = ModernButton("Calculer union", True, "∪")
        btn_union.clicked.connect(self.calculer_union)
        op_layout.addWidget(btn_union, 0, 1)
        
        btn_intersection = ModernButton("Calculer intersection", True, "∩")
        btn_intersection.clicked.connect(self.calculer_intersection)
        op_layout.addWidget(btn_intersection, 1, 0)
        
        btn_complement = ModernButton("Calculer complément", True, "¬")
        btn_complement.clicked.connect(self.calculer_complement)
        op_layout.addWidget(btn_complement, 1, 1)
        
        left_layout.addWidget(op_group)

        # Return Button
        btn_revenir = ModernButton("Retour à l'accueil", False, "🏠")
        btn_revenir.clicked.connect(self.revenir_accueil)
        left_layout.addWidget(btn_revenir)

        # Add left panel to main layout with shadow
        left_container = QWidget()
        left_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #e2e8f0;
            }
        """)
        left_container_layout = QVBoxLayout(left_container)
        left_container_layout.addWidget(left_panel)
        
        shadow = QGraphicsDropShadowEffect(left_container)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        left_container.setGraphicsEffect(shadow)
        
        main_layout.addWidget(left_container, 1)

        # Right Panel (Results and Visualization)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # Visualization Title
        viz_title = QLabel("Visualisation de l'Automate")
        viz_title.setStyleSheet("""
            QLabel {
                color: #1e293b;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 0;
            }
        """)
        right_layout.addWidget(viz_title)

        # Image Display
        self.label_image = QLabel()
        self.label_image.setAlignment(Qt.AlignCenter)
        self.label_image.setMinimumSize(500, 300)
        self.label_image.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        right_layout.addWidget(self.label_image, 2)

        # Results Title
        results_title = QLabel("Résultats")
        results_title.setStyleSheet("""
            QLabel {
                color: #1e293b;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 0;
            }
        """)
        right_layout.addWidget(results_title)

        # Results Display
        self.resultat = QTextEdit()
        self.resultat.setReadOnly(True)
        self.resultat.setStyleSheet("""
            QTextEdit {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 15px;
                font-family: 'Consolas', monospace;
                font-size: 14px;
                line-height: 1.6;
                color: #1e293b;
            }
        """)
        right_layout.addWidget(self.resultat, 1)

        # Add right panel to main layout with shadow
        right_container = QWidget()
        right_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #e2e8f0;
            }
        """)
        right_container_layout = QVBoxLayout(right_container)
        right_container_layout.addWidget(right_panel)
        
        shadow = QGraphicsDropShadowEffect(right_container)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        right_container.setGraphicsEffect(shadow)
        
        main_layout.addWidget(right_container, 2)

        # Si un automate est déjà chargé, l'afficher
        if self.automate:
            self.afficher_automate(self.automate)

    def afficher_automate(self, automate):
        try:
            # Générer l'image de l'automate
            automate.to_graphviz("temp_automate")
            pixmap = QPixmap("temp_automate.png")
            if not pixmap.isNull():
                # Redimensionner l'image si elle est trop grande tout en gardant le ratio
                label_size = self.label_image.size()
                scaled_pixmap = pixmap.scaled(
                    label_size,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.label_image.setPixmap(scaled_pixmap)
            else:
                self.label_image.setText("Visualisation non disponible")
                print("Erreur: Impossible de charger l'image générée")
        except Exception as e:
            self.label_image.setText(f"Erreur de visualisation : {str(e)}")
            print(f"Erreur lors de la visualisation : {str(e)}")  # Pour le débogage

    def get_initial_state(self, data):
        for etat in data["etats"]:
            if etat.get("est_initial"):
                return etat["nom"]
        return None

    def charger_automate_principal(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choisir un automate principal", "", "Fichiers JSON (*.json)")
        if path:
            with open(path, "r", encoding="utf-8") as f:
                jsonData = json.load(f)
                self.etat_initial = self.get_initial_state(jsonData)
                self.automate = Automate.from_dict(jsonData)
            self.resultat.setText(f"✅ Automate principal chargé : {self.automate.nom}")

    def charger_automate_secondaire(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choisir un autre automate", "", "Fichiers JSON (*.json)")
        if path:
            with open(path, "r", encoding="utf-8") as f:
                jsonData = json.load(f)
                self.autre_automate = Automate.from_dict(jsonData)
                nom, ok = QInputDialog.getText(self, "Nom de l'automate", "Entrez un nom pour cet automate :")
                if ok and nom:
                    self.autres_automates[nom] = self.autre_automate
                    self.resultat.setText(f"✅ Automate secondaire « {nom} » chargé avec succès.")
                else:
                    self.resultat.setText("❌ Nom invalide. L'automate n'a pas été ajouté.")

    def reconnait(self, mot: str) -> bool:
        etat_courant = self.etat_initial
        for symbole in mot:
            if symbole not in self.automate.alphabet:
                return False
            transition_trouvee = False
            for t in self.automate.transitions:
                if t.source == etat_courant and t.symbole == symbole:
                    etat_courant = t.destination
                    transition_trouvee = True
                    break
            if not transition_trouvee:
                return False
        return etat_courant in [e.nom for e in self.automate.etats.values() if e.est_final]

    def tester_mot(self):
        mot = self.input_mot.text()
        if mot == "":
            self.resultat.setText("❌ Veuillez entrer un mot.")
            return
        reconnu = self.reconnait(mot)
        self.resultat.setText(f"✅ Le mot « {mot} » est reconnu." if reconnu else f"❌ Le mot « {mot} » est rejeté.")

    def generer_mots_acceptes(self):
        try:
            n = int(self.input_longueur.text())
            mots = self.automate.generer_mots_acceptes(n)
            self.resultat.setText("Mots acceptés :\n" + ", ".join(mots))
        except Exception:
            self.resultat.setText("❌ Entrez une longueur maximale valide.")

    def mots_rejetes(self):
        try:
            n = int(self.input_longueur.text())
            mots = self.automate.mots_rejetes(n)
            self.resultat.setText("Mots rejetés :\n" + ", ".join(mots))
        except Exception:
            self.resultat.setText("❌ Entrez une longueur maximale valide.")

    def tester_equivalence(self):
        if not self.autre_automate:
            self.resultat.setText("❌ Aucun automate secondaire chargé.")
            return
        try:
            n = int(self.input_longueur.text())
            equiv = self.automate.est_equivalent(self.autre_automate, n)
            msg = "✅ Les deux automates sont équivalents." if equiv else "❌ Les deux automates ne sont pas équivalents."
            self.resultat.setText(msg)
        except Exception:
            self.resultat.setText("❌ Spécifiez une longueur maximale valide.")

    def calculer_union(self):
        if not self.autre_automate:
            self.resultat.setText("❌ Aucun automate secondaire chargé.")
            return
        try:
            union = self.automate.union(self.autre_automate)
            self.autres_automates[union.nom] = union
            self.resultat.setText(f"✅ Union calculée : {union.nom}")
            self.afficher_automate(union)
        except Exception as e:
            self.resultat.setText(f"❌ Erreur lors du calcul de l'union : {str(e)}")

    def calculer_intersection(self):
        if not self.automate or not self.autre_automate:
            self.resultat.setText("❌ Assurez-vous que les deux automates sont chargés.")
            return
        try:
            intersection = self.automate.intersection(self.autre_automate)
            self.autres_automates[intersection.nom] = intersection
            self.resultat.setText(f"✅ Intersection calculée : {intersection.nom}")
            self.afficher_automate(intersection)
        except Exception as e:
            self.resultat.setText(f"❌ Erreur lors du calcul de l'intersection : {str(e)}")

    def calculer_complement(self):
        try:
            # Crée un automate complément avec un nom explicite
            complement = self.automate.complement()

            # S'il n'a pas de nom (et ça cause l'erreur), on en donne un ici :
            if not hasattr(complement, 'nom') or not complement.nom:
                complement.nom = f"{self.automate.nom}_complement"

            self.autres_automates[complement.nom] = complement
            self.resultat.setText(f"✅ Complément calculé : {complement.nom}")
            self.afficher_automate(complement)

        except Exception as e:
            self.resultat.setText(f"❌ Erreur lors du calcul du complément : {str(e)}")

    def revenir_accueil(self):
        from interfaceGraphique.AcceuilWindow import AccueilWindow
        self.accueil_window = AccueilWindow()
        self.accueil_window.show()
        self.close()