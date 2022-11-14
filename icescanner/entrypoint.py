import time
import yaml
from typing import List
from icescanner.file_handler import FileHandler
from icescanner.logger import Logger
from icescanner.devices.camera import PortCamera, StarCamera, SternCamera, ForeCamera
from icescanner.devices.lidar import PortLidar, StarLidar, SternLidar, ForeLidar
from icescanner.thread import PropagatingThread
from icescanner.utils import parse_string_to_secs


logger = Logger.get_logger("dataset-recorder")

class Entrypoint:
    """Main class to store dataset recorder functionality.
    It uses configuration file in YAML format to control main functionality.
    Configuration example:
    ```
    common:
        shot_frequency: 1s
        root_dir: /opt/datasets

    credentials:
        cameras: &default_camera_creds
            username: user
            password: pass

    devices:
        cameras:
            port_camera:
            is_enabled: True
            ip: 192.168.1.1
            star_camera:
            is_enabled: False
            ip: 192.168.1.2
            stern_camera:
            is_enabled: True
            ip: 192.168.1.3
            fore_camera:
            is_enabled: True
            ip: 192.168.1.4
        lidars:
            port_lidar:
            is_enabled: True
            ip: 192.168.1.5
            star_lidar:
            is_enabled: True
            ip: 192.168.1.6
            stern_lidar:
            is_enabled: False
            ip: 192.168.1.7
            fore_lidar:
            is_enabled: True
            ip: 192.168.1.8
    ```

    Raises:
        Exception: common exception

    Returns:
        None
    """

    def __init__(self, config_file: str) -> None:
        """Constructor

        Args:
            config_file (str): path to configuration file
        """
        self.config = yaml.load(open(config_file).read(), Loader=yaml.FullLoader)
        self.file_handler = FileHandler(
            root_dir=self.config['common']['root_dir'],
            config=self.config)
        self.threads = []
        self._device_classes = [PortCamera, StarCamera, SternCamera, ForeCamera, PortLidar, StarLidar, SternLidar, ForeLidar]
        self._devices = []

    @property
    def devices(self) -> List:
        """Device list.
        Device may be disabled in configuration with 'is_enabled: False'
        Returns:config: Dict[Dict]={}
            List[DeviceClass]: list of initialized devices
        """
        if not self._devices:
            for _dev in self._device_classes:
                device = _dev(self.config, self.file_handler)
                if not device.is_enabled:
                    logger.warning(f"Device {device.name} is disabled")
                    continue
                self._devices.append(device)
        return self._devices

    @property
    def shot_frequency(self) -> int:
        """Timeout of data getting from devices.
        Returns:
            int: timeout
        """
        return parse_string_to_secs(self.config['common']['shot_frequency'])
    
    def take_shot(self) -> None:
        while True:
            self.file_handler.prepare_for_measurement()
            self.threads = [PropagatingThread(target=device.take_shot, name=device.name) for device in self.devices]
            for thread in self.threads:
                thread.start()
            for thread in self.threads:
                try:
                    thread.join()
                    self.file_handler.cleanup_folder()
                except Exception:
                    logger.critical(f"Got exception from {thread.name}: {thread.exc}")
                    raise Exception()
            logger.info(f"Sleeping {self.shot_frequency} secs...")
            time.sleep(self.shot_frequency)

    def do_diagnostics(self):
        for device in self.devices:
            device.do_diagnostics()
        broken_devices = [d for d in self.devices if not d.is_ok]
        if broken_devices:
            logger.critical(
                "Some devices are not working: {}".format({d.name:d.status for d in broken_devices}))
            raise Exception("Some devices are broken")
        logger.info("All devices diagnostics success!")

    def stop(self) -> None:
        for t in self.threads:
            t.join()
            logger.warning(f"stopped {t.name}")
