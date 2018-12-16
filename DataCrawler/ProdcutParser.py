from html.parser import HTMLParser


import copy
import json


class MyHTMLParser(HTMLParser):
        
    def __init__(self):
        HTMLParser.__init__(self)
        self.start_capture = False
        self.prodcut_dict = json.loads(open("howto_template").read())
        self.cur_param = ""
        self.main_catergoy = True


    def handle_starttag(self, tag, attrs):
        try:
            if tag == "a" and attrs[0][0] == "href":
                if attrs[0][1][0:9] == "/Category":
                    if self.main_catergoy:
                        self.cur_param = "Category"
                        self.main_catergoy = False
                    else: self.cur_param = "SubCategory"
            if tag == "div" and attrs[0][0] == "id" and attrs[0][1] == "thingsyoullneed":
                self.start_capture = True
            if tag == "div" and attrs[0][0] == "class" and attrs[0][1] == "clearall":
                self.start_capture = False
        except:
            pass

    def handle_endtag(self, tag):
        pass
        # if tag == "div" and self.start_capture:
        #     self.start_capture = False
        

    def handle_data(self, data):
        if self.start_capture and data.strip():
            self.prodcut_dict["Products"].append(data)
        if self.cur_param == "Category" and data.strip():
            self.prodcut_dict["Category"] = data
        if self.cur_param == "SubCategory" and data.strip(): 
            self.prodcut_dict["SubCategory"] = data
        self.cur_param = ""

def extract_prodcuts(text, url, id):
    parser = MyHTMLParser()
    parser.prodcut_dict["id"] = id
    parser.prodcut_dict["url"] = url
    parser.feed(text)
    if len(parser.prodcut_dict["Products"]) > 0:
        return copy.deepcopy(parser.prodcut_dict)
    else: return -1
