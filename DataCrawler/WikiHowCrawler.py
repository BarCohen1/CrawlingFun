from time import sleep

import requests
import pickle

import ProdcutParser


RAND_HOW_TO = "https://www.wikihow.com/Special:Randomizer"
MAX_PAGE_NUM = 10000

def start_crawling_over_wikihow(need_to, id_counter, urls):
    counter = 0
    while counter <= MAX_PAGE_NUM:
        try:
            if counter % 200 == 0:
                print("saving new results to pickle")
                dump_to_pickle(need_to)
            print("iterating over page num " + str(counter) + " cur len of need_to " + str(len(need_to)))
            rand_result = requests.get(RAND_HOW_TO)
            if rand_result.status_code == 200:
                ret = requests.get(rand_result.url)
                if not_yet_parsed(need_to, ret.url, urls):
                    need_to = retrive_needto(ret.text, need_to, ret.url, id_counter)
                    id_counter = len(need_to)
                    counter += 1
                    sleep(1)
                urls.append(ret.url)
        except Exception as e:
            print("wiki crawler got exception:" + str(e) + "continuing...")
    return need_to

def not_yet_parsed(need_to, url, urls):
    if url in urls:
        print("url already visited")
        return False
    else:
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
    f.close()
def write_urls_to_pickel(urls):
    with open("urls.pkl", 'wb') as f:
        pickle.dump(urls, f)
    f.close()

def read__urls_from_pickel():
    try:
        pickle_off = open("urls.pkl", "rb")
        loaded_data = pickle.load(pickle_off)
        if loaded_data:
            print("loaded urls " + str(len(loaded_data)))
            return loaded_data
    except:
        print("no urls were loaded")
        return list()

def read_from_pickle():
    try:
        pickle_off = open("needTo.pkl", "rb")
        loaded_data = pickle.load(pickle_off)
        if loaded_data:
            print("loaded pickle of length " + str(len(loaded_data)))
            return loaded_data
    except:
        print("empty [] was loaded")
        return list()

def only_prodcuts_print(need_to):
    total_prods = 0
    for url in need_to:
        print(url["Products"])
        total_prods += len(url["Products"])
    print("total products got: " + str(total_prods))


if __name__ == '__main__':
    ret = input("what do you want to do? press 1 for more crawling, press 2 for category print")
    if int(ret) == 1:
        need_to = read_from_pickle()
        urls = read__urls_from_pickel()
        need_to = start_crawling_over_wikihow(need_to, len(need_to), urls)
        print(need_to)
        dump_to_pickle(need_to)
        write_urls_to_pickel(urls)
        only_prodcuts_print(need_to)
    if int(ret) == 2:
        need_to = read_from_pickle()
        only_prodcuts_print(need_to)
