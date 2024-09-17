import re
from typing import Optional, Dict, Any, List
from psychopy import gui
from .exceptions import ExperimentStopped

def dialog_form(
    information: Dict[str, Dict[str, Any]],
    title: Optional[str] = None,
    cancel_message: str = "User cancelled input information.",
) -> Dict[str, Any]:
    """
    Display a dialog to request subject information based on a given information dictionary.

    This function creates a dialog window using PsychoPy's GUI module, allowing the user to input
    or select information as specified in the `information` dictionary. It supports text input,
    fixed fields, dropdown selections, and regex validation.

    Parameters
    ----------
    information : dict
        A dictionary where each key corresponds to a field in the dialog. The value for each key
        is another dictionary that can contain the following optional keys:
        - `'label'`: str, the label to display for this field (default is the key itself).
        - `'default'`: Any, the default value for this field (default is an empty string).
        - `'regex'`: str, a regular expression pattern to validate the input (default is `None`).
        - `'fixed'`: bool, whether the field is read-only (default is `False`).
        - `'choices'`: list, if provided, the field will be a dropdown menu with these choices.

    title : str, optional
        The title of the dialog window. If not provided, no title will be displayed.

    cancel_message : str, optional
        The message of the exception if the user cancels the dialog or if input validation fails.
        Defaults to "User cancelled input information."

    Returns
    -------
    dict
        A dictionary containing the user's input, with keys corresponding to those in the
        `information` dictionary.

    Raises
    ------
    ExperimentStopped
        If the user cancels the dialog or if input validation fails due to regex mismatch.
    """

    # Separate fields with and without choices
    info_choices = {k: v for k, v in information.items() if "choices" in v}
    info_fields = {k: v for k, v in information.items() if "choices" not in v}

    # Prepare the dialog data
    info = {k: v.get("default", "") for k, v in info_fields.items()}
    labels = {k: v.get("label", k) for k, v in info_fields.items()}
    labels.update({k: v.get("label", k) for k, v in info_choices.items()})
    regex_patterns = {k: v.get("regex") for k, v in info_fields.items()}
    fixed_fields = [k for k, v in info_fields.items() if v.get("fixed", False)]

    try:
        # Create the dialog
        dialog = gui.DlgFromDict(
            dictionary=info,
            title=title,
            fixed=fixed_fields,
            labels=labels,
            show=False
        )

        # Add choice fields
        for k, v in info_choices.items():
            choices = v.get("choices", ["-"])
            initial = v.get("default", choices[0])
            # label = v.get("label", k)
            dialog.addField(k, initial=initial, choices=choices)

        dialog.show()

    except KeyboardInterrupt:
        raise ExperimentStopped(cancel_message)

    if not dialog.OK:
        raise ExperimentStopped(cancel_message)

    # Validate input using regex patterns
    for k, pattern in regex_patterns.items():
        if pattern is not None and not re.match(pattern, info[k]):
            raise ExperimentStopped(f"Invalid {k} format: {info[k]}.")

    
    return info

def dialog_accept(message: str, title: Optional[str] = None, **kwargs) -> Optional[bool]:
    """
    Display a dialog with a message and Yes/No buttons.

    Returns `True` for 'Yes', `False` for 'No', and `None` if the window is closed.
    """
    dialog = gui.Dlg(title=title, **kwargs)
    dialog.addText(message)
    user_response = dialog.show()
    
    if dialog.OK:
        return True
    elif user_response is None:
        # Dialog was closed using the window's close button
        return None
    else:
        return False
    
class DialogMixin:
    """Mixin class for dialogs in PsychoPy."""

    def dialog_form(self, information: Dict[str, Dict[str, Any]], title: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Display an information dialog."""
        return dialog_form(information, title=title, **kwargs)
    
    def dialog_accept(self, message: str, title: Optional[str] = None, **kwargs) -> Optional[bool]:
        """Display an accept dialog."""
        return dialog_accept(message, title=title, **kwargs)
    