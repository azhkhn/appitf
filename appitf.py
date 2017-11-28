"""Application interface for system interaction.

This interface provides a WSGI service to allow an
Adobe AIR or HTML5 digital signage application to
interact with the local operating system.
"""

from flask import Flask

from backlight import NoSupportedGraphicsCards, Backlight


APP = Flask('AppItf')


@APP.route('/brightness/<int:brightness>', methods=['POST'])
def set_brightness(brightness):
    """Sets the display brightness."""

    try:
        backlight = Backlight.load()
    except NoSupportedGraphicsCards:
        return ('No supported graphics card found.', 503)

    try:
        backlight.percent = brightness
    except ValueError as value_error:
        return (str(value_error), 400)
    except PermissionError:
        return ('Service is not running as root.', 500)

    return f'Brightness set to {brightness}%.'
