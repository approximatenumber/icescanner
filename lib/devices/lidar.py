from openpylivox import openpylivox
from lib.devices.common_device import CommonDevice
from lib.file_handler import FileHandler
from lib.logger import Logger
from lib.utils import parse_string_to_secs
from lib.algo.input_filter import is_dataset_valid


logger = Logger.get_logger("dataset-recorder")


class CommonLidar(CommonDevice):
    def __init__(self, config: str, file_handler: FileHandler) -> None:
        super().__init__()
        self.config = config
        self.is_enabled = self.config['devices']['lidars'][self.name]['is_enabled']
        self.ip = self.config['devices']['lidars'][self.name]['ip']
        self.file_handler = file_handler
        self.lidar = openpylivox(showMessages=True, logger=logger)
        self.status = "initialized"
        self.exc = None
    
    def take_shot(self):
        """Take shot with lidar."""
        logger.info(f"Taking shot from lidar: {self.name}")
        filepath = self.file_handler.get_filepath(self.name)
        self.lidar.connect(self.config['common']['server_ip'], self.ip, 0, 0, 0)
        self.lidar.dataStart_RT_B()
        self.lidar.saveDataToFile(
            filepath,
            secsToWait=1,
            duration=parse_string_to_secs(self.config['common']['exposure']))
        while True:
            if self.lidar.doneCapturing():
                self.lidar.closeFile()
                break
        self.lidar.dataStop()
        self.lidar.disconnect()
        self.process_dataset(filepath)
        
    def process_dataset(self, filepath: str) -> None:
        """Process dataset after taking shot using algrorithm.
        Args:
            filepath (str): Path to saved file with dataset
        """
        input_filter_success = is_dataset_valid(filepath)
        metadata = {
            "input_filter_success": input_filter_success
        }
        self.file_handler.update_metadata_file(self.name, metadata)

class PortLidar(CommonLidar):
    name = "port_lidar"


class StarLidar(CommonLidar):
    name = "star_lidar"


class SternLidar(CommonLidar):
    name = "stern_lidar"


class ForeLidar(CommonLidar):
    name = "fore_lidar"
