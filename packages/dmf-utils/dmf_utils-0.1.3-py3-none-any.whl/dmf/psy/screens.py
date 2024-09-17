

from typing import Optional, List, Union, Tuple
from psychopy import visual

DEFAULT_TEXT_COLOR = [-1, -1, -1]

class ScreenMixin:
    """Mixin class for basic methods to Display operations"""

    def screen_message(
        self,
        text: Union[str, List[str]],
        text_position: Optional[List[int]] = [0, 0],
        text_color: Optional[List[int]] = None,
        wrap_width: Optional[Union[int, float]] = 30,
        instruction_text: str = "Pulsa spacio para continuar",
        instruction_wrap_width: Optional[Union[int, float]] = 40,
        instruction_height: Optional[Union[int, float]] = 0.9,
        instruction_position: Optional[List[int]] = [0, -6],
        key_list: Optional[List[str]] = ["space"],
        min_wait: Optional[Union[int, float]] = 0.3,
        max_wait: Optional[Union[int, float]] = None,
        flip: bool = True,
    ) -> Tuple[Optional[str], Optional[float]]:
        """Show a message on the screen."""

        text_color = text_color or self.config.get("display.text", DEFAULT_TEXT_COLOR)

        if isinstance(text, list):
            for t in text:
                self.screen_message(
                    t,
                    text_position=text_position,
                    text_color=text_color,
                    wrap_width=wrap_width,
                    instruction_text=instruction_text,
                    instruction_wrap_width=instruction_wrap_width,
                    instruction_height=instruction_height,
                    instruction_position=instruction_position,
                    key_list=key_list,
                    max_wait=max_wait,
                )
            return
        

        # Draw the message
        message_stim = visual.TextStim(self.window, pos=text_position, color=text_color)
        message_stim.wrapWidth = wrap_width
        message_stim.text = text
        message_stim.draw()

        # Draw the instruction to continue
        instruction_stim = visual.TextStim(
            self.window, pos=instruction_position, color=text_color
        )
        instruction_stim.wrapWidth = instruction_wrap_width
        instruction_stim.text = instruction_text
        instruction_stim.height = instruction_height
        instruction_stim.draw()

        if flip:
            self.flip()

        if key_list:
            key, timestamp = self.wait_for_key(key_list, max_wait=max_wait, min_wait=min_wait)

        return key, timestamp
    
    def screen_fixation(
        self,
        duration: Union[int, float] = 2,
        symbol: str = "+",
        height: float = 3,
        wrap_width: float = 6,
        color: str = "black",
    ) -> None:
        """Display a fixation cross."""
        fixation = visual.TextStim(
            self.window, text=symbol, color=color, height=height, wrapWidth=wrap_width
        )
        fixation.draw()
        self.window.flip()
        self.wait(duration)

    def screen_image(
        self,
        image_path: str,
        duration: Union[int, float] = 4,
        size: Optional[int] = None,
        flip: bool = True,
        image_pos = (0, 0),
    ):
        """Show an image on the screen."""
        size = size or self.config.get("display.image_size", 20)
        image = visual.ImageStim(self.window, image_path, size=size, pos=image_pos)
        image.draw()

        # Free image from memory
        del image

        if flip:
            self.flip()

        if duration > 0:
            self.wait(duration)

    def screen_image_and_label(
        self,
        image_path: str,
        text: str = "",
        duration: Union[int, float] = 4,
        size: Optional[int] = None,
        image_pos = (0, 0),
        text_position: Optional[List[int]] = [0, -10],
        text_color: Optional[List[int]] = None,
        text_size: Optional[Union[int, float]] = 1.5,
        flip: bool = True,
    ):
        """Show an image on the screen."""
        text_color = text_color or self.config.get("display.text", DEFAULT_TEXT_COLOR)
        text = visual.TextStim(self.window, text=text, pos=text_position, color=text_color, height=text_size)
        text.draw()
        self.screen_image(image_path=image_path, duration=duration, size=size, flip=flip, image_pos=image_pos)

  
    def screen_likert(
        self,
        question: str="",
        tick_labels: list = ["1", "2", "3", "4", "5"],
        ticks=None,
        ticks_keys: list = None,
        question_wrap_width: Optional[Union[int, float]] = 40,
        question_height: Optional[Union[int, float]] = 1,
        question_position: Optional[Tuple[int, int]] = [0, 4],
        question_color: Optional[Tuple[int, int, int]] = None,
        max_wait: Optional[Union[int, float]] = None,
        min_wait: Optional[Union[int, float]] = None,
        slider_size: Optional[Tuple[int, int]] = (30, 1.5),
        slider_pos: Optional[Tuple[int, int]] = (0, 0),
        clock=None,
    ) -> int:
        """Display a question with a slider."""

        question_color = question_color or self.config.get("display.text", DEFAULT_TEXT_COLOR)
        if ticks is None:
            ticks = list(range(1, len(tick_labels) + 1))
        if ticks_keys is None:
            ticks_keys = [str(t) for t in range(1, len(tick_labels) + 1)]

        slider = visual.Slider(
            self.window,
            ticks=ticks,
            labels=tick_labels,
            granularity=1,
            size=slider_size,
            pos=slider_pos,
            color="black",
            borderColor="black",
            font="Arial",
        )
        if question:
            question_stim = visual.TextStim(
                self.window, pos=question_position, color=question_color
            )
            question_stim.wrapWidth = question_wrap_width
            question_stim.text = question
            question_stim.height = question_height
            question_stim.draw()

        slider.draw()
        self.flip()

        res, timestamp = self.wait_for_key(
            ticks_keys, max_wait=max_wait, min_wait=min_wait, clock=clock
        )
        if res is None:
            return None, None  # Max wait reached
        
        # Get key index in the list of keys
        rating_index = ticks_keys.index(res)
        rating = ticks[rating_index]
        
        return rating, timestamp