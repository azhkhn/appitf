"""Application interface for system interaction.

This interface provides a HTTP service to allow an
Adobe AIR or HTML5 digital signage application to
interact with the local operating system.
"""
from argparse import ArgumentParser
from sys import stderr
from xml.etree import cElementTree as ElementTree

from flask import jsonify, request, Flask, Response

from backlight import brightness


APPLICATION = Flask('AppItf')
DESCRIPTION = 'Application interface daemon for system interaction.'


def get_args():
    """Returns the command line arguments."""

    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        '-a', '--address', default='127.0.0.1', metavar='address',
        help='IPv4 address to listen on')
    parser.add_argument(
        '-p', '--port', type=int, default=5000, metavar='port',
        help='port to listen on')
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='turn on verbose logging')
    return parser.parse_args()


def check_content_type(content_type):
    """Checks the content type against the provided content types."""

    content_types = request.headers.get('Accept', 'application/xml').split(',')

    if '*/*' in content_types:
        return True

    return any(item.startswith(content_type) for item in content_types)


def xmlify(element):
    """Reutns an XML response."""

    xml = ElementTree.tostring(element)
    return Response(xml, mimetype='application/xml')


def make_response(brightness_):
    """Generates a brightness response."""

    if check_content_type('application/xml'):
        root = ElementTree.Element('brightness')
        root.attrib['percent'] = str(brightness_.percent)
        root.attrib['method'] = brightness_.method
        return xmlify(root)

    if check_content_type('application/json'):
        return jsonify({
            'percent': brightness_.percent,
            'method': brightness_.method})

    return ('Content type not supported.', 406)


@APPLICATION.route('/backlight/<int:percent>', methods=['POST'])
def set_backlight(percent):
    """Sets the backlight brightness."""

    if not 0 <= percent <= 100:
        print('Got invalid percentage:', percent, file=stderr, flush=True)
        return (f'Got invalid percentage: {percent}.', 400)

    return make_response(brightness(percent))


def main():
    """Runs the daemon."""

    args = get_args()
    APPLICATION.run(host=args.address, port=args.port)
    return 0
