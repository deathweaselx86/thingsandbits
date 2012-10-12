#!/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

# Let's work through chapter 4 of the O'Reilly Collective Intelligence book.
# That has scientist code, though. I'll try to write mine a bit better.

import urllib2
import re
import BeautifulSoup
import urlparse
from sqlite3 import dbapi2 as sqlite # replace with MongoDB or CouchDB
from sqlite3 import OperationalError
ignore_list = ['the','of','to','and','a','in','is','it']
class NonStringURLException(Exception):
    pass

class Crawler(object):
    # Do we need this?
    # header_data = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'}
    
    def __init__(self, dbname):
        self.connection = Database().connect(dbname)
        self.splitter_regex = re.compile(r'\W*') 

    def crawl(self, urls, depth):
        """
            This is the method that actually does the crawling. This is actually smarter than
            a recursive solution; no risk of stack exhaustion.
        """
        for i in range(depth):
            new_urls = set()
            for url in urls:
                try:
                    page_contents = urllib2.urlopen(url)
                except: # Find list of exceptions?
                    print "Couldn't open %s" % url
                    continue
                soup_contents = BeautifulSoup.BeautifulSoup(markup=page_contents.read())
                self.add_to_index(url, soup_contents)
                links = soup_contents('a') # anchor elements
                for link in links:
                    if 'href' in dict(link.attrs):
                        next_url = urlparse.urljoin(url,link['href'])
                        if next_url.find("'") != -1:
                            continue
                        next_url = next_url.split('#')[0] #no location
                        if next_url[0:4] == 'http' and not self.is_indexed(next_url):
                            new_urls.add(next_url)
                        text = self.get_text_only(link)
                        self.add_link_reference(url, next_url, text)
                self.commit()
            urls = new_urls

    def add_link_reference(self, url, next_url, text):
        """
            This method populates the table that links 
            urls to other urls.
        """
        word_list = self.separate_words(text)
        url_id = self.get_entry_id('urllist', 'url', url)
        next_url_id = self.get_entry_id('urllist', 'url', next_url)
        if url_id == next_url_id:
            return
        cursor = self.connection.execute("INSERT INTO link(fromid, toid) VALUES (%d, %d)" %\
                (url_id, next_url_id))
        link_id = cursor.lastrowid
        for word in word_list:
            if word in ignore_list:
                continue
            word_id = self.get_entry_id('wordlist','word', word)
            self.connection.execute("INSERT INTO linkwords(linkid, wordid) VALUES (%d, %d)" %\
                    (link_id, word_id))


    def commit(self):
        self.connection.commit()

    def is_indexed(self, url):
        rowid = self.connection.execute("SELECT rowid FROM urllist where url='%s'" % url).fetchone()
        if rowid != None:
            # Now testing to see if we've crawled the page. This is a little flawed; the page could
            # consist of pictures only or else maybe consist of links other than FTP sites.
            has_words = self.connection.execute("SELECT * from wordlocation where urlid=%d" % rowid[0]).fetchone()
            if has_words != None:
                return True
        return False

    def get_text_only(self, soup_object):
        if soup_object.string == None:
            contents = soup_object.contents
            result_text = ''
            for text in contents:
                subtext = self.get_text_only(text)
                result_text = '\n'.join((result_text, subtext))
            return result_text
        else:
            return soup_object.string.strip()
    
    def get_entry_id(self, table, field, value, createnew=True):
        """
        This gets unique ids associated with entering values into the
        database. I need to fold this into the Database class so I 
        can refactor that without changing the Crawler class.
        """
        
        cursor = self.connection.execute("SELECT rowid FROM %s WHERE %s = '%s'" % \
                (table, field, value))
        result = cursor.fetchone()
        if result == None:
            cursor = self.connection.execute("INSERT INTO %s (%s) VALUES ('%s')" % (table, field, value))
            return cursor.lastrowid
        else:
            return result[0]


    def separate_words(self, text):
        """
            Superficially, it should be enough to split on whitespace, but that's not quite it.
            Just split on non-word.
        """
        return [word.lower() for word in self.splitter_regex.split(text) if word !='']

    def add_to_index(self, url, soup_object):
        """
            This method inserts URLs and associated information into the database.
            Needs to be refactored such that I can swap the database in and out without
            changing the Crawler code.
        """
        if self.is_indexed(url):
            return
        print "Indexing %s " % url

        text = self.get_text_only(soup_object)
        word_list = self.separate_words(text)
        url_id = self.get_entry_id('urllist','url',url)

        query = "INSERT INTO wordlocation(urlid, wordid, location) \
                VALUES (%d, %d, %d)"
        for i in xrange(len(word_list)):
            word = word_list[i]
            if word in ignore_list:
                continue
            word_id = self.get_entry_id('wordlist','word',word)
            
            self.connection.execute(query % (url_id, word_id, i))

class Database(object):

    def connect(self, dbname):
        self.connection = sqlite.connect(dbname)
        return self

    def close(self):
        self.connection.close()

    def create_tables(self):
        # Ughhhhhh, don't make this a specific method in the Database class.
        try:
            self.connection.execute('create table urllist(url)')
            self.connection.execute('create table wordlist(word)')
            self.connection.execute('create table wordlocation(urlid,wordid,location)')
            self.connection.execute('create table link(fromid integer,toid integer)')
            self.connection.execute('create table linkwords(wordid,linkid)')
            self.connection.execute('create index wordidx on wordlist(word)')
            self.connection.execute('create index urlidx on urllist(url)')
            self.connection.execute('create index wordurlidx on wordlocation(wordid)')
            self.connection.execute('create index urltoidx on link(toid)')
            self.connection.execute('create index urlfromidx on link(fromid)')
            self.connection.commit()
        except OperationalError, e:
            pass
    def execute(self, *args, **kwargs):
        return self.connection.execute(*args,**kwargs)
    def commit(self, *args, **kwargs):
        return self.connection.commit(*args, **kwargs)
if __name__ == "__main__":
    crawler = Crawler('crawlerdb.db').crawl(['http://deathweasel.net','http://google.com'], 2)
