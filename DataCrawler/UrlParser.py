from html.parser import HTMLParser
import math
import requests

class MyHTMLParser(HTMLParser):
    capture_counter = 0
    start_capture = False
    url_list = set()
    def handle_starttag(self, tag, attrs):
        try:
            if tag == "h3" and attrs[0][0] == "class" and attrs[0][1] == "fixed-recipe-card__h3":
                self.start_capture = True
            elif tag == "a" and attrs[0][0] == "href" and self.start_capture:
                self.url_list.add(attrs[0][1])
        except:
            pass

    def handle_endtag(self, tag):
        if self.start_capture and tag == "h3":
            self.start_capture = False

    def handle_data(self, data):
        pass


def parse_and_return_url_recipe_list(text):
    parser = MyHTMLParser()
    parser.feed(text)
    return parser.url_list
