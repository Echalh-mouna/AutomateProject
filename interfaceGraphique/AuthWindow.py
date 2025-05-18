from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import (    QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit,    QFrame, QGraphicsDropShadowEffect, QDesktopWidget,    QMessageBox, QHBoxLayout)
from PyQt5.QtGui import QColor, QFont

from interfaceGraphique.AcceuilWindow import AccueilWindow
from model.user_manager import UserManager

class PasswordLineEdit(QWidget):
    def __init__(self, placeholder="Mot de passe"):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Champ de mot de passe
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(placeholder)
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Bouton pour afficher/masquer le mot de passe
        self.toggle_button = QPushButton("👁")
        self.toggle_button.setFixedSize(40, 40)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 16px;
                padding: 0;
            }
            QPushButton:hover {
                background-color: #f1f5f9;
                border-color: #cbd5e1;
            }
            QPushButton:pressed {
                background-color: #e2e8f0;
            }
        """)
        self.toggle_button.setCursor(Qt.PointingHandCursor)
        self.toggle_button.clicked.connect(self.toggle_password_visibility)
        layout.addWidget(self.toggle_button)

    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_button.setText("🔒")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_button.setText("👁")

    def text(self):
        return self.password_input.text()

class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.user_manager = UserManager()
        self.initUI()
        self.adjust_window_size()
        # Ces fonctions seront définies par MainApplication
        self.switch_to_register_callback = None
        self.open_main_window_callback = None

    def adjust_window_size(self):
        screen = QDesktopWidget().screenGeometry()
        width = int(screen.width() * 0.3)
        height = int(screen.height() * 0.4)
        self.resize(width, height)
        self.center()

    def center(self):
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def initUI(self):
        self.setWindowTitle("Authentification")
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
            QPushButton#registerButton {
                background-color: #cbd5e1;
                color: #1e293b;
            }
            QPushButton#registerButton:hover {
                background-color: #94a3b8;
            }
            QPushButton#registerButton:pressed {
                background-color: #64748b;
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

        # Auth container avec ombre
        auth_container = QFrame()
        auth_container.setObjectName("authContainer")
        auth_container.setStyleSheet("""
            #authContainer {
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
        auth_container.setGraphicsEffect(shadow)

        # Layout du container
        container_layout = QVBoxLayout(auth_container)
        container_layout.setSpacing(20)
        container_layout.setContentsMargins(30, 30, 30, 30)

        # Titre
        title = QLabel("Bienvenue")
        title.setFont(QFont('Segoe UI', 24, QFont.Bold))
        title.setStyleSheet("color: #1e293b;")
        title.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title)

        # Sous-titre
        subtitle = QLabel("Connectez-vous à votre compte")
        subtitle.setFont(QFont('Segoe UI', 12))
        subtitle.setStyleSheet("color: #64748b;")
        subtitle.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(subtitle)

        # Champs de saisie
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        container_layout.addWidget(self.username_input)

        # Champ de mot de passe avec bouton de visibilité
        self.password_input = PasswordLineEdit()
        container_layout.addWidget(self.password_input)

        # Boutons
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)

        login_button = QPushButton("Se connecter")
        login_button.setCursor(Qt.PointingHandCursor)
        login_button.clicked.connect(self.authenticate)
        button_layout.addWidget(login_button)

        register_button = QPushButton("Pas de compte ? S'inscrire")
        register_button.setObjectName("registerButton")
        register_button.setCursor(Qt.PointingHandCursor)
        register_button.clicked.connect(self.switch_to_register)
        button_layout.addWidget(register_button)

        cancel_button = QPushButton("Annuler")
        cancel_button.setObjectName("cancelButton")
        cancel_button.setCursor(Qt.PointingHandCursor)
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)

        container_layout.addLayout(button_layout)
        main_layout.addWidget(auth_container)

    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.password_input.text()

        success, message = self.user_manager.authenticate_user(username, password)
        if success:
            if self.open_main_window_callback:
                self.open_main_window_callback()
        else:
            QMessageBox.warning(
                self,
                "Erreur d'authentification",
                message,
                QMessageBox.Ok
            )

    def switch_to_register(self):
        if self.switch_to_register_callback:
            self.switch_to_register_callback()

    def set_callbacks(self, switch_to_register_fn, open_main_window_fn):
        self.switch_to_register_callback = switch_to_register_fn
        self.open_main_window_callback = open_main_window_fn 