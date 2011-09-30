'''
This module holds the URLGatherer class and associated exceptions.
URLGatherer is a primitive webcrawler.

@author: rossjr
'''

import urllib2
import re

class NonURLException(Exception):
    pass

class InvalidDepthException(Exception):
    pass

class NonStringURLException(Exception):
    pass


class URLGatherer(object):
        
    header_data = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'
}
#header_data is here simply because most webservers do not like bots. We are masquerading as a real 
#browser.
    
    '''
    This class is basically a web crawler. For a given URL and configurable depth,
    get content from the url, filter out all the URLs, rinse, repeat until desired depth.
    Return list.
    
    Assumptions:
    We want HTTP URLs. No FTP, no local files, nothing requiring authentication.

    
    TODO: Needs processes/threads
    '''

    
    url_regex = re.compile(r'\bhttp://[\w/./@/:/+/$/!/*]{0,63}\.\w{2,3}/?[\w@/-/./&/?=%#_!]*\b')
    image_regex = re.compile(r'.*\.(gif|jpg|png|js)') #we don't want to waste time grabbing images
    #This doesn't guarantee that we won't grab images, but it will help.
    
    def get_url_list(self, initial_url, depth):
        """
            This is the gatekeeper to the URLGatherer class. Use this to
            get a big list of URLs.
            
            @param initial_url: a string representing the URL we should start crawling at.
            @param depth: a positive integer depth to which we should follow the links
        """
        if not isinstance(depth, int) or depth < 0:
            raise InvalidDepthException('Expected non-negative integer for recursion depth, got %r' % depth) 
        if not isinstance(initial_url, str):
            raise NonStringURLException('Expected string for initial URL, got %r' % initial_url)
        if not self._isUrl(initial_url):
            raise NonURLException('Expected non-image URL for initial URL, got  %s' % initial_url)
        
        return self._find_urls(initial_url, [], depth)
        
    def _find_urls(self, url, last_urls, depth):
        
        even_more_urls = [url]
        if depth > 0:        
            request = urllib2.Request(url, headers=self.header_data)
            try:
                response = urllib2.urlopen(request, None, timeout=10)
            except:
                return [] 
            #I don't like generic try, except either, but here are apparently some 
            #other errors that urlopen can throw other than URLError, HTTPError. 
            #Better safe than sorry. 
            #TODO: Figure these out.
            url_content = response.read()   
        
        
            url_list = self.url_regex.findall(url_content) #extract urls from content string
            url_list = list(set(url_list)) #Remove duplicates
            url_list =  [n for n in [u for u in url_list if u not in last_urls] \
                         if not self.image_regex.match(n)]
            last_urls.append(url)
            
            for new_url in url_list:
                even_more_urls.extend(self._find_urls(new_url, last_urls, depth-1))
        
        return even_more_urls
    
    def _isUrl(self, initial_url):
        if self.url_regex.match(initial_url) and not self.image_regex.match(initial_url):
            return True
        else:
            return False
    