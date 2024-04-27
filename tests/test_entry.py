# -*- coding: utf-8 -*-

"""
Tests for a basic entry

These are test cases for a basic entry.
"""

import unittest

from feedgen.feed import FeedGenerator


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        fg = FeedGenerator()
        self.feedId = 'https://example.com/feed.xml'
        self.title = 'A Feed'

        fg.id(self.feedId)
        fg.title(self.title)
        fg.link(href='https://example.com', rel='alternate')[0]
        fg.description('...')

        fe = fg.add_entry()
        fe.id('https://example.com/podcast/episode-1.mp3')
        fe.title('The First Episode')
        fe.content(u'…')

        # Use also the different name add_item
        fe = fg.add_item()
        fe.id('https://example.com/podcast/episode-2.mp3')
        fe.title('The Second Episode')
        fe.content(u'…')

        fe = fg.add_entry()
        fe.id('https://example.com/podcast/episode-3.mp3')
        fe.title('The Third Episode')
        fe.content(u'…')

        self.fg = fg

    def test_setEntries(self):
        fg2 = FeedGenerator()
        fg2.entry(self.fg.entry())
        self.assertEqual(len(fg2.entry()), 3)
        self.assertEqual(self.fg.entry(), fg2.entry())

    def test_loadExtension(self):
        fe = self.fg.add_item()
        fe.id('1')
        fe.title(u'…')
        fe.content(u'…')
        fe.load_extension('base')
        self.assertTrue(fe.base)
        self.assertTrue(self.fg.atom_str())

    def test_checkEntryNumbers(self):
        fg = self.fg
        self.assertEqual(len(fg.entry()), 3)

    def test_TestEntryItems(self):
        fe = self.fg.add_item()
        fe.title('A Title')
        self.assertEqual(fe.title(), 'A Title')
        author = fe.author(email='jdoe@example.com')[0]
        self.assertFalse(author.get('name'))
        self.assertEqual(author.get('email'), 'jdoe@example.com')
        author = fe.author(name='John Doe', email='jdoe@example.com',
                           replace=True)[0]
        self.assertEqual(author.get('name'), 'John Doe')
        self.assertEqual(author.get('email'), 'jdoe@example.com')
        contributor = fe.contributor(name='John Doe',
                                     email='jdoe@example.com')[0]
        self.assertEqual(contributor, fe.contributor()[0])
        self.assertEqual(contributor.get('name'), 'John Doe')
        self.assertEqual(contributor.get('email'), 'jdoe@example.com')
        link = fe.link(href='https://example.com/entry', rel='alternate')[0]
        self.assertEqual(link, fe.link()[0])
        self.assertEqual(link.get('href'), 'https://example.com/entry')
        self.assertEqual(link.get('rel'), 'alternate')
        fe.guid('123')
        self.assertEqual(fe.guid().get('guid'), '123')
        fe.updated('2017-02-05 13:26:58+01:00')
        self.assertEqual(fe.updated().year, 2017)
        fe.summary('A summary')
        self.assertEqual(fe.summary(), {'summary': 'A summary'})
        fe.description('A description')
        self.assertEqual(fe.description(), 'A description')
        fe.pubDate('2017-02-05 13:26:58+01:00')
        self.assertEqual(fe.pubDate().year, 2017)
        fe.rights('Some rights')
        self.assertEqual(fe.rights(), 'Some rights')
        source = fe.source(url='https://example.com/entry', title='A Title')
        self.assertEqual(source.get('title'), 'A Title')
        self.assertEqual(source.get('url'), 'https://example.com/entry')
        fe.comments('Some comments')
        self.assertEqual(fe.comments(), 'Some comments')
        fe.enclosure(url='https://example.com/enclosure', type='text/plain',
                     length='1')
        self.assertEqual(fe.enclosure().get('url'),
                         'https://example.com/enclosure')
        fe.ttl(8)
        self.assertEqual(fe.ttl(), 8)

        self.fg.rss_str()
        self.fg.atom_str()

    def test_checkItemNumbers(self):
        fg = self.fg
        self.assertEqual(len(fg.item()), 3)

    def test_checkEntryContent(self):
        fg = self.fg
        self.assertTrue(fg.entry())

    def test_removeEntryByIndex(self):
        fg = FeedGenerator()
        self.feedId = 'https://example.com/feed.xml'
        self.title = 'A Feed'

        fe = fg.add_entry()
        fe.id('https://example.com/podcast/episode-3.mp3')
        fe.title('The Third Episode')
        self.assertEqual(len(fg.entry()), 1)
        fg.remove_entry(0)
        self.assertEqual(len(fg.entry()), 0)

    def test_removeEntryByEntry(self):
        fg = FeedGenerator()
        self.feedId = 'https://example.com/feed.xml'
        self.title = 'A Feed'

        fe = fg.add_entry()
        fe.id('https://example.com/podcast/episode-3.mp3')
        fe.title('The Third Episode')

        self.assertEqual(len(fg.entry()), 1)
        fg.remove_entry(fe)
        self.assertEqual(len(fg.entry()), 0)

    def test_categoryHasDomain(self):
        fg = FeedGenerator()
        fg.title('A Title')
        fg.link(href='https://example.com', rel='alternate')
        fg.description('A description')
        fe = fg.add_entry()
        fe.id('https://example.com/podcast/episode-1.mp3')
        fe.title('An Entry Title')
        fe.category([
             {'term': 'category',
              'scheme': 'https://example.com/category',
              'label': 'Category',
              }])

        result = fg.rss_str()
        self.assertIn(b'domain="https://example.com/category"', result)

    def test_content_cdata_type(self):
        fg = FeedGenerator()
        fg.title('A Title')
        fg.id('https://example.com/feed.xml')
        fe = fg.add_entry()
        fe.id('http://lernfunk.de/media/654322/1')
        fe.title('some title')
        fe.content('content', type='CDATA')
        result = fg.atom_str()
        expected = b'<content type="CDATA"><![CDATA[content]]></content>'
        self.assertIn(expected, result)

    def test_summary_html_type(self):
        fg = FeedGenerator()
        fg.title('A Title')
        fg.id('https://example.com/feed.xml')
        fe = fg.add_entry()
        fe.id('https://example.com/entry')
        fe.title('An Entry Title')
        fe.link(href='https://example.com/entry')
        fe.summary('<p>summary</p>', type='html')
        result = fg.atom_str()
        expected = b'<summary type="html">&lt;p&gt;summary&lt;/p&gt;</summary>'
        self.assertIn(expected, result)
