"""
$description Streamlink plugin for pickleballtv.com
$url pickleballtv.com
$type live
"""

# Place this file in ~/.local/share/streamlink/plugins/pickleballtv.py
# Streamlink will include it in its plugin list.
# Test via 'streamlink --plugins'.

import logging
import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream


log = logging.getLogger(__name__)


# Debug via:
# curl https://cdn.jwplayer.com/v2/media/kqrvUq1X | json_pp

@pluginmatcher(
    pattern=re.compile(r"https?://pickleballtv\.com"),
)
class PickleballTV(Plugin):

    def _get_streams(self):

        playlist = self.session.http.get(
            "https://cdn.jwplayer.com/v2/media/kqrvUq1X",
            schema=validate.Schema(
                validate.parse_json(),
                {
                    "playlist": [
                        {
                            "sources": [
                                {
                                    "file": validate.url(
                                        path=validate.endswith(".m3u8"),
                                    ),
                                },
                            ],
                        },
                    ],
                },
                # validate.get(("playlist", [{"sources", [{"file"},]}]))
                validate.get("playlist"),
            ),
        )
        log.debug(f"playlist: {playlist}")

        video_url = playlist[0]["sources"][0]["file"]

        if not video_url:
            log.warn("Could not find video_url")
            return

        log.info(f"Using video_url: {video_url}")

        return HLSStream.parse_variant_playlist(self.session, video_url)


__plugin__ = PickleballTV
