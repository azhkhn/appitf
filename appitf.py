"""Application interface for system interaction.

This interface provides a WSGI service to allow an
Adobe AIR or HTML5 digital signage application to
interact with the local operating system.
"""

from flask import Flask

from backlight.api import NoSupportedGraphicsCards, Backlight


APP = Flask('AppItf')


@APP.route('/brightness/<int:brightness>', methods=['POST'])
def set_brightness(brightness):
    """Sets the display brightness."""

    if 0 <= brightness <= 100:
        try:
            backlight = Backlight.load()
        except NoSupportedGraphicsCards:
            return ('No supported graphics card found.', 503)

        backlight.percent = brightness
        return f'Brightness set to {brightness}%.'

    return (f'Brightness must be between 0 and 100.', 400)
