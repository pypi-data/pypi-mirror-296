# GitHub Database

A Python package for custom databases powered by GitHub, with encryption using `cryptography`. It allows you, as a python developer to have a quick and easy to use database without learning a whole new programming language.

## Installation

Install via pip:

```bash
pip install gitbase
```

Example code: 

```py
from gitbase.database import GitHubDatabase, PlayerDataSystem, DataSystem
from cryptography.fernet import Fernet

# Initialize GitHub database and encryption key
token = "your_github_token"
repo_owner = "your_repo_owner"
repo_name = "your_repo_name"
key = Fernet.generate_key()

db = GitHubDatabase(token, repo_owner, repo_name)
player_data_system = PlayerDataSystem(db, key)
data_system = DataSystem(db, key)

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

# Save a piece of data using a key and value pair
data_system.save_data(key="key_name", value=69)

# Load the value of a specific key by its name
key_1 = data_system.load_data(key="key_name")

# Print the key
print(key_1)
```