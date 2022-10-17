from pathlib import Path
from datetime import datetime
import os
from typing import Dict
import json
from icescanner.logger import Logger


logger = Logger.get_logger("dataset-recorder")


class FileHandler():
    """Class for file handling: filenames, paths, etc.
    Used by all operators which saves data.
    """
    
    DEFAULT_METADATA = {
        "port_lidar": {},
        "star_lidar": {},
        "stern_lidar": {},
        "fore_lidar": {}
    }
    
    def __init__(self, root_dir=os.environ['HOME']) -> None:
        """Constructor

        Args:
            root_dir (str, optional): root directory to store files. Default is $HOME.
        """
        self.root_dir = root_dir
        if not os.path.isdir(self.root_dir):
            os.makedirs(self.root_dir)
            logger.info(f"Root directory created: {self.root_dir}")
        self.folder = None
    
    def get_filepath(self, filename: str) -> str:
        """Path to file to write."""
        return Path(self.folder, filename)
    
    def prepare_for_measurement(self) -> None:
        """Create folder with timestamp, where all files will be stored."""
        self.folder = os.path.join(self.root_dir, datetime.now().strftime(f"%Y%m%d_%H%M%S"))
        os.makedirs(self.folder)
        logger.info(f"Created dir {self.folder}")
        self.create_metadata_file()
        
    def write_file(self, data: str, filename: str, mode='w') -> None:
        """Write file according to data and filename.

        Args:
            data (str): data to save
            filename (str): filename to save
            mode (str): file mode
        """
        path = os.path.join(self.folder, filename)
        with open(path, mode) as f:
            f.write(data)
        logger.info(f"Written file: {path}")
        
    def create_metadata_file(self, data: Dict = DEFAULT_METADATA):
        """Create metadata file.
        Args:
            data (Dict, optional): data to write. Defaults to DEFAULT_METADATA.
        """
        filename = "metadata.json"
        path = os.path.join(self.folder, filename)
        with open(path, 'w') as f:
            json.dump(data, f)
        logger.debug(f"Created metadata file {path} with data: {data}")
    
    def update_metadata_file(self, name: str, data: Dict):
        """Create metadata file
        Args:
            name (str): name of device?
            data (Dict): data dict with meta information
        """
        filename = "metadata.json"
        path = os.path.join(self.folder, filename)
        with open(path) as f:
            json_data = json.load(f)
            logger.debug(f"Existing metadata: {json_data}")
        json_data[name].update(data)
        with open(path, 'w') as f:
            json.dump(json_data, f, indent=4)
        logger.debug(f"Metadata {path} updated with data: {json_data}")
