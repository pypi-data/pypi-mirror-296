from .logger import get_logger
from typing import Literal, Optional, Union, Any
from psychopy import core

logger = get_logger()

class Trigger:
    """
    A class for sending triggers via parallel or serial ports.

    Attributes
    ----------
    port : Literal["parallel", "serial"]
        The type of port used for sending triggers (parallel or serial).
    port_address : Any
        The address of the port (e.g., hexadecimal for parallel ports, serial port name for serial ports).
    mapping : dict, optional
        A dictionary mapping trigger names (str) to trigger codes (int).
    delay : float
        The delay in seconds between sending the trigger and resetting the port.
    _port : object
        The initialized port object (parallel or serial).
    """

    def __init__(
        self,
        port: Literal["parallel", "serial", "dummy"],
        port_address: Any = None,
        mapping: Optional[dict] = None,
        delay: float = 0.01,
        **kwargs,
    ):
        """
        Initialize the Trigger object with port type, address, and optional settings.

        Parameters
        ----------
        port : Literal["parallel", "serial"]
            The type of port (parallel or serial).
        port_address : str
            The address of the port (e.g., '0x378' for parallel ports, 'COM3' for serial).
        mapping : dict, optional
            A dictionary mapping trigger names to trigger codes, by default None.
        delay : float, optional
            The delay in seconds between sending the trigger and resetting the port, by default 0.01.
        **kwargs : dict
            Additional keyword arguments passed to the serial port if applicable.

        Examples
        --------
        Initialize a Serial port:

        >>> trigger = Trigger(port="serial", port_address="COM3", delay=0.01, baudrate=115200, timeout=0)
        """
        self.port = port
        self.port_address = port_address
        self.delay = delay
        self.mapping = mapping or {}

        # Initialize the port based on the type
        if port == "parallel":
            self._open_parallel_port(**kwargs)
        elif port == "serial":
            self._open_serial_port(**kwargs)

    def send_trigger(self, trigger_code: Union[int, str]):
        """
        Send a trigger via the configured port.

        The trigger can be provided as a string (which will be mapped to a trigger code)
        or directly as an integer. If the trigger code is not found in the mapping, an error will be logged.

        Parameters
        ----------
        trigger_code : Union[int, str]
            The trigger code to send, either as an integer or a string key mapped to an integer.
        """
        if isinstance(trigger_code, str):
            original_trigger_code = trigger_code
            trigger_code = self.mapping.get(trigger_code)
            if trigger_code is None:
                logger.error(f"Unknown trigger code: {original_trigger_code}")
                return

        # Send the trigger based on the port type
        if self.port == "parallel":
            self._send_parallel_trigger(trigger_code)
        elif self.port == "serial":
            self._send_serial_trigger(trigger_code)
        elif self.port == "dummy":
            logger.info(f"Dummy trigger sent: {trigger_code}")

    def _send_parallel_trigger(self, trigger_code: int):
        """
        Send a trigger through the parallel port.

        Parameters
        ----------
        trigger_code : int
            The trigger code to send through the parallel port.
        """
        logger.info(f"Sending parallel trigger: {trigger_code}")
        self._port.setData(trigger_code)
        core.wait(self.delay)
        self._port.setData(0)  # Reset the port after the delay

    def _open_parallel_port(self, **kwargs):
        """
        Initialize the parallel port.

        Returns
        -------
        None
        """
        from psychopy import parallel
        logger.info(f"Parallel port initialized at address {self.port_address}")
        self._port = parallel.ParallelPort(address=self.port_address, **kwargs)
        self._port.setData(0)  # Reset port at initialization

    def _open_serial_port(self, **kwargs):
        """
        Initialize the serial port with optional keyword arguments for serial configuration.

        Parameters
        ----------
        **kwargs : dict
            Additional keyword arguments for serial.Serial() initialization (e.g., baudrate, timeout).

        Returns
        -------
        None
        """
        import serial
        self._port = serial.Serial(self.port_address, **kwargs)
        logger.info(f"Serial port initialized at address {self.port_address}")
        self._port.write(b"\x00")  # Send a reset command to the serial port

    def _send_serial_trigger(self, trigger_code: int):
        """
        Send a trigger through the serial port.

        Parameters
        ----------
        trigger_code : int
            The trigger code to send through the serial port.
        """
        logger.info(f"Sending serial trigger: {trigger_code}")
        trigger_bytes = trigger_code.to_bytes(1, 'big')  # Convert to a single byte
        self._port.write(trigger_bytes)
        core.wait(self.delay)
        self._port.write(b"\x00")  # Reset the port
