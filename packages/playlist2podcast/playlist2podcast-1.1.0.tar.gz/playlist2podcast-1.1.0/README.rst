Playlist2Podcast
================

|Repo| |Downloads| |Code style| |Checked against| |Checked with| |PyPI - Python Version| |PyPI - Wheel|
|CI - Woodpecker| |AGPL|


Playlist2Podcast is a command line tool that takes a Youtube playlist, downloads the audio portion of the videos on that
list, and creates a podcast feed from this.

Playlist2Podcast:

1) downloads and converts the videos in one or more playlists to opus audio only files,
2) downloads thumbnails and converts them to JPEG format, and
3) creates a podcast feed with the downloaded videos and thumbnails.

Install and run natively
------------------------

Easiest way to use Playlist2Podcast is to use `pipx` to install it from PyPi. Then you can simply use
`playlist2podcast` on the command line run it.

Playlist2Podcast will ask for all necessary parameters when run for the first time and store them in `config.json`
file in the current directory.

Docker Compose
--------------

There is a docker-image published for playlist2podcast.

You can use the below example docker compose to run playlist2podcast with a caddy frontend to publish the resulting podcast feed::

    ---
    version: "3.5"
    services:

    ##########################################################################
    # C A D D Y - R E V E R S E   P R O X Y
    ##########################################################################
       caddy:
        image: lucaslorentz/caddy-docker-proxy:latest
        container_name: caddy
        ports:
          - 80:80
          - 443:443
        environment:
          - CADDY_INGRESS_NETWORKS=caddy
        networks:
          - caddy
        volumes:
          - /var/run/docker.sock:/var/run/docker.sock
          - <path to folder where caddy can store ssl certs>:/data
          - <path to folder where caddy can write log files>:/logs
          - podcast-data:/publish:ro    # actual podcast feed data
        restart: unless-stopped

    ##########################################################################
    # P L A Y L I S T 2 P O D C A S T
    ##########################################################################
      playlist2podcast:
        image: codeberg.org/pyyttools/playlist2podcast:latest
        container_name: playlist2podcast
        tty: true
        stdin_open: true
        environment:
          - DEBUG_LOG_FILE=debug.log    # Optional: If set will create a debug log file
          - UPDATE_INTERVAL=4h          # How long to wait between updates.
       volumes:
          - <path to directory containing config.json file>:/config
          - podcast-data:/publish       # podcast feed data will be saved here
        restart: unless-stopped
        networks:
          - caddy
        labels:
          caddy: <full hostname podcast>    # DNS for this needs to resolve before starting
          caddy.root: "* /publish"
          caddy.file_server:

    ##########################################################################
    # N E T W O R K S
    ##########################################################################
    networks:
      caddy:


    ##########################################################################
    # V O L U M E S
    ##########################################################################
    volumes:
      podcast-data:


Changelog
---------

See the `Changelog`_ for any changes introduced with each version.

License
-------

Playlist2Podcast is licences under the `GNU Affero General Public License v3.0`_

.. _GNU Affero General Public License v3.0: http://www.gnu.org/licenses/agpl-3.0.html

.. |AGPL| image:: https://www.gnu.org/graphics/agplv3-with-text-162x68.png
    :alt: AGLP 3 or later
    :target: https://codeberg.org/PyYtTools/Playlist2Podcasts/src/branch/main/LICENSE.md

.. |Repo| image:: https://img.shields.io/badge/repo-Codeberg.org-blue
    :alt: Repo at Codeberg
    :target: https://codeberg.org/PyYtTools/Playlist2Podcasts

.. |Downloads| image:: https://pepy.tech/badge/playlist2podcast
    :target: https://pepy.tech/project/playlist2podcast

.. |Code style| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code Style: Black
    :target: https://github.com/psf/black

.. |Checked against| image:: https://img.shields.io/badge/Safety--DB-Checked-green
    :alt: Checked against Safety DB
    :target: https://pyup.io/safety/

.. |Checked with| image:: https://img.shields.io/badge/pip--audit-Checked-green
    :alt: Checked with pip-audit
    :target: https://pypi.org/project/pip-audit/

.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/playlist2podcast

.. |PyPI - Wheel| image:: https://img.shields.io/pypi/wheel/playlist2podcast

.. |CI - Woodpecker| image:: https://ci.codeberg.org/api/badges/PyYtTools/Playlist2Podcasts/status.svg
    :target: https://ci.codeberg.org/PyYtTools/Playlist2Podcasts

.. _Changelog: https://codeberg.org/PyYtTools/Playlist2Podcasts/src/branch/main/CHANGELOG.rst
