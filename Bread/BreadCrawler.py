from time import sleep

import requests
import pickle
import json
import RecipeParser
import UrlParser

START_URL = "https://www.allrecipes.com/recipes/156/bread/"
MAX_PAGE_NUM = 16
MAX_RECIPE_NUM = 300


def get_all_bread_recipes():
    cur_page = "?page="
    counter = 1
    cur_url = lambda x: START_URL + cur_page + str(x)
    while requests.get(cur_url(counter)).status_code == 200 and counter <= MAX_PAGE_NUM:
        print("iterating over page num " + str(counter))
        ret = requests.get(cur_url(counter))
        text = ret.text
        retrieve_recipe_url_from_text(text)
        counter += 1
        sleep(2)


def retrieve_recipe_url_from_text(text):
    global bread_urls
    bread_urls = bread_urls.union(UrlParser.parse_and_return_url_recipe_list(text))


def dump_to_pickle():
    print("dumping total " + str(len(bread_urls)) + " urls to pickle")
    with open("BreadUrls.pkl", 'wb') as f:
        pickle.dump(bread_urls, f)


def read_from_pickle():
    pickle_off = open("BreadUrls.pkl", "rb")
    global bread_urls
    bread_urls = pickle.load(pickle_off)


def build_recipe_json(url, counter):
    ret = requests.get(url)
    if ret.status_code == 200:
        text = ret.text
        return RecipeParser.parse_recipe(text, counter, url)


def build_full_json():
    for counter, url in enumerate(bread_urls):
        if counter > MAX_RECIPE_NUM:
            break
        full_json["recipes"].append(build_recipe_json(url, counter))
        print(str(counter) + "/" + str(MAX_RECIPE_NUM))
        sleep(1)


def save_full_json():
    with open("bread.json", 'w') as bread_f:
        json.dump(full_json, bread_f, indent=4)


def load_full_json():
    return json.loads(open("bread.json").read())


if __name__ == '__main__':
    bread_urls = set()
    get_all_bread_recipes()
    full_json = {"recipes": []}
    build_full_json()
    save_full_json()