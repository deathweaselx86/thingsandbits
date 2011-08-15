'''
Created on Jul 11, 2011

@author: rossjr
'''
import unittest
import urlgather

class TestURLGatherer(unittest.TestCase):
    

    def setUp(self):
        self.url_gatherer = urlgather.URLGatherer()
        self.maxDiff = None
        
    def test_nonstring_input(self):
        """
        Does this throw an exception properly when you
        pass a nonstring object for the URL parameter?
        """
        self.assertRaises(urlgather.NonStringURLException, 
                          self.url_gatherer.get_url_list, [], 1)
    
    def test_nonurl_input(self):
        """
        Does this throw an exception properly when
        you pass a non URL string  for the URL parameter?
        """
        
        self.assertRaises(urlgather.NonURLException, 
                          self.url_gatherer.get_url_list, 'asdf', 0)
        
    def test_noninteger_depth(self):
        """
        Does this throw an exception properly when
        you pass a noninteger depth parameter?
        """
        self.assertRaises(urlgather.InvalidDepthException,
                           self.url_gatherer.get_url_list, "http://www.yahoo.com","-.45")
        
    def test_negative_depth(self):
        """
        Does this throw an exception properly when
        you pass a noninteger depth parameter?
        """
        self.assertRaises(urlgather.InvalidDepthException,
                           self.url_gatherer.get_url_list, "http://www.yahoo.com",-1)
        
    
    def test_returns_list(self):
        """
            Does this return a list with a purely restful URL e.g.
            no query string, pure scheme, authority.
        """
        django_url= 'http://docs.djangoproject.com/en/1.3/ref/contrib/gis/gdal/#django.contrib.gis.gdal.DataSource'
        #In real life, this url has scheme https, but no actual auth for some reason
        return_url_list = self.url_gatherer.get_url_list(django_url, 0)
        self.assertIsInstance(return_url_list, list)

    def test_handle_nonhtml(self):
        """
         Does this handle URLs that do not return HTML?
         
        """
        test_url = 'http://docs.python.org/_static/py.png'
        self.assertRaises(urlgather.NonURLException, 
                          self.url_gatherer.get_url_list, test_url, 0)

    def test_handle_at_url(self):
        """
         Does this handle URLs with @ signs?
         
        """
        test_url = 'http://www.flickr.com/photos/7216709@N08/2993628587/'
        return_url_list = self.url_gatherer.get_url_list(test_url, 0)
        self.assertNotEquals(return_url_list, [])
        
         
    def test_timeout(self):
        """
            Does this handle URLs that timeout?
            As of 07/12/2011, this times out.
        """   
        test_url= 'http://lysator.liu.se'
        return_url_list = self.url_gatherer.get_url_list(test_url, 1)
        self.assertEquals(return_url_list, [])
         
    def test_post_url(self):
        """
            Does this work with a POST request?
        """
        test_url= 'http://www.google.com/search?q=pylons'
        return_url_list = self.url_gatherer.get_url_list(test_url, 0)
        self.assertNotEquals(return_url_list, [])

    def test_HTTPError(self):
        """
        Can this handle general HTTPError without dying?
        """
        test_url = 'http://jxint.apps.journyx.com/asdf'
        return_url_list = self.url_gatherer.get_url_list(test_url, 0)
    
    def test_works(self):
        """
            Does this return the links on a page that
            I wrote specifically for this purpose?
            
        """
        expected_results = ['http://www.epilogue.net',
        'http://sandbox.sevarg.net/links.html',
        'http://www.artvark.us',
        'http://www.kyoht.com',
        'http://elfwood.lysator.liu.se',
        'http://www.goldenwolfen.com',
         'http://hyenapaws.critter.net']
        test_url = "http://sandbox.sevarg.net/links.html"
        return_url_list = self.url_gatherer.get_url_list(test_url,1)
        self.assertEquals(set(return_url_list), set(expected_results))

    def test_recursion(self):
        """
            Does this work with a little page with 1 levels of recursion?
            I would test more, but it takes long enough with just 1.
            I did get an IOError at least once here. 
            Please find a copy of this page in the same directory that
            the rest of the code is in.
        """
        test_url = "http://sandbox.sevarg.net/art.html"
        return_url_list = self.url_gatherer.get_url_list(test_url,1)
        self.assertEquals(return_url_list, ['http://sandbox.sevarg.net/art.html',
                                            'http://arstechnica.com'])
        
        
if __name__ == "__main__":
    unittest.main()