import cv2
from typing import Dict
from lib.logger import Logger
from lib.file_handler import FileHandler
from lib.devices.common_device import CommonDevice


logger = Logger.get_logger("dataset-recorder")


class CommonCamera(CommonDevice):
    """Common Camera class used a base class for specific cameras."""
    def __init__(self, config: Dict, file_handler: FileHandler) -> None:
        """Constructor

        Args:
            config (Dict): camera configuration part from main config
            file_handler (FileHandler): file handler instance
        """
        super().__init__()
        self.config = config
        self.file_handler = file_handler
        self.is_enabled = self.config['devices']['cameras'][self.name]['is_enabled']
        self.ip = self.config['devices']['cameras'][self.name]['ip']
        self.username = self.config['credentials']['cameras']['username']
        self.password = self.config['credentials']['cameras']['password']
        self.url = f"rtsp://{self.ip}:554/user={self.username}&password=${self.password}&channel=1&stream=0.sdp"
        self.status = "initialized"
        
    def take_shot(self) -> None:
        """Main process of camera used by thread."""
        logger.info(f"Camera is ready: {self.name}")
        logger.info(f"Getting picture from cam: {self.name}")
        # paste your code
        self.file_handler.write_file("camera_data", f"{self.name}.png")


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
