from time import sleep

import requests
import pickle

import ProdcutParser


RAND_HOW_TO = "https://www.wikihow.com/Special:Randomizer"
MAX_PAGE_NUM = 2000

def start_crawling_over_wikihow(need_to, id_counter):
    counter = 0
    while counter <= MAX_PAGE_NUM:
        print("iterating over page num " + str(counter) + " cur len of need_to " + str(len(need_to)))
        rand_result = requests.get(RAND_HOW_TO)
        if rand_result.status_code == 200:
            ret = requests.get(rand_result.url)
            if not_yet_parsed(need_to, ret.url):
                need_to = retrive_needto(ret.text, need_to, ret.url, id_counter)
                id_counter = len(need_to)
                counter += 1
                sleep(10)
    return need_to

def not_yet_parsed(need_to, url):
    for cur in need_to:
        if cur["url"] == url:
            print("url already in DB")
            return False
    return True


def retrive_needto(text, need_to, url, counter):
    ret = ProdcutParser.extract_prodcuts(text, url, counter)
    if ret != -1:
        need_to.append(ret)
    return need_to

def dump_to_pickle(need_to):
    print("dumping total " + str(len(need_to)) + " products to pickle")
    with open("needTo.pkl", 'wb') as f:
        pickle.dump(need_to, f)

def read_from_pickle():
    try:
        pickle_off = open("needTo.pkl", "rb")
        loaded_data = pickle.load(pickle_off)
        if loaded_data:
            return loaded_data
    except:
        print("empty [] was loaded")
        return list()

if __name__ == '__main__':
    need_to = read_from_pickle()
    # need_to = list()
    need_to = start_crawling_over_wikihow(need_to, len(need_to))
    print(need_to)
    dump_to_pickle(need_to)
