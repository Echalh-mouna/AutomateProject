from PyQt5.QtWidgets import QApplication
from interfaceGraphique.AuthWindow import AuthWindow
from interfaceGraphique.AcceuilWindow import AccueilWindow
from interfaceGraphique.RegisterWindow import RegisterWindow

class MainApplication:
    def __init__(self):
        self.auth_window = None
        self.register_window = None
        self.main_window = None
        self.current_window = None

    def start(self):
        """Démarre l'application avec la fenêtre d'authentification"""
        self.show_auth_window()

    def show_auth_window(self):
        """Affiche la fenêtre d'authentification"""
        if self.current_window:
            self.current_window.hide()
        
        if not self.auth_window:
            self.auth_window = AuthWindow()
            self.auth_window.set_callbacks(
                switch_to_register_fn=self.show_register_window,
                open_main_window_fn=self.show_main_window
            )
        
        self.auth_window.show()
        self.current_window = self.auth_window

    def show_register_window(self):
        """Affiche la fenêtre d'inscription"""
        if self.current_window:
            self.current_window.hide()
        
        if not self.register_window:
            self.register_window = RegisterWindow()
            self.register_window.set_callbacks(
                switch_to_login_fn=self.show_auth_window
            )
        
        self.register_window.show()
        self.current_window = self.register_window

    def show_main_window(self):
        """Affiche la fenêtre principale"""
        if self.current_window:
            self.current_window.hide()
        
        if not self.main_window:
            self.main_window = AccueilWindow()
        
        self.main_window.show()
        self.current_window = self.main_window 