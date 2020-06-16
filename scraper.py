import re
from urllib.parse import urlparse
from collections import defaultdict
from bs4 import BeautifulSoup
#import requests


def scraper(url, resp):
    links = extract_next_links(url, resp)
    # print(links)
    return [link for link in links if is_valid(link)]


stop = []
with open("stopWords.txt", 'r') as stopW:
    for i in stopW:
        stop.append(i.rstrip().lower())
stopW.close()


def extract_next_links(url, resp):

    # Implementation requred.
    try:
        # First check the url is valid or not.
        # If not, then return empty list.
        if not is_valid(url):
            return []
        # if the status is not from 200 to 202, then return empty list
        if resp.status not in range(200, 203):
            return []

        # create a list to store urls
        url_list = []

        # Find all valid urls in the page.
        storeDocument = resp.raw_response.content
        soup = BeautifulSoup(storeDocument, 'html.parser')

        punctuation = '\"'
        url_text = soup.get_text()
        url_text = re.sub(r'[{}]+'.format(punctuation),
                          ' ', url_text).strip().lower()

        lengthfile = open("length.txt", "a")
        # length = len(url_text.split())
        # if length == 0 or length > 30000: return []
        # else: lengthfile.write(url+" "+str(length)+"\n")
        # lengthfile.close()

        words = defaultdict(int)
        wordfile = open("words.txt", 'a')
        length = 0
        for i in url_text.split():
            if(len(i) > 1) and re.match("^[a-z]+['-]?[a-z]+$", i) and i not in stop:
                words[i] += 1
                length += 1
        if length == 0 or length > 6000000:
            return []
        else:
            lengthfile.write(url + " " + str(length) + "\n")
        wordfile.write("=================================" + '\n')
        wordfile.write(f"{url} {str(length)}\n")
        for k, v in words.items():
            wordfile.write(str(k) + " " + str(v) + "\n")
        wordfile.close()

        # if len(soup.get_text()) < 100:
        # return []

        for link in soup.findAll('a'):
            temp_url = link.get('href')
            if is_valid(temp_url):
                symbol_index = temp_url.find("#")
                if symbol_index != -1:
                    temp_url = temp_url[:symbol_index]
                url_list.append(temp_url)

        # Get all unique urls in the current page
        url_list = list(set(url_list))

        # Optional part. To save all urls in the current page. May include the urls we have saved from other pages.
        # To get unique urls from all, we have another py file to do that.
        file = open("output2.txt", "a")

        for i in url_list:
            file.write(str(i).rstrip("/") + "\n")
        print(len(url_list))
        file.close()
        return url_list
    except:
        pass


def is_valid(url):
    # print(url)
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        check_valid = 0
        # if the sub_domain of url is in the list, then pass
        for i in [".ics.uci.edu", ".cs.uci.edu", ".informatics.uci.edu", ".stat.uci.edu"]:
            if i in parsed.netloc:
                check_valid = 1
            if "today.uci.edu" == parsed.netloc:
                check_valid = 1
        # if the sub_domain of url is not in the list, then return False
        if check_valid == 0:
            return False
        if parsed.netloc == "today.uci.edu":
            # We can only crawler /department/information_computer_sciences in today.uci.edu
            if "/department/information_computer_sciences" not in parsed.path:
                return False
            # Calendar is a trap, we need to skip it
            if "/department/information_computer_sciences/calendar" in parsed.path:
                return False

        # trap
        if parsed.netloc == "wics.ics.uci.edu":
            if "/event" in parsed.path:
                return False
            if "share" in url:
                return False

        if parsed.netloc == "evoke.ics.uci.edu":
            if "replytocom=" in url:
                return False

        # if parsed.netloc == "plrg.eecs.uci.edu" and "/publications" in url:
        #     return False

        if len(url) > 300:
            return False
        # make sure not extracting pages with request errors
        '''
        if requests.get(url, timeout=5).status_code not in range(200, 400):
            return False
        '''
        # add .ppsx and .war
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|ppsx|war"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", url.lower())

    except TimeoutError:
        print("TimeoutError for ", parsed)
        return False

    except TypeError:
        print("TypeError for ", parsed)
        raise
