"""Data storage for Oliver the Dog."""
import json
import os
from copy import deepcopy

# Storage related global constants.
STORAGE_FILE_PATH = "./oliver_data.json"
STORAGE_FILE_TEMPLATE = {
    "posture_notice_time_seconds": 1800,    # 30 minutes
    "mention_blacklist": []
}

class OliverStorage:
    """Data storage system for Oliver the Dog."""
    def __init__(self):
        """Initializes the data storage system."""
        self.setup()
        self.data = self.load()
    
    def setup(self):
        """Create an empty data file if it doesn't exist."""
        if (not os.path.exists(STORAGE_FILE_PATH)
            or os.path.getsize(STORAGE_FILE_PATH) == 0):
            self.data = deepcopy(STORAGE_FILE_TEMPLATE)
            self.save()
    
    def save(self):
        """Update the data file with the current data."""
        with open(STORAGE_FILE_PATH, 'w') as file:
            json.dump(self.data, file)
    
    def load(self):
        """Loads the data storage file. Throws an exception if it fails."""
        with open(STORAGE_FILE_PATH, 'r+') as file:
            return json.load(file)

        raise RuntimeError("Couldn't load storage file.")