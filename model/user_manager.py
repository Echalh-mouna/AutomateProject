import json
import os
import re
from pathlib import Path
from datetime import datetime

class UserManager:
    def __init__(self):
        self.users_file = Path("data/users.json")
        self._ensure_data_directory()
        self.load_users()

    def _ensure_data_directory(self):
        self.users_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.users_file.exists():
            self.users_file.write_text('{}')

    def load_users(self):
        try:
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self.users = {}
            self._save_users()

    def _save_users(self):
        """Sauvegarde les utilisateurs dans le fichier JSON"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=4)
            print(f"Fichier users.json sauvegardé avec succès")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du fichier users.json: {str(e)}")
            raise

    def validate_password(self, password):
        """
        Valide que le mot de passe respecte les critères de sécurité.
        Retourne (bool, str) : (est_valide, message_erreur)
        """
        if len(password) < 8:
            return False, "Le mot de passe doit contenir au moins 8 caractères"
        
        if not re.search(r"[A-Z]", password):
            return False, "Le mot de passe doit contenir au moins une majuscule"
        
        if not re.search(r"[a-z]", password):
            return False, "Le mot de passe doit contenir au moins une minuscule"
        
        if not re.search(r"\d", password):
            return False, "Le mot de passe doit contenir au moins un chiffre"
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Le mot de passe doit contenir au moins un caractère spécial"
        
        return True, "Mot de passe valide"

    def validate_username(self, username):
        """
        Valide que le nom d'utilisateur respecte les critères.
        Retourne (bool, str) : (est_valide, message_erreur)
        """
        if len(username) < 3:
            return False, "Le nom d'utilisateur doit contenir au moins 3 caractères"
        
        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            return False, "Le nom d'utilisateur ne peut contenir que des lettres, chiffres et _"
        
        if username in self.users:
            return False, "Ce nom d'utilisateur existe déjà"
        
        return True, "Nom d'utilisateur valide"

    def register_user(self, username, password):
        """
        Enregistre un nouvel utilisateur.
        Retourne (bool, str) : (succès, message)
        """
        try:
            # Recharger les utilisateurs depuis le fichier pour avoir les données les plus récentes
            self.load_users()
            
            username_valid, username_msg = self.validate_username(username)
            if not username_valid:
                return False, username_msg
            
            password_valid, password_msg = self.validate_password(password)
            if not password_valid:
                return False, password_msg
            
            self.users[username] = {
                "password": password,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self._save_users()
            
            print(f"Utilisateur enregistré: {username}")
            print(f"Contenu de users après enregistrement: {self.users}")
            
            return True, "Inscription réussie"
        except Exception as e:
            print(f"Erreur d'enregistrement: {str(e)}")
            return False, f"Erreur lors de l'inscription: {str(e)}"

    def authenticate_user(self, username, password):
        """
        Authentifie un utilisateur.
        Retourne (bool, str) : (succès, message)
        """
        try:
            # Recharger les utilisateurs depuis le fichier pour avoir les données les plus récentes
            self.load_users()
            
            if username not in self.users:
                return False, "Nom d'utilisateur inconnu"
            
            stored_password = self.users[username]["password"]
            if password != stored_password:
                return False, "Mot de passe incorrect"
            
            return True, "Authentification réussie"
        except Exception as e:
            print(f"Erreur d'authentification: {str(e)}")
            print(f"Contenu de users: {self.users}")
            return False, f"Erreur lors de l'authentification: {str(e)}" 