from psychopy import visual, core, event
from typing import List, Optional


class DistractorMixin:
    """Mixin to add distractor methods/screens to the experiment class."""

    def screen_reaction(
        self,
        initial_delay: float = 3,
        max_time: float = 9.999,
        final_delay: float = 2,
        rect_width: float = 10,
        rect_ratio: float = 0.5,
        text_ratio: float = 0.25,
        border_size: float = 0.8,
        background_color: str = "white",
        rect_color: str = "black",
        keys: List[str] = ["space"],
        correct_color: str = "green",
        timeout_color: str = "red",
    ):
        """
        Displays a reaction screen with a square and measures reaction time.

        A black square with a white center is displayed, and the participant is required to press a key
        as quickly as possible after it appears. The reaction time is recorded, and the square's color
        changes based on whether the response was on time or if the timeout was reached.

        Args:
            initial_delay (float, optional): Time to wait before showing the square. Defaults to 3.
            max_time (float, optional): Maximum time to wait for a response. Defaults to 9.999 seconds.
            final_delay (float, optional): Time to wait after the response is recorded. Defaults to 2.
            rect_width (float, optional): Width of the square. Defaults to 10.
            rect_ratio (float, optional): Height-to-width ratio of the square. Defaults to 0.5.
            text_ratio (float, optional): Ratio of the text size relative to the square. Defaults to 0.25.
            border_size (float, optional): Size of the square's border. Defaults to 0.8.
            background_color (str, optional): Background color of the square. Defaults to "white."
            rect_color (str, optional): Color of the square's border. Defaults to "black."
            keys (List[str], optional): List of keys to listen for during the response. Defaults to ["space"].
            correct_color (str, optional): Color to change the square and text if the response is on time. Defaults to "green."
            timeout_color (str, optional): Color to change the square and text if the response is too late or missed. Defaults to "red."

        Example:
            >>> mixin.screen_reaction(initial_delay=2, max_time=10, keys=["space"])
        """

        # Create the square and text stimuli
        square_black = visual.Rect(
            self.window,
            width=rect_width,
            height=rect_ratio * rect_width,
            fillColor=rect_color,
        )

        square_white = visual.Rect(
            self.window,
            width=rect_width - border_size,
            height=rect_ratio * rect_width - border_size,
            fillColor=background_color,
        )

        number_box = visual.TextStim(
            self.window,
            text="0.000",
            height=rect_width * text_ratio,
            color=rect_color,
        )

        # Draw the initial square on screen
        square_black.draw()
        square_white.draw()
        self.flip()

        timeout = False
        interval = core.StaticPeriod()
        interval.start(initial_delay)
        pressed, _ = self.wait_for_key(keys, max_wait=initial_delay)

        # If the key is pressed before the square appears
        if pressed:
            self.log(
                f"Pressed before the square appeared with time remaining: {interval.countdown.getTime()}"
            )
            square_black.color = timeout_color
            square_black.draw()
            square_white.draw()
            self.window.flip()
            timeout = True
            number_box.color = timeout_color

        if interval.countdown.getTime() > 0:
            interval.complete()

        del interval
        event.clearEvents()

        timestamp = None
        timer = core.Clock()
        timer.reset()

        # Reaction timing loop
        while True:
            time = timer.getTime()
            if time > max_time:
                timeout = True
                self.log(f"Timeout reached at {time} seconds")
                number_box.text = "{:.3f}".format(max_time)
                break
            number_box.text = "{:.3f}".format(time)

            # Check for key presses
            pressed_keys = event.getKeys(keyList=keys, timeStamped=timer)
            if pressed_keys:
                _, timestamp = pressed_keys[0]
                number_box.text = "{:.3f}".format(timestamp)
                self.log(f"Correctly pressed at {timestamp} seconds")
                break

            square_black.draw()
            square_white.draw()
            number_box.draw()
            self.window.flip()

        # Update square and text color based on timeout or correct response
        color = correct_color if not timeout else timeout_color
        square_black.color = color
        number_box.color = color
        square_black.draw()
        square_white.draw()
        number_box.draw()
        self.flip()

        core.wait(final_delay)
        event.clearEvents()

    def screen_counter(
        self,
        text: str = "",
        seconds: float = 10,
        text_wait: float = 1,
        height: float = 4,
        color: Optional[str] = None,
    ):
        """
        Displays a countdown screen for a short break or pause in the experiment.

        Optionally displays a message for a set amount of time before starting the countdown. A text stimulus 
        with a descending counter is updated every second. After the countdown reaches zero, the screen is cleared, 
        and the experiment proceeds.

        Args:
            text (str, optional): Optional message to display before the countdown starts. Defaults to an empty string (no message).
            seconds (float, optional): Duration of the countdown in seconds. Defaults to 10.
            text_wait (float, optional): Time to wait while displaying the message (if provided). Defaults to 1 second.
            height (float, optional): Height of the text displayed on the screen. Defaults to 4.
            color (str, optional): Color of the text. Defaults to None, which retrieves the color from the configuration or uses "black".

        Example:
            >>> display.screen_counter(text="Take a short break", seconds=5, text_wait=2)
        """

        color = color or self.config.get("display.text_color", "black")        
        countdown_text = visual.TextStim(
            self.window, text=text, height=height, color=color
        )
        if text:
            countdown_text.draw()
            self.flip()
            core.wait(text_wait)

        # Display the countdown timer
        for i in range(int(seconds), 0, -1):
            countdown_text.text = f"00:{str(i).zfill(2)}"
            countdown_text.draw()
            self.flip()
            core.wait(1)
