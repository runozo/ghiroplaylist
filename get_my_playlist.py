#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
from collections import OrderedDict
from gmusicapi import Mobileclient


class GmusicClient(object):
    """Implements a client for gmusic."""

    def __init__(self, user, password, phone_id):
        self.api = Mobileclient()
        self.api.login(user, password, phone_id)
        self.playlists = self.api.get_all_user_playlist_contents()

    def get_all_playlists(self):
        """Gets all the tracks in all the playlists."""
        playlists = {}
        for pl in self.playlists:
            playlists[pl['name']] = []
            for track in pl['tracks']:
                if 'track' in track:
                    playlists[pl['name']].append({
                        'title': track['track']['title'],
                        'artist': track['track']['artist'],
                        'album': track['track']['album']
                    })
        return OrderedDict(sorted(playlists.items(), key=lambda t: t[0]))

class MarkDownRenderer(object):
    """Renders a list of playlists in markdown format."""
    def __init__(self, playlists):
        self.playlists = playlists

    def render(self):
        """Renders the page in markdown."""
        page = u'# My playlists:\n'
        toc = u''
        plist = ''
        for k, playlist in self.playlists.items():
            toc += '* [%s](#%s)\n' % (k, k.lower()
                .replace('& ', '-')
                .replace(' ', '-')
                .replace('/', '')
            ) 
            plist += "## %s\n" % k
            for track in playlist:
                plist += '* %s - %s - %s\n' % (track['artist'], track['album'], track['title'])
        return page + toc + plist


if __name__ == '__main__':
    os.environ["PYTHONWARNINGS"] = "ignore:Unverified HTTPS request"
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("username", type=str,
                    help="gmusic username")
    parser.add_argument("password", type=str,
                    help="gmusic password")
    parser.add_argument("phone_id", type=str,
                    help="your android id")
    args = parser.parse_args()
    c = GmusicClient(args.username, args.password, args.phone_id)
    m = MarkDownRenderer(c.get_all_playlists())
    page = m.render()
    print(page)
    with open('README.md', mode='w') as readme:
        readme.write(page)

