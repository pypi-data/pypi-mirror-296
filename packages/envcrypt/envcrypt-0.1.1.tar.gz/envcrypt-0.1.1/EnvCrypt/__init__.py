"""
MIT License

Copyright (c) 2024 Ali Crafty

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import base64
import json
import hashlib
from cryptography.fernet import Fernet
from typing import Optional, Any
from string import Template
import os
import shutil

class Env:
    """
    A library to handle encrypted environment files using Base64, AES, and JSON, 
    with support for backups, multiple environments, and integrity checks.
    """

    def __init__(self, env_file: str, key_error_output: Optional[Any] = None, encryption_method: str = "Base64", environment: str = "default") -> None:
        """
        Initialize the Env object to load and manage data from an encrypted JSON file.

        :param env_file: Path to the environment file.
        :param key_error_output: The default value to return when a key is not found.
        :param encryption_method: The encryption method to use ("Base64" or "AES").
        :param environment: The environment (development, production, etc.).
        """
        self.env_file = f"{env_file}_{environment}.json"
        self.key_error_output = key_error_output
        self.encryption_method = encryption_method
        self.aes_key = Fernet.generate_key() if encryption_method == "AES" else None
        self.env = self._load_env()
        self.environment = environment
        self.backup_folder = "env_backups"
        self._cache = {}  # Initialize cache dictionary

    def _load_env(self) -> dict:
        """Load the data from the environment file and decode it as a dictionary."""
        try:
            if not os.path.isfile(self.env_file):
                with open(self.env_file, 'wb') as file: 
                    file.write(base64.b64encode(json.dumps({}).encode()))

            with open(self.env_file, 'r') as file:
                encoded_data = file.read()
            
            if self.encryption_method == "Base64":
                return json.loads(base64.b64decode(encoded_data))
            elif self.encryption_method == "AES":
                cipher = Fernet(self.aes_key)
                return json.loads(cipher.decrypt(encoded_data.encode()))
        except (FileNotFoundError, json.JSONDecodeError, base64.binascii.Error, ValueError) as e:
            raise ValueError(f"Error loading or decoding the environment file: {e}")

    def _save_env(self) -> None:
        """Update the environment file by saving the current values."""
        self._backup_env()  # Create a backup before saving
        try:
            if self.encryption_method == "Base64":
                encoded_data = base64.b64encode(json.dumps(self.env).encode()).decode()
            elif self.encryption_method == "AES":
                cipher = Fernet(self.aes_key)
                encoded_data = cipher.encrypt(json.dumps(self.env).encode()).decode()

            with open(self.env_file, 'w') as file:
                file.write(encoded_data)
        except Exception as e:
            raise IOError(f"Error saving environment file: {e}")
    
    def _backup_env(self) -> None:
        """Create a backup of the current environment file before modifying it."""
        if not os.path.exists(self.backup_folder):
            os.makedirs(self.backup_folder)
        
        backup_file = os.path.join(self.backup_folder, f"backup_{self.environment}.json")
        shutil.copy2(self.env_file, backup_file)
    
    def _generate_hash(self) -> str:
        """Generate a SHA-256 hash of the environment file."""
        with open(self.env_file, 'rb') as file:
            return hashlib.sha256(file.read()).hexdigest()

    def verify_integrity(self, original_hash: str) -> bool:
        """Verify the integrity of the environment file using a provided hash."""
        return original_hash == self._generate_hash()

    def _refresh_cache(self) -> None:
        """Refresh the cache with the current environment data."""
        self._cache = self.env.copy()

    def get(self, name: str) -> Any:
        """
        Retrieve a value from the dictionary by key.

        :param name: The key name.
        :return: The value associated with the key or `key_error_output` if the key is not found.
        """
        # Use cache if available
        if not self._cache:
            self._refresh_cache()
        return self._cache.get(name, self.key_error_output)

    def pop(self, name: str) -> Any:
        """
        Remove a key and its value from the dictionary and update the environment file.

        :param name: The key name.
        :return: The removed value or `key_error_output` if the key is not found.
        """
        try:
            value = self.env.pop(name)
            self._save_env()
            self._refresh_cache()  # Refresh cache after modification
            print(f"Key '{name}' has been removed successfully.")
            return value
        except KeyError:
            return self.key_error_output

    def setdefault(self, name: str, value: Any) -> Any:
        """
        Set a default value for a key if it doesn't exist and update the environment file.

        :param name: The key name.
        :param value: The default value to set for the key.
        :return: The existing value or the newly set value.
        """
        result = self.env.setdefault(name, value)
        self._save_env()
        self._refresh_cache()  # Refresh cache after modification
        return result
    
    def upsert(self, name: str, value: Any) -> Any:
        """
        Update the value for an existing key in the environment dictionary.

        If the key does not exist, the key will be added with the provided value.

        :param name: The key name to update.
        :param value: The new value to set for the key.
        :return: The updated value if the key exists or was added, otherwise `key_error_output` if there was a KeyError.
        """
        self.env[name] = value
        self._save_env()  # Save changes to file
        self._refresh_cache()  # Refresh cache after modification
        return value

    def list_env(self, format: str = "${key}: ${value}") -> list:
        """List all keys and values in the environment file."""
        out = []
        formating = Template(format)
        for key, value in self.env.items():
            data = {"key": key, "value": value}
            out.append(formating.safe_substitute(data))
        
        return out

    def switch_environment(self, new_environment: str) -> None:
        """
        Switch to a different environment by loading its corresponding file.
        
        :param new_environment: The new environment to switch to.
        """
        self.environment = new_environment
        self.env_file = f"{self.env_file.split('_')[0]}_{new_environment}.json"
        self.env = self._load_env()
        self._refresh_cache()  # Refresh cache after switching environment