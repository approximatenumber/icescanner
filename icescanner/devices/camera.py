from typing import Dict
import cv2
import numpy
from icescanner.logger import Logger
from icescanner.file_handler import FileHandler
from icescanner.devices.common_device import CommonDevice
from icescanner.exceptions import DeviceDataError


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
        self.url = f"rtsp://{self.username}:{self.password}@{self.ip}:554/cam/realmonitor?channel=1&subtype=00&authbasic=[BASE64_USERNAME_PASSWORD]"
        self.status = "initialized"
        
    def take_shot(self, _format="jpg") -> None:
        """
        Main process of camera used by thread.
        It gets image from RTSP stream and saves it as a picture.
        """
        logger.info(f"Getting picture from cam: {self.name}")
        shot = cv2.VideoCapture(self.url)
        success, image = shot.read()
        if not success:
            logger.error(f"Cannot get data from camera {self.name}: {e}")
            raise DeviceDataError("Device Data error")
        self.file_handler.write_file(
            numpy.array(cv2.imencode(f'.{_format}', image)[1]).tostring(),
            f"{self.name}.{_format}",
            mode='wb')

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
