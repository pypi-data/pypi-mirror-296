# GitHub Database

A Python package for saving and loading player data on GitHub, with encryption using `cryptography`. It allows selective saving of class attributes.

## Installation

Install via pip:

```bash
pip install gitbase
```

Example code: 

```py
from github_database import GitHubDatabase, PlayerDataSystem
from cryptography.fernet import Fernet

# Initialize GitHub database and encryption key
token = "your_github_token"
repo_owner = "your_repo_owner"
repo_name = "your_repo_name"
key = Fernet.generate_key()

db = GitHubDatabase(token, repo_owner, repo_name)
player_data_system = PlayerDataSystem(db, key)

# Player instance with some attributes
class Player:
    def __init__(self, username, score):
        self.username = username
        self.score = score

player = Player("john_doe", 100)

# Save specific attributes of the player instance
player_data_system.save_player_data("john_doe", player, attributes=["username", "score"])

# Load player data
player_data_system.load_player_data("john_doe", player)
```