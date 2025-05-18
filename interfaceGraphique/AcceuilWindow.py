from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QSize, QTimer
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QFrame,
    QHBoxLayout, QGraphicsDropShadowEffect, QScrollArea,
    QGraphicsOpacityEffect, QDesktopWidget, QApplication
)
from PyQt5.QtGui import QColor, QFont, QPalette, QLinearGradient, QGradient
from PyQt5.QtSvg import QSvgWidget

from Window.AnalyseAutomateWindow import AnalyseAutomateWindow
from Window.MotEtLanguages import MotEtLangages
from model.automate import Automate

class AnimatedLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(1000)
        self.opacity_animation.setStartValue(0)
        self.opacity_animation.setEndValue(1)
        self.opacity_animation.setEasingCurve(QEasingCurve.OutCubic)

    def showWithAnimation(self):
        self.opacity_animation.start()

class FeatureCard(QFrame):
    def __init__(self, icon, title, description, parent=None):
        super().__init__(parent)
        self.setObjectName("featureCard")
        self.setStyleSheet("""
            #featureCard {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
                border: 1px solid #e2e8f0;
            }
            #featureCard:hover {
                background-color: #f8f9fa;
                transform: translateY(-5px);
                transition: all 0.3s ease;
            }
        """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)
        
        # Layout
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 25, 20, 25)
        
        # Icon container
        icon_container = QFrame()
        icon_container.setFixedSize(120, 120)
        icon_container.setStyleSheet("""
            QFrame {
                background-color: #EBF4FF;
                border-radius: 60px;
                min-width: 120px;
                min-height: 120px;
                max-width: 120px;
                max-height: 120px;
            }
            QLabel {
                font-size: 60px;
            }
        """)
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setFont(QFont('Segoe UI Emoji', 60))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("background-color: transparent;")
        icon_layout.addWidget(icon_label)
        layout.addWidget(icon_container, alignment=Qt.AlignCenter)
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont('Segoe UI', 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin-top: 10px;")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("color: #64748b; font-size: 14px; line-height: 1.6;")
        desc_label.setMinimumHeight(80)
        layout.addWidget(desc_label)

        # Animation
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)

    def enterEvent(self, event):
        geometry = self.geometry()
        self.animation.setStartValue(geometry)
        geometry.setY(geometry.y() - 10)
        self.animation.setEndValue(geometry)
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        geometry = self.geometry()
        self.animation.setStartValue(geometry)
        geometry.setY(geometry.y() + 10)
        self.animation.setEndValue(geometry)
        self.animation.start()
        super().leaveEvent(event)

class AccueilWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.automate_courant = Automate("A1")
        self.tous_les_automates = {"A1": self.automate_courant}
        self.adjust_window_size()
        self.showAnimated()

    def adjust_window_size(self):
        screen = QDesktopWidget().screenGeometry()
        width = int(screen.width() * 0.8)
        height = int(screen.height() * 0.8)
        self.resize(width, height)
        self.center()

    def center(self):
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def showAnimated(self):
        for i, label in enumerate(self.findChildren(AnimatedLabel)):
            QTimer.singleShot(i * 200, label.showWithAnimation)

    def initUI(self):
        self.setWindowTitle("Gestionnaire d'Automates")
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                font-family: 'Segoe UI', Arial;
            }
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #2563eb;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(59, 130, 246, 0.3);
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
                transform: translateY(0px);
            }
        """)

        # Main layout with gradient background
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(40)
        main_layout.setContentsMargins(50, 50, 50, 50)

        # Header with animated elements
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setSpacing(15)
        
        # Animated title
        title = AnimatedLabel("Gestionnaire d'Automates")
        title.setFont(QFont('Segoe UI', 42, QFont.Bold))
        title.setStyleSheet("""
            color: #1e293b;
            letter-spacing: -1px;
        """)
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        # Animated subtitle
        subtitle = AnimatedLabel("Une interface moderne pour l'analyse et la manipulation d'automates")
        subtitle.setFont(QFont('Segoe UI', 16))
        subtitle.setStyleSheet("color: #64748b; margin-bottom: 20px;")
        subtitle.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle)
        
        main_layout.addWidget(header)

        # Features grid with modern layout
        features_widget = QWidget()
        features_layout = QHBoxLayout(features_widget)
        features_layout.setSpacing(30)

        # Enhanced feature cards
        features = [
            {
                "icon": "⚙️",
                "title": "Gestion Basique",
                "description": "Interface intuitive pour créer, modifier et gérer vos automates. Visualisez et manipulez facilement vos structures.",
                "slot": self.ouvrir_gestion_basique
            },
            {
                "icon": "🔍",
                "title": "Analyse d'Automates",
                "description": "Outils puissants pour analyser les propriétés et caractéristiques de vos automates. Vérifiez la déterminisation et la minimalité.",
                "slot": self.ouvrir_analyse_automate
            },
            {
                "icon": "🔤",
                "title": "Mots et Langages",
                "description": "Explorez les fonctionnalités avancées pour manipuler les mots et langages. Testez l'appartenance et générez des expressions.",
                "slot": self.mot_et_langages
            }
        ]

        for feature in features:
            card = FeatureCard(feature["icon"], feature["title"], feature["description"])
            card_container = QWidget()
            card_layout = QVBoxLayout(card_container)
            card_layout.setSpacing(15)
            card_layout.addWidget(card)
            
            button = QPushButton(f"Explorer {feature['title']}")
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(feature["slot"])
            card_layout.addWidget(button, alignment=Qt.AlignCenter)
            
            features_layout.addWidget(card_container)

        main_layout.addWidget(features_widget)

        # Modern footer with gradient
        footer = QFrame()
        footer.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f0f9ff, stop:1 #e0f2fe);
                border-radius: 15px;
                padding: 20px;
                margin-top: 20px;
            }
        """)
        footer_layout = QHBoxLayout(footer)
        footer_layout.setSpacing(20)
        
        footer_text = QLabel("© 2024 Gestionnaire d'Automates • Conçu avec ❤️ • Tous droits réservés")
        footer_text.setStyleSheet("color: #64748b; font-size: 13px;")
        footer_text.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(footer_text, stretch=1)
        
        quit_button = QPushButton("Quitter")
        quit_button.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
            QPushButton:pressed {
                background-color: #b91c1c;
            }
        """)
        quit_button.clicked.connect(QApplication.instance().quit)
        footer_layout.addWidget(quit_button)
        
        main_layout.addWidget(footer)

    def ouvrir_gestion_basique(self):
        from Window.AutomateApp import AutomateApp
        self.gestion_window = AutomateApp()
        self.gestion_window.show()
        self.close()

    def ouvrir_analyse_automate(self):
        self.analyse_window = AnalyseAutomateWindow()
        self.analyse_window.show()
        self.close()

    def mot_et_langages(self):
        self.mots_langages_window = MotEtLangages(self.automate_courant, self.tous_les_automates)
        self.mots_langages_window.show()
        self.close()
