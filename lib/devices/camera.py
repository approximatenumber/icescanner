import cv2
import time
from typing import Dict
from lib.logger import Logger
from lib.file_handler import FileHandler


logger = Logger.get_logger("dataset-recorder")


class CommonCamera():
    """Common Camera class used a base class for specific cameras."""
    def __init__(self, config: Dict, file_handler: FileHandler) -> None:
        """Constructor

        Args:
            config (Dict): camera configuration part from main config
            file_handler (FileHandler): file handler instance
        """
        self.config = config
        self.is_enabled = self.config['devices']['cameras'][self.name]['is_enabled']
        self.file_handler = file_handler
        self.ip = self.config['devices']['cameras'][self.name]['ip']
        self.username = self.config['credentials']['cameras']['username']
        self.password = self.config['credentials']['cameras']['password']
        self.url = f"rtsp://{self.ip}:554/user={self.username}&password=${self.password}&channel=1&stream=0.sdp"
        self.is_ok = None
        self.status = "initialized"
        
    def do_diagnostics(self):
        """Provide self-check to be sure camera is ok.
        Saves cameras states according to status.
        Should be used as a first step to test camera after initialization.
        """
        logger.debug(f"Starting diagnostics for camera: {self.name}")
        if not "pingable":
            self.is_ok = False
            self.status = "Camera is unreachable over network"
        self.is_ok = True
        logger.info(f"Diagnostics success for camera: {self.name}")
    
    def run(self) -> None:
        """Main process of camera used by thread."""
        # logger.info(f"Camera is ready: {self.name}")
        logger.info(f"Getting picture from cam: {self.name}")
        self.file_handler.write_file("camera_data", f"{self.name}.png")
        time.sleep(3)
        # if not self.is_stopped:
        #     logger.info(f"Getting picture from cam: {self.name}")
        #     time.sleep(5)
        # logger.warning(f"Camera stopped: {self.name}")


class PortCamera(CommonCamera):
    """Port Camera class.

    Args:
        CommonCamera (class): common camera class
    """
    name = "port_camera"


class StarCamera(CommonCamera):
    """Star Camera class.

    Args:
        CommonCamera (class): common camera class
    """
    name = "star_camera"


class SternCamera(CommonCamera):
    """Stern Camera class.

    Args:
        CommonCamera (class): common camera class
    """
    name = "stern_camera"


class ForeCamera(CommonCamera):
    """Fore Camera class.

    Args:
        CommonCamera (class): common camera class
    """
    name = "fore_camera"
