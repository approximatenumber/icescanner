from pathlib import Path
from datetime import datetime
import os
from lib.logger import Logger


logger = Logger.get_logger("dataset-recorder")


class FileHandler():
    """Class for file handling: filenames, paths, etc.
    Used by all operators which saves data.
    """
    
    def __init__(self, root_dir="/tmp") -> None:
        """Constructor

        Args:
            root_dir (str, optional): root directory to store files. Defaults to "/tmp".
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
        
    def write_file(self, data: str, filename: str) -> None:
        """Write file according to data and filename.

        Args:
            data (str): data to save
            filename (str): filename to save
        """
        path = os.path.join(self.folder, filename)
        with open(path, 'w') as f:
            f.write(data)
        logger.info(f"Written file: {path}")
    