import argparse
import sys
from pathlib import Path
from . import send_alert, send_message

def main():
    parser = argparse.ArgumentParser(
        description="Command-line tool to send alerts using DMF alert system."
    )

    parser.add_argument(
        'text',
        nargs='?',
        type=str,
        help='The text message to send as an alert. If not provided, text is read from stdin.'
    )
    parser.add_argument(
        '-a', '--attachment',
        type=Path,
        help='Optional: Path to the file to attach.'
    )
    parser.add_argument(
        '-l', '--level',
        type=str,
        choices=['success', 'info', 'warning', 'error'],
        default=None,
        help=argparse.SUPPRESS  # Hide this from the help documentation
    )
    parser.add_argument(
        '-p', '--param',
        action='append',
        help="Optional: Named parameters to include in the alert, specified as key=value pairs."
    )

    args = parser.parse_args()

    # Read text from stdin if not provided as an argument
    if args.text is None:
        args.text = sys.stdin.read().strip()

    # Process params into a dictionary
    params = {}
    if args.param:
        for param in args.param:
            key, value = param.split('=', 1)
            params[key] = value

    # Determine which function to call based on the presence of params and level
    if not params and args.level is None:
        # Use send_message if no params and no level are provided
        send_message(text=args.text, attachment=args.attachment)
    else:
        # Use send_alert if params or level are provided
        send_alert(text=args.text, attachment=args.attachment, level=args.level, params=params)

if __name__ == "__main__":
    main()
