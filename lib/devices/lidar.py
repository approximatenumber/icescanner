from openpylivox import openpylivox
from lib.devices.common_device import CommonDevice
from lib.file_handler import FileHandler
from lib.logger import Logger



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
        logger.info(f"Lidar is ready: {self.name}")
        logger.info(f"Taking shot from lidar: {self.name}")
        self.filepath = self.file_handler.get_filepath(self.name)
        self.lidar.connect(self.config['common']['server_ip'], self.ip, 0, 0, 0)
        self.lidar.dataStart_RT_B()
        self.lidar.saveDataToFile(
            self.filepath,
            secsToWait=1,
            duration=self.config['common']['exposure'])
        while True:
            if self.lidar.doneCapturing():
                self.lidar.closeFile()
                break
        self.lidar.dataStop()
        self.lidar.disconnect()

class PortLidar(CommonLidar):
    name = "port_lidar"


class StarLidar(CommonLidar):
    name = "star_lidar"


class SternLidar(CommonLidar):
    name = "stern_lidar"


class ForeLidar(CommonLidar):
    name = "fore_lidar"
