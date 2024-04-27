# -*- coding: utf-8 -*-
'''
    feedgen
    ~~~~~~~

    :copyright: 2013-2024, Lars Kiesow <lkiesow@uos.de>

    :license: FreeBSD and LGPL, see license.* for more details.
'''

import sys

from feedgen.feed import FeedGenerator


USAGE = '''
Usage: python -m feedgen [OPTION]

Use one of the following options:

File options:
  <file>.atom      -- Generate ATOM test feed
  <file>.rss       -- Generate RSS test teed

Stdout options:
  atom             -- Generate ATOM test output
  rss              -- Generate RSS test output
  podcast          -- Generate Podcast test output
  dc.atom          -- Generate DC extension test output (atom format)
  dc.rss           -- Generate DC extension test output (rss format)
  syndication.atom -- Generate syndication extension test output (atom format)
  syndication.rss  -- Generate syndication extension test output (rss format)
  torrent          -- Generate Torrent test output

'''


def print_enc(s):
    '''Print function compatible with both python2 and python3 accepting
    strings and byte arrays.
    '''
    if sys.version_info[0] >= 3:
        print(s.decode('utf-8') if isinstance(s, bytes) else s)
    else:
        print(s)


def main():
    if len(sys.argv) != 2 or not (
            sys.argv[1].endswith('rss') or
            sys.argv[1].endswith('atom') or
            sys.argv[1] == 'torrent' or
            sys.argv[1] == 'podcast'):
        print(USAGE)
        exit()

    arg = sys.argv[1]

    fg = FeedGenerator()
    fg.id('https://example.com/feed.xml')
    fg.title('A Feed')
    fg.author({'name': 'John Doe', 'email': 'jdoe@example.com'})
    fg.link(href='https://example.com', rel='alternate')
    fg.category(term='test')
    fg.contributor(name='John Doe', email='jdoe@example.com')
    fg.contributor(name='Jane Doe', email='jdoe@example.net')
    fg.icon('https://example.com/icon.jpg')
    fg.logo('https://example.com/logo.jpg')
    fg.rights('cc-by')
    fg.subtitle('This is a cool feed!')
    fg.link(href='https://example.com/feed.xml', rel='self')
    fg.language('de')
    fe = fg.add_entry()
    fe.id('https://example.com/entry')
    fe.title('First Element')
    fe.content('''Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            Tamen aberramus a proposito, et, ne longius, prorsus, inquam, Piso,
            si ista mala sunt, placet. Aut etiam, ut vestitum, sic sententiam
            habeas aliam domesticam, aliam forensem, ut in fronte ostentatio
            sit, intus veritas occultetur? Cum id fugiunt, re eadem defendunt,
            quae Peripatetici, verba.''')
    fe.summary(u'Lorem ipsum dolor sit amet, consectetur adipiscing elit…')
    fe.link(href='https://example.com/entry', rel='alternate')
    fe.author(name='John Doe', email='jdoe@example.com')

    if arg == 'atom':
        print_enc(fg.atom_str(pretty=True))
    elif arg == 'rss':
        print_enc(fg.rss_str(pretty=True))
    elif arg == 'podcast':
        # Load the podcast extension. It will automatically be loaded for all
        # entries in the feed, too. Thus also for our “fe”.
        fg.load_extension('podcast')
        fg.podcast.itunes_author('John Doe')
        fg.podcast.itunes_category('Technology', 'Podcasting')
        fg.podcast.itunes_explicit('no')
        fg.podcast.itunes_complete('no')
        fg.podcast.itunes_new_feed_url('https://example.com/new-feed.rss')
        fg.podcast.itunes_owner('John Doe', 'jdoe@example.com')
        fg.podcast.itunes_summary('Lorem ipsum dolor sit amet, consectetur ' +
                                  'adipiscing elit. Verba tu fingas et ea ' +
                                  'dicas, quae non sentias?')
        fg.podcast.itunes_type('episodic')
        fe.podcast.itunes_author('John Doe')
        fe.podcast.itunes_season(1)
        fe.podcast.itunes_episode(1)
        fe.podcast.itunes_title('First podcast episode')
        fe.podcast.itunes_episode_type('full')
        print_enc(fg.rss_str(pretty=True))

    elif arg == 'torrent':
        fg.load_extension('torrent')
        fe.link(href='https://example.com/torrent/debian-8-netint.iso.torrent',
                rel='alternate',
                type='application/x-bittorrent, length=1000')
        fe.torrent.filename('debian-8.4.0-i386-netint.iso.torrent')
        fe.torrent.infohash('7661229811ef32014879ceedcdf4a48f256c88ba')
        fe.torrent.contentlength('331350016')
        fe.torrent.seeds('789')
        fe.torrent.peers('456')
        fe.torrent.verified('123')
        print_enc(fg.rss_str(pretty=True))

    elif arg.startswith('dc.'):
        fg.load_extension('dc')
        fg.dc.dc_contributor('John Doe')
        if arg.endswith('.atom'):
            print_enc(fg.atom_str(pretty=True))
        else:
            print_enc(fg.rss_str(pretty=True))

    elif arg.startswith('syndication'):
        fg.load_extension('syndication')
        fg.syndication.update_period('daily')
        fg.syndication.update_frequency(2)
        fg.syndication.update_base('2000-01-01T12:00+00:00')
        if arg.endswith('.rss'):
            print_enc(fg.rss_str(pretty=True))
        else:
            print_enc(fg.atom_str(pretty=True))

    elif arg.endswith('atom'):
        fg.atom_file(arg)

    elif arg.endswith('rss'):
        fg.rss_file(arg)


if __name__ == '__main__':
    main()
