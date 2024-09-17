from typing import Optional, Union, List, Tuple
from psychopy import monitors, visual, core, event
from .config import Config, load_config
from .monitor import resolve_monitor
from .screens import ScreenMixin
from .dialog import DialogMixin
from .distractors import DistractorMixin
from .logger import get_logger

# Global display instance
DISPLAY = None
BACKGROUND_COLOR = (153 / 256, 153 / 256, 153 / 256)

def load_display(**kwargs):
    """
    Load or create a global Display instance.

    Parameters
    ----------
    **kwargs : dict
        Keyword arguments to pass to the Display constructor.

    Returns
    -------
    Display
        The global Display instance.
    """
    global DISPLAY
    if DISPLAY is None:
        DISPLAY = Display(**kwargs)
    return DISPLAY

class Display(DialogMixin, ScreenMixin, DistractorMixin):
    """
    A class representing the experimental display window and related functionalities.
    """

    def __init__(
        self,
        config: Optional[Config] = None,
        monitor: Optional[monitors.Monitor] = None,
        keyboard_refresh: float = 0.03,
        monitor_kwargs: dict = {},
        config_kwargs: dict = {},
        trigger = None
    ):
        """
        Initialize the Display.

        Parameters
        ----------
        config : Config, optional
            Configuration object.
        monitor : psychopy.monitors.Monitor, optional
            Monitor object.
        keyboard_refresh : float, optional
            Refresh rate for keyboard polling.
        monitor_kwargs : dict, optional
            Additional keyword arguments for monitor resolution.
        config_kwargs : dict, optional
            Additional keyword arguments for configuration loading.

        Notes
        -----
        It is needed call the `show` method to create the window.

        """
        self.config = config or load_config(**config_kwargs)
        self.monitor = monitor or resolve_monitor(self.config, **monitor_kwargs)
        self.keyboard_refresh = keyboard_refresh
        self.window = None
        self.clock = core.Clock()
        self.global_clock = core.Clock()
        self.trial_clock = core.Clock()
        self.logger = get_logger()
        self.trigger = trigger

    def show(
        self,
        fullscreen: Optional[bool] = None,
        background_color: Optional[tuple] = None,
        mouse_visible: bool = False,
        screen: int = 0,
        units: str = "deg",
        **kwargs,
    ) -> visual.Window:
        """
        Create and display the experiment window.

        Parameters
        ----------
        fullscreen : bool, optional
            Whether to display in fullscreen mode.
        background_color : tuple, optional
            Background color of the window.
        mouse_visible : bool, optional
            Whether the mouse cursor is visible.
        screen : int, optional
            Screen index to display the window.
        units : str, optional
            Units for window measurements.
        **kwargs : dict
            Additional keyword arguments for the visual.Window constructor.

        Returns
        -------
        visual.Window
            The created PsychoPy window.
        """
        background_color = background_color or self.config.get("display.background", BACKGROUND_COLOR)
        fullscreen = fullscreen if fullscreen is not None else self.config.get("display.fullscreen", False)

        self.window = visual.Window(
            size=self.monitor.getSizePix(),
            monitor=self.monitor,
            units=units,
            screen=screen,
            fullscr=fullscreen,
            color=background_color,
            checkTiming=False,
            **kwargs,
        )
        self.window.setMouseVisible(mouse_visible)
        return self.window

    def log(self, message: str):
        """
        Log a message to the console.

        Parameters
        ----------
        message : str
            The message to log.
        """
        print(message)

    def flip(self) -> "Display":
        """
        Flip the window buffers to update the display.

        Returns
        -------
        Display
            Returns self for method chaining.
        """
        if self.window:
            self.window.flip()
        return self

    def wait(self, duration: Union[int, float]):
        """
        Wait for a specified duration.

        Parameters
        ----------
        duration : int or float
            Duration to wait in seconds.
        """
        core.wait(duration)

    def wait_for_key(
        self,
        key_list: Optional[List[str]] = ["space"],
        clear_events: bool = True,
        max_wait: Optional[Union[int, float]] = None,
        min_wait: Optional[Union[int, float]] = None,
        clock: Optional[core.Clock] = None,
    ) -> Tuple[Optional[str], Optional[float]]:
        """
        Wait for a key press from the user.

        Parameters
        ----------
        key_list : list of str, optional
            List of keys to listen for.
        clear_events : bool, optional
            Whether to clear existing key events before waiting.
        max_wait : int or float, optional
            Maximum time to wait for a key press.
        min_wait : int or float, optional
            Minimum time to wait before accepting key presses.
        clock : psychopy.core.Clock, optional
            Clock to use for timestamping key presses.

        Returns
        -------
        tuple
            A tuple containing the key pressed and its timestamp.
        """
        self.log(f"Waiting for key: {key_list}.")
        self.clock.reset()

        if clear_events:
            event.clearEvents()
        interval = core.StaticPeriod()

        if min_wait is not None:
            core.wait(min_wait)
        timestamp_clock = clock if clock else self.clock

        while True:
            interval.start(self.keyboard_refresh)
            keys = event.getKeys(keyList=key_list, timeStamped=timestamp_clock)
            interval.complete()
            if keys:
                key, timestamp = keys[0]
                self.log(f"Key pressed: {key} ({timestamp})")
                return key, timestamp
            if max_wait is not None and self.clock.getTime() > max_wait:
                self.log("Max wait time reached.")
                return None, None

    def close(self):
        """
        Close the experiment window.
        """
        if self.window is not None:
            self.window.close()
            self.window = None

    def set_trigger(self, trigger):
        self.trigger = trigger

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
        if self.trigger is None:
            self.log("No trigger device configured.")
            return
        self.trigger.send_trigger(trigger_code)

    def screen_choice(
        self,
        options: Tuple[str, ...],
        keys: Optional[List[str]] = None,
        wrap_width: Optional[Union[int, float]] = 50,
        max_wait: Optional[Union[int, float]] = None,
        min_wait: Optional[Union[int, float]] = None,
        positions: Optional[List[List[float]]] = None,
        clock: Optional[core.Clock] = None,
        show_keys: bool = True,
        text: Optional[str] = None,
        text_position: Optional[List[float]] = [0, 6],
        text_wrap_width: Optional[Union[int, float]] = 40,
        text_height: Optional[Union[int, float]] = 1,
    ) -> Tuple[Optional[str], Optional[float], Optional[str]]:
        """
        Display a choice screen with visual buttons for the participant to select an option.

        Parameters
        ----------
        options : tuple of str
            The text labels for each option.
        keys : list of str, optional
            The keys corresponding to each option.
        wrap_width : int or float, optional
            The width at which to wrap text.
        max_wait : int or float, optional
            Maximum time to wait for a response.
        min_wait : int or float, optional
            Minimum time to wait before accepting responses.
        positions : list of list of float, optional
            Positions of the buttons on the screen.
        clock : psychopy.core.Clock, optional
            Clock to use for timestamping responses.
        show_keys : bool, optional
            Whether to display the key labels below the buttons.

        Returns
        -------
        tuple
            A tuple containing the key pressed, timestamp, and the selected option.
        """
        if keys is None:
            keys = [str(i) for i in range(1, len(options) + 1)]

        if positions is None:
            if len(options) == 2:
                positions = [[-6, 1], [6, 1]]
            elif len(options) == 3:
                positions = [[-12, 1], [0, 1], [12, 1]]
            else:
                raise ValueError(
                    f"Only two or three options are implemented ({len(options)} options provided). Please provide the positions."
                )

        if not (len(options) == len(positions) == len(keys)):
            raise ValueError("The number of options, positions, and keys must be the same.")
        
        if text:
            text_sim = visual.TextStim(
                self.window, pos=text_position, color="black"
            )
            text_sim.wrapWidth = text_wrap_width
            text_sim.text = text
            text_sim.height = text_height
            text_sim.draw()

        # Draw buttons and texts
        for option, key, position in zip(options, keys, positions):
            # Create button stimulus
            button_stim = visual.ButtonStim(
                win=self.window,
                text="",
                pos=position,
                size=(10, 5),
                color="black",
                font="Arial",
                fillColor="lightgray",
                borderColor="black",
                borderWidth=2,
                letterHeight=1.5,
                bold=False,
                anchor="center",
                padding=2.2,
            )
            # Text stimulus for the button label
            button_text = visual.TextStim(
                self.window,
                text=option,
                pos=position,
                color="black",
                font="Arial",
                height=1.5,
            )

            # Text below the button indicating the key to press
            if show_keys:
                key_label = key.upper()
                replacements = {"LEFT": "⇽", "RIGHT": "⇾", "UP": "↑", "DOWN": "↓"}
                for k, v in replacements.items():
                    key_label = key_label.replace(k, v)
                key_text = visual.TextStim(
                    self.window,
                    text=f"[{key_label}]",
                    pos=[position[0], position[1] - 4],
                    color="black",
                    wrapWidth=wrap_width,
                )
                key_text.draw()

            # Draw the buttons and text on the screen
            button_stim.draw()
            button_text.draw()

        self.flip()

        # Wait for the participant to press one of the predefined keys
        res, timestamp = self.wait_for_key(
            key_list=keys,
            max_wait=max_wait,
            min_wait=min_wait,
            clock=clock,
        )
        if res is None:
            self.log("Choice question timed out.")
            return None, None, None  # Max wait reached or no key was pressed

        if res not in keys:
            self.log(f"Invalid key pressed: {res}.")
            return res, timestamp, None

        option_index = keys.index(res)
        option = options[option_index]

        self.log(f"Choice question answered with: {res} - {option} ({timestamp})")
        return res, timestamp, option
