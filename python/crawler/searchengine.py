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

from nltk.stem.porter import PorterStemmer

IGNORE_LIST = ['the','of','to','and','a','in','is','it']


# Yes, I need an ORM. 

class NonStringURLException(Exception):
    pass

class Crawler(object):
    """
    Method signatures for this class are taken from Programming
    Collective Intelligence: Building Smart Web 2.0 Applications
    
    These aren't really the same though.
    """
   
    def __init__(self):
        self.connection = DatabaseInterface().connect()
        self.splitter_regex = re.compile(r'[^\d|\w|\+|\^|\$|\|]+') 
        # Primitive caching. Get a real caching solution.
        # This is already ridiculous.
        self.stemmed_words = {}
        self.indexed_urls = set()

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
        query = self.connection.execute("INSERT INTO link(fromid, toid) VALUES (%d, %d)" %\
                (url_id, next_url_id))
        link_id = query.lastrowid
        for word in word_list:
            if word in IGNORE_LIST:
                continue
            word_id = self.get_entry_id('wordlist','word', word)
            self.connection.execute("INSERT INTO linkwords(linkid, wordid) VALUES (%d, %d)" %\
                    (link_id, word_id))


    def commit(self):
        self.connection.commit()

    def is_indexed(self, url):
        """
            Check to see if this URL has already been cataloged. Adds a form of caching to 
            avoid repeating queries. TODO: Add a real caching system.
        """
        if url in self.indexed_urls:
            print "%s is indexed" % url
            return True
        else:
            rowid = self.connection.execute("SELECT rowid FROM urllist WHERE url = '%s'" % url).fetchone()
        if rowid != None:
            self.indexed_urls.add(url)
            print "%s is indexed" % url
            return True 
        return False

    def get_text_only(self, soup_object):
        """
            Recursively split, then rejoin the contents of our BeautifulSoup object
            into a plain text string.
        """
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
        database. 
        
        The naked queries inside of this method don't really belong here.
        We need an ORM.
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

            We should also stem words so we don't have redundant entries in the database.
        """
        unstemmed_word_list = [word.lower() for word in self.splitter_regex.split(text) if word !='']
        stemmed_word_list = []

        # This is still an inefficient way of storing words that have already been stemmed.
        # I will come up with a better way.

        for word in unstemmed_word_list:
            stemmed_word = self.stemmed_words.get(word, None)
            if stemmed_word is None:
                stemmed_word = PorterStemmer().stem(word)
                self.stemmed_words[word] = stemmed_word
            stemmed_word_list.append(stemmed_word)
        return stemmed_word_list

    def add_to_index(self, url, soup_object):
        """
            This method inserts URLs and associated information into the database.
            
            Naked queries don't belong in this method in this form. I need an ORM
            of some sort.
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
    """
        Method signatures for this class are taken from Programming
        Collective Intelligence: Building Smart Web 2.0 Applications

    """
    def __init__(self):
        """
            Set up connection through a database interface to avoid
            having to change this if we chose to swap the database.
        """
        self.connection = DatabaseInterface().connect()
    
    def get_match_rows(self, query):
        field_string = 'w0.urlid'
        table_string = ''
        clause_string = ''
        word_ids = []
        word_dict = {}
        word_list = [PorterStemmer().stem(word) for word in query.split(' ')]
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
    
    def get_scored_list(self, rows):
        total_scores = {}
        total_scores.update([(row[0],0) for row in rows])
        weights = [(1, self.frequency_score(rows)), (20.0, self.distance_score(rows))]

        for weight, scores in weights:
            for url in total_scores:
                total_scores[url] += weight*scores[url]
        return total_scores
   
    def get_url_name(self, id):
        return self.connection.execute(\
                "SELECT url FROM urllist WHERE rowid=%d" % id).fetchone()[0]
   
    def search_term_query(self, query_string, returns=20):
        """
            Use this method to seach for your words... or the stems
            of them, anyway. Right now does a search of ALL of your words.

        """
        rows, word_ids = self.get_match_rows(query_string)
        scores = self.get_scored_list(rows)
        ranked_scores = scores.items()
        ranked_scores.sort(key = lambda item:item[1], reverse=True)
        for (url_id, score) in ranked_scores[0:returns]:
            print '%f\t%s' % (score, self.get_url_name(url_id))

    def normalize_scores(self, scores, smaller_is_better=False):
        """
            Use this method to get all of the scores in the range 
            [0,1]. Sometimes a better value should be closer to
            0 or 1, so we add the smaller_is_better kwarg.
        """
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
        """
            This method is used to score urls based on
            how many times the search terms appear.
        """
        frequencies = {}
        frequencies.update([(row[0],0) for row in rows])
        for row in rows:
            frequencies[row[0]] += 1
        return self.normalize_scores(frequencies)
    
    def location_score(self, rows):
        """
            This method is used to score urls based on
            the location in the document the search terms appear.
        """
        locations = {}
        locations.update([(row[0],10000000) for row in rows])
        for row in rows:
            location = sum(row[1:])
            if location < locations[row[0]]:
                locations[row[0]] = location
        return self.normalize_scores(locations, smaller_is_better=True)

    def distance_score(self, rows):
        """
            This method is used to score urls based on the distance
            of the search terms from one another.
        """
        distances = {}
        if len(rows[0]) <= 2:
            distances.update([(row[0], 1.0) for row in rows])
        
        distances.update([(row[0], 1000000) for row in rows])
        for row in rows:
            distance = sum([abs(row[i] - row[i-1]) for i in range(2, len(row))])
            if distance < distances[row[0]]:
                distances[row[0]] = distance

        return self.normalize_scores(distances, smaller_is_better=True)

    # Inbound link scores
    def inbound_link_score(self, rows):
        inbound_count = {}
        unique_urls = set([row[0] for row in rows])
        inbound_count.update([(url, self.connection.execute(\
                'SELECT COUNT(*) FROM link WHERE toid=%d' % url).fetchone()[0]) \
                for url in unique_urls])
        return self.normalize_scores(inbound_count)

# TODO: Make a base class for database interfaces. Make two subclasses;
# one that is SQLAlchemy-based for relational database usage and one for
# MongoDB.

class DatabaseInterface(object):

    def connect(self):
        """
            This method is used to open up our SQLite database for now.
            I hope to transform this into something we can use with
            an arbitrary relational or non-relational database.
        """
        db_config = open('dbconfig.txt')
        dbname = db_config.readline().replace('\n','')
        self.connection = sqlite.connect(dbname)
        return self

    def close(self):
        self.connection.close()

    def create_tables(self):
        """
            This method makes the tables needed for this to run
            properly. We should only need to run this once. It
            will raise if you try to create tables that already exist.
        """
        try:
            self.connection.execute('CREATE TABLE urllist(url)')
            self.connection.execute('CREATE TABLE wordlist(word)')
            self.connection.execute('CREATE TABLE wordlocation(urlid,wordid,location)')
            self.connection.execute('CREATE TABLE link(fromid integer,toid integer)')
            self.connection.execute('CREATE TABLE linkwords(wordid,linkid)')
            self.connection.execute('CREATE INDEX wordidx ON wordlist(word)')
            self.connection.execute('CREATE INDEX urlidx ON urllist(url)')
            self.connection.execute('CREATE INDEX wordurlidx ON wordlocation(wordid)')
            self.connection.execute('CREATE INDEX urltoidx ON link(toid)')
            self.connection.execute('CREATE INDEX urlfromidx ON link(fromid)')
            self.connection.commit()
        except OperationalError, e:
            pass

    def calculate_pagerank(self, iterations=20):
        """
            This method calculates the PageRank of the URLs in the database. This assumes
            you have populated the tables link and urllist.

            It will wipe out any existing pagerank table and take forever, at least
            on SQLite.
            
        """
        self.connection.execute('DROP TABLE IF EXISTS pagerank')
        self.connection.execute('CREATE TABLE pagerank(urlid primary key, score)')
        
        # Every url is initialized with a page rank of 1
        self.connection.execute('INSERT INTO pagerank SELECT rowid, 1.0 FROM urllist')
        self.commit()
        
        final_pageranks = {}
        for i in range(iterations):
            print "Iteration %d" % i
            url_ids = self.connection.execute('SELECT rowid FROM urllist')
            for url_id in url_ids:
                url_id = url_id[0]
                pr = 0.15
                # For every page that links to this one
                url_links = self.connection.execute('SELECT distinct fromid FROM link WHERE toid=%d' % url_id)
                for url_link in url_links:
                    page_rank = self.connection.execute('SELECT score FROM pagerank WHERE urlid=%d' % url_link).fetchone()[0]
                    # Get the total number of links from this url
                    url_link_count = self.connection.execute('SELECT count(*) FROM link WHERE fromid=%d' % url_link).fetchone()[0]
                    pr += 0.85*(page_rank/url_link_count)
                self.connection.execute('UPDATE pagerank SET score=%f WHERE urlid=%d' % (pr, url_id))
                self.commit()

                linked_pages = self
    def execute(self, *args, **kwargs):
        return self.connection.execute(*args,**kwargs)
    
    def commit(self, *args, **kwargs):
        return self.connection.commit(*args, **kwargs)

if __name__ == "__main__":
    import sys
    DatabaseInterface().connect().calculate_pagerank()
    #if len(sys.argv) > 1:
    #    print ' '.join(sys.argv[1:])
    #    Searcher().search_term_query(' '.join(sys.argv[1:]))
    #else:
    #    print "I need some search terms."
    #crawler = Crawler().crawl(['http://deathweasel.net','http://google.com','http://www.yahoo.com','http://www.atxhackerspace.org'], 2)
