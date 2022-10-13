import subprocess
from lib.exceptions import DeviceUnreachableError
from lib.logger import Logger
from lib.wrappers import retry


logger = Logger.get_logger("dataset-recorder")


class CommonDevice():
    def __init__(self) -> None:
        self.is_ok = True

    @retry(exception_class=DeviceUnreachableError, retries=3, time_between_retries=1)
    def do_diagnostics(self) -> None:
        """Provide self-check to be sure device is ok.
        Saves device state into `self.is_ok` variable according to status.
        Should be used as a first step for device after initialization.
        """
        logger.debug(f"Starting diagnostics for lidar: {self.name}")
        if not self._is_device_pingable():
            self.is_ok = False
            raise DeviceUnreachableError(f"{self.name} ({self.ip}) is unreachable!")
        logger.info(f"Diagnostics success for lidar: {self.name}")

    def _is_device_pingable(self) -> bool:
        """Run ping command to test if device is online."""
        command = ['ping', '-w', '1', '-c', '1', self.ip]
        logger.debug(f"pinging device with command: {command}")
        ping = subprocess.Popen(['ping', '-w', '1', '-c', '1', self.ip], stdout=subprocess.PIPE)
        logger.debug(ping.communicate())
        return ping.returncode == 0
