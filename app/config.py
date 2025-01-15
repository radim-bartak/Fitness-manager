import json
import os

class ConfigError(Exception):
    pass

class Config:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.load_config()

        self.validate_config()

    def load_config(self):
        if not os.path.exists(self.config_file):
            raise ConfigError(f"Konfigurační soubor '{self.config_file}' nebyl nalezen.")
        try:
            with open(self.config_file, "r") as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise ConfigError(f"Chyba při načítání JSON: {e}")

    def validate_config(self):
        required_keys = {
            "db": ["host", "user", "password", "name"],
        }

        for section, keys in required_keys.items():
            if section not in self.config:
                raise ConfigError(f"Chybí sekce '{section}' v konfiguraci.")
            for key in keys:
                if key not in self.config[section]:
                    raise ConfigError(f"Chybí klíč '{key}' v sekci '{section}'.")

    def get_database_uri(self):
        db = self.config["db"]
        return f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}/{db['name']}"

    def get_app_setting(self, key, default=None):
        return self.config["app_settings"].get(key, default)

try:
    config = Config("config.json")
    DATABASE_URI = config.get_database_uri()
    DB_HOST = config.config["db"]["host"]
    DB_USER = config.config["db"]["user"]
    DB_PASSWORD = config.config["db"]["password"]
    DB_NAME = config.config["db"]["name"]
except ConfigError as e:
    print(f"Chyba v konfiguraci: {e}")