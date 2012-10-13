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


IGNORE_LIST = ['the','of','to','and','a','in','is','it']


# Yes, I need an ORM. 

class NonStringURLException(Exception):
    pass

class Crawler(object):
    
    def __init__(self, dbname):
        self.connection = DatabaseInterface().connect(dbname)
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
            if word in IGNORE_LIST:
                continue
            word_id = self.get_entry_id('wordlist','word', word)
            self.connection.execute("INSERT INTO linkwords(linkid, wordid) VALUES (%d, %d)" %\
                    (link_id, word_id))


    def commit(self):
        self.connection.commit()

    def is_indexed(self, url):
        rowid = self.connection.execute("SELECT rowid FROM urllist WHERE url = '%s'" % url).fetchone()
        if rowid != None:
            # Now testing to see if we've crawled the page. This is a little flawed; the page could
            # consist of pictures only or else maybe consist of links other than FTP sites.
            has_words = self.connection.execute("SELECT * from wordlocation WHERE urlid = %d" % rowid[0]).fetchone()
            if has_words != None:
                print "%s is indexed." % url
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
    
    def get_entry_id(self, table, field, value):
        """
        This gets unique ids associated with entering values into the
        database. I need to fold this into the Database class so I 
        can refactor that without changing the Crawler class.
        """
        
        query = self.connection.execute("SELECT rowid FROM %s WHERE %s = '%s'" % \
                (table, field, value))
        result = query.fetchone()
        if result == None:
            query = self.connection.execute("INSERT INTO %s (%s) VALUES ('%s')" % (table, field, value))
            return query.lastrowid
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

        query_string = "INSERT INTO wordlocation(urlid, wordid, location) \
                VALUES (%d, %d, %d)"
        for i in xrange(len(word_list)):
            word = word_list[i]
            if word in IGNORE_LIST:
                continue
            word_id = self.get_entry_id('wordlist','word',word)
            
            self.connection.execute(query_string % (url_id, word_id, i))

class Searcher(object):
    def __init__(self, dbname):
        self.connection = DatabaseInterface().connect(dbname)
    
    def get_match_rows(self, query):
        field_string = 'w0.urlid'
        table_string = ''
        clause_string = ''
        word_ids = []
        word_dict = {}
        word_list = query.split(' ')
        table_number = 0

        # Find out if the words even exist in our database first.
        for word in word_list:
            result = self.connection.execute(\
                    "SELECT rowid FROM wordlist WHERE word = '%s'" % word).fetchone()
            if result:
               word_dict[word] = result[0]

        # If none of them exist, let's just return empty results instead of trying
        # to construct this query.
        if not word_dict:
           return [],[]

        for word, word_id in word_dict.iteritems():
            if word_id != None:
                word_ids.append(word_id)
                if table_number > 0:
                    table_string += ','
                    clause_string +=' AND '
                    clause_string += 'w%d.urlid=w%d.urlid AND ' % (table_number-1, table_number)
                field_string += ',w%d.location' % table_number
                table_string += 'wordlocation w%d' % table_number
                clause_string += 'w%d.wordid=%d' % (table_number, word_id)
                table_number = table_number + 1
        full_query = ' SELECT %s FROM %s WHERE %s ' % (field_string, table_string, clause_string)
        result = self.connection.execute(full_query)
        rows = [row for row in result]

        return rows, word_ids
    
    def get_scored_list(self, rows, word_ids):
        total_scores = {}
        total_scores.update([(row[0],0) for row in rows])
        weights = []

        for (weight, scores) in weights:
            for url in total_scores:
                total_scores[url] += total_scores[url]
        return total_scores
   
    def get_url_name(self, id):
        return self.connection.execute(\
                "SELECT url FROM urllist WHERE rowid=%d" % id).fetchone()[0]
   
    def query(self, query_string):
        rows, word_ids = self.get_match_rows(query_string)
        scores = self.get_scored_list(rows, word_ids)
        ranked_scores = scores.items()
        ranked_scores.sort(key = lambda item:item[1])
        for (url_id, score) in ranked_scores[0:10]:
            print '%f\t%s' % (score, self.get_url_name(url_id))

    def normalize_scores(self, scores, smaller_is_better=False):
        very_small_value = 0.00001
        return_dict = {}
        if smaller_is_better:
            minimum_score = min(scores.values())
            return_dict.update([(url_id, float(minimum_score)/max(very_small_value, score)) for url_id, score in scores.items()])
        else:
            maximum_score = max(scores.values())
            if not maximum_score:
                maximum_score = very_small_value
            return_dict.update([(url_id, float(score)/maximum_score) for url_id, score in scores.items()])
        return return_dict
    
    def frequency_score(self, rows):
        frequencies = {}
        frequencies.update([(row[0],0) for row in rows])
        for row in rows:
            frequencies[row[0]] += 1
        return self.normalize_scores(frequencies)
    
    def location_score(self, rows):
        locations = {}
        locations.update([(row[0],10000000) for row in rows])
        for row in rows:
            location = sum(row[1:])
            if location < locations[row[0]]:
                locations[row[0]] = location
        return self.normalize_scores(locations, smaller_is_better=True)

    def distance_score(self, rows):
        distances = {}
        if len(rows[0]) <= 2:
            distances.update([(row[0], 1.0) for row in rows])
        
        distances.update([(row[0], 1000000) for row in rows])
        for row in rows:
            distance = sum([abs(row[i] - row[i-1]) for i in range(2, len(row))])
            if distance < distances[row[0]]:
                distances[row[0]] = distance

        return self.normalize_scores(distances, smaller_is_better=True)


# TODO: Make a base class for database interfaces. Make two subclasses;
# one that is SQLAlchemy-based for relational database usage and one for
# MongoDB.

class DatabaseInterface(object):

    def connect(self, dbname):
        self.connection = sqlite.connect(dbname)
        return self

    def close(self):
        self.connection.close()

    def create_tables(self):
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
    Searcher('crawlerdb.db')
    # crawler = Crawler('crawlerdb.db').crawl(['http://deathweasel.net','http://google.com','http://www.yahoo.com','http://www.atxhackerspace.org'], 2)
