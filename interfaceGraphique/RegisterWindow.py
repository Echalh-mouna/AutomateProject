from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit,
    QFrame, QGraphicsDropShadowEffect, QDesktopWidget,
    QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QColor, QFont

from model.user_manager import UserManager
from interfaceGraphique.AuthWindow import PasswordLineEdit

class RegisterWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.user_manager = UserManager()
        self.initUI()
        self.adjust_window_size()
        # Cette fonction sera définie par MainApplication
        self.switch_to_login_callback = None

    def adjust_window_size(self):
        screen = QDesktopWidget().screenGeometry()
        width = int(screen.width() * 0.3)
        height = int(screen.height() * 0.5)
        self.resize(width, height)
        self.center()

    def center(self):
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def initUI(self):
        self.setWindowTitle("Inscription")
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                font-family: 'Segoe UI', Arial;
            }
            QLineEdit {
                padding: 12px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 14px;
                background-color: #f8fafc;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
                background-color: white;
            }
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
            QPushButton#cancelButton {
                background-color: #ef4444;
            }
            QPushButton#cancelButton:hover {
                background-color: #dc2626;
            }
            QPushButton#cancelButton:pressed {
                background-color: #b91c1c;
            }
        """)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Container avec ombre
        container = QFrame()
        container.setObjectName("container")
        container.setStyleSheet("""
            #container {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #e2e8f0;
            }
        """)

        # Ajouter l'ombre
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 4)
        container.setGraphicsEffect(shadow)

        # Layout du container
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(20)
        container_layout.setContentsMargins(30, 30, 30, 30)

        # Titre
        title = QLabel("Créer un compte")
        title.setFont(QFont('Segoe UI', 24, QFont.Bold))
        title.setStyleSheet("color: #1e293b;")
        title.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title)

        # Champs de saisie
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        container_layout.addWidget(self.username_input)

        # Champs de mot de passe avec boutons de visibilité
        self.password_input = PasswordLineEdit("Mot de passe")
        container_layout.addWidget(self.password_input)

        self.confirm_password_input = PasswordLineEdit("Confirmer le mot de passe")
        container_layout.addWidget(self.confirm_password_input)

        # Critères du mot de passe
        password_criteria = QLabel(
            "Le mot de passe doit contenir :\n"
            "• Au moins 8 caractères\n"
            "• Au moins une majuscule\n"
            "• Au moins une minuscule\n"
            "• Au moins un chiffre\n"
            "• Au moins un caractère spécial (!@#$%^&*(),.?\":{}|<>)"
        )
        password_criteria.setStyleSheet("color: #64748b; font-size: 12px;")
        password_criteria.setAlignment(Qt.AlignLeft)
        container_layout.addWidget(password_criteria)

        # Boutons
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)

        register_button = QPushButton("S'inscrire")
        register_button.setCursor(Qt.PointingHandCursor)
        register_button.clicked.connect(self.register)
        button_layout.addWidget(register_button)

        login_button = QPushButton("Déjà inscrit ? Se connecter")
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #cbd5e1;
                color: #1e293b;
            }
            QPushButton:hover {
                background-color: #94a3b8;
            }
            QPushButton:pressed {
                background-color: #64748b;
            }
        """)
        login_button.setCursor(Qt.PointingHandCursor)
        login_button.clicked.connect(self.switch_to_login)
        button_layout.addWidget(login_button)

        container_layout.addLayout(button_layout)
        main_layout.addWidget(container)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.password_input.text()
        confirm_password = self.confirm_password_input.password_input.text()

        if password != confirm_password:
            QMessageBox.warning(
                self,
                "Erreur",
                "Les mots de passe ne correspondent pas.",
                QMessageBox.Ok
            )
            return

        success, message = self.user_manager.register_user(username, password)
        if success:
            QMessageBox.information(
                self,
                "Succès",
                "Inscription réussie ! Vous pouvez maintenant vous connecter.",
                QMessageBox.Ok
            )
            if self.switch_to_login_callback:
                self.switch_to_login_callback()
        else:
            QMessageBox.warning(
                self,
                "Erreur",
                message,
                QMessageBox.Ok
            )

    def switch_to_login(self):
        if self.switch_to_login_callback:
            self.switch_to_login_callback()

    def set_callbacks(self, switch_to_login_fn):
        self.switch_to_login_callback = switch_to_login_fn 