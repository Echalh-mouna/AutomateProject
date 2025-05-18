import json
import os
import shutil

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QTextEdit, QFileDialog, QMessageBox, QCheckBox,
    QFrame, QScrollArea, QGroupBox, QGridLayout, QDesktopWidget
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from interfaceGraphique.AcceuilWindow import AccueilWindow
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
        
        # Add shadow effect
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
    def __init__(self, text, is_primary=True, parent=None):
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
        self.setCursor(Qt.PointingHandCursor)

class AutomateApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Automates")
        self.automate = None
        self.base_path = ""
        self.init_ui()
        self.adjust_window_size()
        
    def adjust_window_size(self):
        # Get screen size
        screen = QDesktopWidget().screenGeometry()
        # Set window size to 80% of screen size
        width = int(screen.width() * 0.8)
        height = int(screen.height() * 0.8)
        self.resize(width, height)
        # Center window
        self.center()

    def center(self):
        # Center window on screen
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
        
    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
                font-family: 'Segoe UI', Arial;
            }
            QLabel {
                color: #334155;
                font-size: 13px;
            }
            QCheckBox {
                color: #334155;
                font-size: 13px;
                padding: 5px;
            }
            QTextEdit {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 10px;
                font-family: 'Consolas', monospace;
                font-size: 14px;
                line-height: 1.4;
            }
        """)

        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Left panel for controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(15)

        # Automate Creation Group
        creation_group = ModernGroupBox("Création et Chargement")
        creation_layout = QVBoxLayout(creation_group)
        
        self.nom_automate = ModernLineEdit(placeholder="Nom de l'automate")
        creation_layout.addWidget(QLabel("Nom de l'automate"))
        creation_layout.addWidget(self.nom_automate)
        
        btn_layout = QHBoxLayout()
        btn_dossier = ModernButton("📁 Choisir Dossier")
        btn_dossier.clicked.connect(self.choisir_dossier)
        btn_layout.addWidget(btn_dossier)
        
        btn_creer = ModernButton("✨ Créer")
        btn_creer.clicked.connect(self.creer_automate)
        btn_layout.addWidget(btn_creer)
        
        btn_charger = ModernButton("📂 Charger")
        btn_charger.clicked.connect(self.charger_automate)
        btn_layout.addWidget(btn_charger)
        
        creation_layout.addLayout(btn_layout)
        left_layout.addWidget(creation_group)

        # États Group
        etats_group = ModernGroupBox("Gestion des États")
        etats_layout = QVBoxLayout(etats_group)
        
        self.etat_name = ModernLineEdit(placeholder="Nom de l'état")
        etats_layout.addWidget(QLabel("Nom de l'état"))
        etats_layout.addWidget(self.etat_name)
        
        checks_layout = QHBoxLayout()
        self.check_initial = QCheckBox("État Initial")
        self.check_final = QCheckBox("État Final")
        checks_layout.addWidget(self.check_initial)
        checks_layout.addWidget(self.check_final)
        etats_layout.addLayout(checks_layout)
        
        etats_btn_layout = QHBoxLayout()
        btn_ajouter_etat = ModernButton("➕ Ajouter")
        btn_ajouter_etat.clicked.connect(self.ajouter_etat)
        etats_btn_layout.addWidget(btn_ajouter_etat)
        
        btn_supprimer_etat = ModernButton("❌ Supprimer", False)
        btn_supprimer_etat.clicked.connect(self.supprimer_etat)
        etats_btn_layout.addWidget(btn_supprimer_etat)
        
        etats_layout.addLayout(etats_btn_layout)
        left_layout.addWidget(etats_group)

        # Transitions Group
        transitions_group = ModernGroupBox("Gestion des Transitions")
        transitions_layout = QGridLayout(transitions_group)
        
        self.source = ModernLineEdit(placeholder="État source")
        self.symbole = ModernLineEdit(placeholder="Symbole")
        self.destination = ModernLineEdit(placeholder="État destination")
        
        transitions_layout.addWidget(QLabel("État source"), 0, 0)
        transitions_layout.addWidget(self.source, 0, 1)
        transitions_layout.addWidget(QLabel("Symbole"), 1, 0)
        transitions_layout.addWidget(self.symbole, 1, 1)
        transitions_layout.addWidget(QLabel("État destination"), 2, 0)
        transitions_layout.addWidget(self.destination, 2, 1)
        
        trans_btn_layout = QHBoxLayout()
        btn_ajouter_trans = ModernButton("➕ Ajouter")
        btn_ajouter_trans.clicked.connect(self.ajouter_transition)
        trans_btn_layout.addWidget(btn_ajouter_trans)
        
        btn_supprimer_trans = ModernButton("❌ Supprimer", False)
        btn_supprimer_trans.clicked.connect(self.supprimer_transition)
        trans_btn_layout.addWidget(btn_supprimer_trans)
        
        transitions_layout.addLayout(trans_btn_layout, 3, 0, 1, 2)
        left_layout.addWidget(transitions_group)

        # Actions Group
        actions_group = ModernGroupBox("Actions")
        actions_layout = QHBoxLayout(actions_group)
        
        btn_sauvegarder = ModernButton("💾 Sauvegarder")
        btn_sauvegarder.clicked.connect(self.sauvegarder_automate)
        actions_layout.addWidget(btn_sauvegarder)
        
        btn_supprimer = ModernButton("🗑️ Supprimer", False)
        btn_supprimer.clicked.connect(self.supprimer_automate)
        actions_layout.addWidget(btn_supprimer)
        
        left_layout.addWidget(actions_group)

        # Return button
        btn_revenir = ModernButton("🏠 Retour à l'accueil", False)
        btn_revenir.clicked.connect(self.revenir_accueil)
        left_layout.addWidget(btn_revenir)

        # Add left panel to main layout
        left_panel_container = QWidget()
        left_panel_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #e2e8f0;
            }
        """)
        left_panel_container_layout = QVBoxLayout(left_panel_container)
        left_panel_container_layout.addWidget(left_panel)
        
        # Add shadow to left panel
        shadow = QGraphicsDropShadowEffect(left_panel_container)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        left_panel_container.setGraphicsEffect(shadow)
        
        main_layout.addWidget(left_panel_container, 1)

        # Right panel for result
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Créer un widget pour contenir la visualisation
        viz_container = QWidget()
        viz_layout = QVBoxLayout(viz_container)
        
        # Title for visualization
        viz_title = QLabel("Visualisation de l'Automate")
        viz_title.setStyleSheet("""
            QLabel {
                color: #1e293b;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 0;
            }
        """)
        viz_layout.addWidget(viz_title)

        # Scroll area pour la visualisation
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)

        # Label pour l'image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        scroll.setWidget(self.image_label)
        viz_layout.addWidget(scroll)

        # Description textuelle
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setMaximumHeight(150)  # Limiter la hauteur
        viz_layout.addWidget(self.result)

        right_layout.addWidget(viz_container)

        # Add right panel to main layout
        right_panel_container = QWidget()
        right_panel_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #e2e8f0;
            }
        """)
        right_panel_container_layout = QVBoxLayout(right_panel_container)
        right_panel_container_layout.addWidget(right_panel)
        
        # Add shadow to right panel
        shadow = QGraphicsDropShadowEffect(right_panel_container)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        right_panel_container.setGraphicsEffect(shadow)
        
        main_layout.addWidget(right_panel_container, 2)

    def choisir_dossier(self):
        self.base_path = QFileDialog.getExistingDirectory(self, "Choisir un dossier")
        if self.base_path:
            QMessageBox.information(self, "Succès", f"Dossier sélectionné : {self.base_path}")

    def creer_automate(self):
        nom = self.nom_automate.text()
        if not nom or not self.base_path:
            QMessageBox.warning(self, "Erreur", "Veuillez spécifier un nom d'automate et sélectionner un dossier.")
            return
        try:
            os.makedirs(os.path.join(self.base_path, nom), exist_ok=True)
            self.automate = Automate(nom)
            self.afficher_automate()
            QMessageBox.information(self, "Succès", f"L'automate '{nom}' a été créé avec succès.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la création de l'automate : {str(e)}")

    def charger_automate(self):
        if not self.base_path:
            QMessageBox.warning(self, "Erreur", "Veuillez d'abord sélectionner un dossier.")
            return
        try:
            chemin = os.path.join(self.base_path, self.nom_automate.text(), f"{self.nom_automate.text()}.json")
            if not os.path.exists(chemin):
                QMessageBox.warning(self, "Erreur", "Fichier automate introuvable.")
                return
            with open(chemin, "r", encoding="utf-8") as f:
                self.automate = Automate.from_dict(json.load(f))
            self.afficher_automate()
            QMessageBox.information(self, "Succès", f"L'automate '{self.automate.nom}' a été chargé avec succès.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement de l'automate : {str(e)}")

    def ajouter_etat(self):
        if not self.automate:
            QMessageBox.warning(self, "Erreur", "Veuillez d'abord créer ou charger un automate.")
            return
        try:
            nom_etat = self.etat_name.text()
            if not nom_etat:
                QMessageBox.warning(self, "Erreur", "Veuillez spécifier un nom d'état.")
                return
            self.automate.ajouter_etat(nom_etat, self.check_initial.isChecked(), self.check_final.isChecked())
            self.etat_name.clear()
            self.check_initial.setChecked(False)
            self.check_final.setChecked(False)
            self.afficher_automate()
            QMessageBox.information(self, "Succès", f"L'état '{nom_etat}' a été ajouté avec succès.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout de l'état : {str(e)}")

    def supprimer_etat(self):
        if not self.automate:
            QMessageBox.warning(self, "Erreur", "Veuillez d'abord créer ou charger un automate.")
            return
        try:
            nom_etat = self.etat_name.text()
            if not nom_etat:
                QMessageBox.warning(self, "Erreur", "Veuillez spécifier un nom d'état.")
                return
            self.automate.supprimer_etat(nom_etat)
            self.etat_name.clear()
            self.afficher_automate()
            QMessageBox.information(self, "Succès", f"L'état '{nom_etat}' a été supprimé avec succès.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression de l'état : {str(e)}")

    def ajouter_transition(self):
        if not self.automate:
            QMessageBox.warning(self, "Erreur", "Veuillez d'abord créer ou charger un automate.")
            return
        try:
            source = self.source.text()
            symbole = self.symbole.text()
            destination = self.destination.text()
            if not all([source, symbole, destination]):
                QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs de la transition.")
                return
            self.automate.ajouter_transition(source, symbole, destination)
            self.source.clear()
            self.symbole.clear()
            self.destination.clear()
            self.afficher_automate()
            QMessageBox.information(self, "Succès", f"La transition {source} --{symbole}--> {destination} a été ajoutée.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout de la transition : {str(e)}")

    def supprimer_transition(self):
        if not self.automate:
            QMessageBox.warning(self, "Erreur", "Veuillez d'abord créer ou charger un automate.")
            return
        try:
            source = self.source.text()
            symbole = self.symbole.text()
            destination = self.destination.text()
            if not all([source, symbole, destination]):
                QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs de la transition.")
                return
            self.automate.supprimer_transition(source, symbole, destination)
            self.source.clear()
            self.symbole.clear()
            self.destination.clear()
            self.afficher_automate()
            QMessageBox.information(self, "Succès", f"La transition {source} --{symbole}--> {destination} a été supprimée.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression de la transition : {str(e)}")

    def sauvegarder_automate(self):
        if not self.automate or not self.base_path:
            QMessageBox.warning(self, "Erreur", "Aucun automate à sauvegarder ou dossier non sélectionné.")
            return
        try:
            path = os.path.join(self.base_path, self.automate.nom, f"{self.automate.nom}.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.automate.to_dict(), f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Succès", f"L'automate a été sauvegardé dans :\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la sauvegarde : {str(e)}")

    def supprimer_automate(self):
        if not self.automate or not self.base_path:
            QMessageBox.warning(self, "Erreur", "Aucun automate à supprimer ou dossier non sélectionné.")
            return
        try:
            reponse = QMessageBox.question(self, "Confirmation",
                                         f"Êtes-vous sûr de vouloir supprimer l'automate '{self.automate.nom}' ?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reponse == QMessageBox.Yes:
                path = os.path.join(self.base_path, self.automate.nom)
                if os.path.exists(path):
                    shutil.rmtree(path)
                    self.automate = None
                    self.result.clear()
                    self.image_label.clear()
                    QMessageBox.information(self, "Succès", "L'automate a été supprimé avec succès.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression : {str(e)}")

    def revenir_accueil(self):
        self.accueil_window = AccueilWindow()
        self.accueil_window.show()
        self.close()

    def afficher_automate(self):
        if self.automate:
            # Mettre à jour la description textuelle
            self.result.setStyleSheet("""
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
            self.result.setText(str(self.automate))

            # Générer et afficher la visualisation
            try:
                image_path = self.automate.visualiser()
                if image_path and os.path.exists(image_path):
                    pixmap = QPixmap(image_path)
                    # Redimensionner l'image si elle est trop grande
                    if pixmap.width() > 800:
                        pixmap = pixmap.scaledToWidth(800, Qt.SmoothTransformation)
                    self.image_label.setPixmap(pixmap)
                    self.image_label.setStyleSheet("""
                        QLabel {
                            background-color: white;
                            border-radius: 10px;
                            padding: 10px;
                        }
                    """)
                else:
                    self.image_label.setText(
                        "Visualisation non disponible.\n\n"
                        "Pour activer la visualisation graphique, veuillez :\n"
                        "1. Installer Graphviz depuis https://graphviz.org/download/\n"
                        "2. Ajouter le dossier bin de Graphviz au PATH système\n"
                        "3. Redémarrer l'application"
                    )
                    self.image_label.setStyleSheet("""
                        QLabel {
                            background-color: #fff5f5;
                            color: #e53e3e;
                            border: 2px solid #fed7d7;
                            border-radius: 10px;
                            padding: 20px;
                            font-size: 13px;
                        }
                    """)
            except Exception as e:
                self.image_label.setText(f"Erreur de visualisation :\n{str(e)}")
                self.image_label.setStyleSheet("""
                    QLabel {
                        background-color: #fff5f5;
                        color: #e53e3e;
                        border: 2px solid #fed7d7;
                        border-radius: 10px;
                        padding: 20px;
                        font-size: 13px;
                    }
                """)
        else:
            self.result.clear()
            self.image_label.clear()
