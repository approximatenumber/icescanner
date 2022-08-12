import time
from threading import Thread
from lib.file_handler import FileHandler
from lib.logger import Logger


logger = Logger.get_logger("dataset-recorder")


class CommonLidar():
    def __init__(self, config: str, file_handler: FileHandler) -> None:
        self.config = config
        self.is_enabled = self.config['devices']['lidars'][self.name]['is_enabled']
        self.file_handler = file_handler
        self.is_ok = None
        self.status = "initialized"
        self.exc = None
    
    def run(self):
        logger.info(f"Lidar is ready: {self.name}")
        logger.info(f"Taking shot from lidar: {self.name}")
        time.sleep(5)
        logger.warning(f"Lidar stopped: {self.name}")

    def do_diagnostics(self):
        """Provide self-check to be sure lidar is ok.
        Saves lidar states according to status.
        Should be used as a first step to test lidar after initialization.
        """
        logger.debug(f"Starting diagnostics for lidar: {self.name}")
        if not "pingable":
            self.is_ok = False
            self.status = "Lidar is unreachable over network"
        self.is_ok = True
        logger.info(f"Diagnostics success for lidar: {self.name}")
        
    def run(self):
        logger.info(f"Getting dataset from lidar: {self.name}")
        self.file_handler.write_file("lidar_data", f"{self.name}.csv")
        time.sleep(1)


class PortLidar(CommonLidar):
    name = "port_lidar"


class StarLidar(CommonLidar):
    name = "star_lidar"


class SternLidar(CommonLidar):
    name = "stern_lidar"


class ForeLidar(CommonLidar):
    name = "fore_lidar"
