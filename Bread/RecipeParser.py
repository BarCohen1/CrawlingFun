from html.parser import HTMLParser


import copy
import json


class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.isIngredients = False
        self.isFirstRating = True
        self.inMadeIt = False
        self.cur_param = ""
        self.recipe_dict = json.loads(open("recipe_template").read())


    def handle_starttag(self, tag, attrs):
        try:
            if tag == "h1" and attrs[0][0] == "id" and attrs[0][1] == "recipe-main-content":
                self.cur_param = "title"
            elif tag == "div" and attrs[0][0] == "class" and attrs[0][1] == "recipe-summary__stars":
                self.cur_param = "rating"
            elif tag == "span" and attrs[0][0] == "class" and attrs[0][1] == "submitter__name":
                self.cur_param = "creator"
            elif tag == "span" and attrs[0][0] == "class" and attrs[0][1] == "review-count":
                self.cur_param = "#reviews"
            elif tag == "span" and attrs[0][0] == "class" and attrs[0][1] == "picture-count-link":
                self.cur_param = "#photos"
            elif tag == "time" and attrs[0][0] == "itemprop" and attrs[0][1] == "prepTime":
                self.recipe_dict["prep_time"] = attrs[1][1][2:]
            elif tag == "time" and attrs[0][0] == "itemprop" and attrs[0][1] == "cookTime":
                self.recipe_dict["cook_time"] = attrs[1][1][2:]
            elif tag == "time" and attrs[0][0] == "itemprop" and attrs[0][1] == "totalTime":
                self.recipe_dict["ready_in"] = attrs[1][1][2:]
            elif tag == "span" and attrs[0][0] == "class" and attrs[0][1] == "recipe-directions__list--item":
                self.cur_param = "directions"
            elif tag == "div" and attrs[0][0] == "class" and attrs[0][1] == "rating-stars" and attrs[2][0] == "data-ratingstars" and self.isFirstRating:
                self.recipe_dict["rating"] = attrs[2][1][:4]
                self.isFirstRating = False
            elif tag == "span" and attrs[0][0] == "class" and attrs[0][1] == "made-it-count":
                self.inMadeIt = True

            # ingredients
            elif tag == "ul":
                if "id" in [i for (i, j) in attrs if j[:15] == "lst_ingredients"]:
                    self.cur_param = "ingredients"
                    self.isIngredients = True
            elif self.isIngredients and tag == "label":
                if attrs[1][1] != "btn-addtolist":
                    self.recipe_dict[self.cur_param].append(attrs[1][1])

        except:
            pass

    def handle_endtag(self, tag):
        if self.isIngredients and tag == "ul":
            self.cur_param = ""
            self.isIngredients = False

    def handle_data(self, data):
        if self.cur_param == "title":
            self.recipe_dict[self.cur_param] = data
            self.cur_param = ""
        if self.cur_param == "creator":
            self.recipe_dict[self.cur_param] = data
            self.cur_param = ""
        if self.cur_param == "#reviews":
            self.recipe_dict[self.cur_param] = data[:-8]
            self.cur_param = ""
        if self.cur_param == "#photos":
            self.recipe_dict[self.cur_param] = data[:-7]
            self.cur_param = ""
        if self.cur_param == "prep_time":
            self.recipe_dict[self.cur_param] = data
            self.cur_param = ""
        if self.cur_param == "directions":
            self.recipe_dict[self.cur_param].append(data.strip())
            self.cur_param = ""
        if self.inMadeIt and data:
            self.inMadeIt = False
            self.recipe_dict["#made_it"] = data[:-8]


def parse_recipe(text, id, url):
    parser = MyHTMLParser()
    parser.feed(text)
    parser.recipe_dict["id"] = id
    parser.recipe_dict["url"] = url
    return copy.deepcopy(parser.recipe_dict)
