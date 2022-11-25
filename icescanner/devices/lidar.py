from openpylivox import openpylivox
from icescanner.devices.common_device import CommonDevice
from icescanner.file_handler import FileHandler
from icescanner.logger import Logger
from icescanner.utils import parse_string_to_secs
from icescanner.algo.input_filter import is_dataset_valid


logger = Logger.get_logger("dataset-recorder")


class CommonLidar(CommonDevice):
    def __init__(self, config: str, file_handler: FileHandler) -> None:
        super().__init__()
        self.config = config
        self.is_enabled = self.config['devices']['lidars'][self.name]['is_enabled']
        self.ip = self.config['devices']['lidars'][self.name]['ip']
        self.file_handler = file_handler
        self.lidar = openpylivox(
            showMessages=True,
            logger=logger,
            debug_data=self.config['devices']['lidars'][self.name].get('debug_data', False))
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
        csv_filepath = str(filepath) + '.csv'
        self.process_dataset(csv_filepath)
        
    def process_dataset(self, filepath: str) -> None:
        """Process dataset after taking shot using algrorithm.
        Args:
            filepath (str): Path to saved file with dataset
        """
        try:
            input_filter_success = is_dataset_valid(filepath, config=self.config)
        except Exception as err:
            logger.error(f"Got exception from input filter: {err}")
            input_filter_success = False
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
