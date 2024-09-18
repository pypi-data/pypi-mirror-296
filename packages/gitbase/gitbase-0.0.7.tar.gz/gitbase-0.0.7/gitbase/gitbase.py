import requests
import json
import base64
from cryptography.fernet import Fernet
from typing import Optional, Tuple, Union, Dict
from altcolor.altcolor import colored_text

data_loaded: bool = False

class GitHubDatabase:
    def __init__(self, token: str, repo_owner: str, repo_name: str, branch: str = 'main') -> None:
        self.token: str = token
        self.repo_owner: str = repo_owner
        self.repo_name: str = repo_name
        self.branch: str = branch
        self.headers: Dict[str, str] = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def _get_file_url(self, path: str) -> str:
        """Generate the URL for a specific file in the repository."""
        return f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{path}"

    def _get_file_content(self, path: str) -> Tuple[Optional[str], Optional[str]]:
        """Retrieve the content of a file from the repository."""
        url: str = self._get_file_url(path)
        response: requests.Response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            file_data: Dict[str, Union[str, bytes]] = response.json()
            sha: str = file_data['sha']
            content: str = base64.b64decode(file_data['content']).decode('utf-8')
            return content, sha
        return None, None

    def read_data(self, path: str) -> Tuple[Optional[str], Optional[str]]:
        """Read and return data from the GitHub repository."""
        content, sha = self._get_file_content(path)
        return content, sha

    def write_data(self, path: str, data: str, message: str = "Updated data") -> int:
        """Create or update a file in the GitHub repository."""
        url: str = self._get_file_url(path)
        content, sha = self._get_file_content(path)
        
        # Encode data as base64
        encoded_data: str = base64.b64encode(data.encode('utf-8')).decode('utf-8')
        
        payload: Dict[str, Union[str, None]] = {
            "message": message,
            "content": encoded_data,
            "branch": self.branch
        }
        
        if sha:  # If file exists, update it
            payload["sha"] = sha

        response: requests.Response = requests.put(url, headers=self.headers, json=payload)
        return response.status_code

    def delete_data(self, path: str, message: str = "Deleted data") -> int:
        """Delete a file from the GitHub repository."""
        url: str = self._get_file_url(path)
        _, sha = self._get_file_content(path)
        
        if sha:  # If file exists, delete it
            payload: Dict[str, str] = {
                "message": message,
                "sha": sha,
                "branch": self.branch
            }

            response: requests.Response = requests.delete(url, headers=self.headers, json=payload)
            return response.status_code
        else:
            return 404  # File not found

class PlayerDataSystem:
    def __init__(self, db: GitHubDatabase, encryption_key: bytes) -> None:
        self.db: GitHubDatabase = db
        self.encryption_key: bytes = encryption_key  # The encryption key (symmetric key)
        self.fernet: Fernet = Fernet(self.encryption_key)

    def encrypt_data(self, data: str) -> bytes:
        """Encrypt data using the provided encryption key."""
        return self.fernet.encrypt(data.encode('utf-8'))

    def decrypt_data(self, encrypted_data: bytes) -> str:
        """Decrypt data using the provided encryption key."""
        return self.fernet.decrypt(encrypted_data).decode('utf-8')

    def save_player_data(self, username: str, player_instance: object, attributes: Optional[list[str]] = None) -> None:
        """
        Save specified attributes of a class to a file, encrypted.
        If no attributes are specified, all attributes will be saved.
        """
        if attributes:
            player_data: Dict[str, Union[str, int, float]] = {var: getattr(player_instance, var) for var in attributes if hasattr(player_instance, var)}
        else:
            player_data: Dict[str, Union[str, int, float]] = {var: getattr(player_instance, var) for var in player_instance.__dict__}

        # Serialize and encrypt the data
        encrypted_data: bytes = self.encrypt_data(json.dumps(player_data))

        # Save the encrypted data to GitHub
        path: str = f"players/{username}.json"
        self.db.write_data(path, encrypted_data.decode('utf-8'), message=f"Saved data for {username}")

    def load_player_data(self, username: str, player_instance: object) -> None:
        """Load and assign all variables back to the class instance."""
        path: str = f"players/{username}.json"
        encrypted_data, _ = self.db.read_data(path)

        if encrypted_data:
            # Decrypt and deserialize the data
            decrypted_data: str = self.decrypt_data(encrypted_data.encode('utf-8'))
            player_data: Dict[str, Union[str, int, float]] = json.loads(decrypted_data)

            # Assign the variables back to the class instance
            for var, value in player_data.items():
                setattr(player_instance, var, value)

            print(colored_text("GREEN", f"Data loaded and assigned for {username}"))
        else:
            print(colored_text("RED", f"No data found for {username}"))
    
    def delete_account(self, username: str) -> int:
        """Delete an account"""
        path: str = f"players/{username}.json"
        return self.db.delete_data(path, message=f"Deleted account '{username}'")

class DataSystem:
    def __init__(self, db: GitHubDatabase, encryption_key: bytes) -> None:
        self.db: GitHubDatabase = db
        self.encryption_key: bytes = encryption_key  # The encryption key (symmetric key)
        self.fernet: Fernet = Fernet(self.encryption_key)

    def encrypt_data(self, data: str) -> bytes:
        """Encrypt data using the provided encryption key."""
        return self.fernet.encrypt(data.encode('utf-8'))

    def decrypt_data(self, encrypted_data: bytes) -> str:
        """Decrypt data using the provided encryption key."""
        return self.fernet.decrypt(encrypted_data).decode('utf-8')

    def save_data(self, key: str, value: any) -> None:
        """
        Save specified value under a key.
        """

        # Serialize and encrypt the data
        encrypted_data: bytes = self.encrypt_data(json.dumps(value))

        # Save the encrypted data to GitHub
        path: str = f"{key}.json"
        self.db.write_data(path, encrypted_data.decode('utf-8'), message=f"Saved {key}")

    def load_data(self, key: str) -> Optional[any]:
        """Get the value of a data key"""
        path: str = f"{key}.json"
        encrypted_data, _ = self.db.read_data(path)

        if encrypted_data:
            # Decrypt and deserialize the data
            decrypted_data: str = self.decrypt_data(encrypted_data.encode('utf-8'))

            return json.loads(decrypted_data)
        else:
            return None

    def delete_data(self, key: str) -> int:
        """Delete a data key and its associated file."""
        path: str = f"{key}.json"
        return self.db.delete_data(path, message=f"Deleted {key}")
