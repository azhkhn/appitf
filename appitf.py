#! /usr/bin/env python3
"""Application interface for system interaction.

This interface provides a HTTP service to allow an
Adobe AIR or HTML5 digital signage application to
interact with the local operating system.
"""
from sys import stderr
from xml.etree import cElementTree as ElementTree

from flask import jsonify, request, Flask, Response

from backlight import brightness


APPLICATION = Flask('AppItf')


def xmlify(element):
    """Reutns an XML response."""

    return Response(ElementTree.dump(element), mimetype='application/xml')


def brightness_xml(brightness_):
    """Returns an element tree for the given brightness."""

    root = ElementTree.Element('brightness')
    root.attrib['percent'] = str(brightness_.percent)
    root.attrib['method'] = brightness_.method
    return root


def make_response(brightness_):
    """Generates a brightness response."""

    if 'xml' in request.args:
        return xmlify(brightness_xml(brightness_))

    return jsonify({
        'percent': brightness_.percent,
        'method': brightness_.method})


@APPLICATION.route('/backlight/<int:percent>', methods=['POST'])
def set_backlight(percent):
    """Sets the backlight brightness."""

    if not 0 <= percent <= 100:
        print('Got invalid percentage:', percent, file=stderr, flush=True)
        return (f'Got invalid percentage: {percent}.', 400)

    return make_response(brightness(percent))


def main(options):
    """Runs the daemon."""

    host = options['--host']
    port = options['--port']

    try:
        port = int(port)
    except ValueError:
        print(f'Port number must be an integer, not "{port}".', file=stderr,
              flush=True)
        return 1

    APPLICATION.run(host=host, port=port)
    return 0
