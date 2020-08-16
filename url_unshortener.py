from bs4 import BeautifulSoup
import re
import requests


class URLParsingError(Exception):
    pass


class UnsupportedURLError(Exception):
    pass


def tinyurl_process(path):
    hosted_url = requests.get(f"http://tinyurl.com/{path}")
    soup = BeautifulSoup(hosted_url.history[0].text,"html.parser")
    return soup.a["href"]



def bitly_process(path):
    hosted_url = requests.get(f"https://bit.ly/{path}")
    soup = BeautifulSoup(hosted_url.history[0].text, "html.parser")
    return soup.a['href']


def rebrandly_process(path):
    hosted_url = requests.get(f"https://rb.gy/{path}")
    response = hosted_url.history[0]
    return response.headers['Location']


supported_sites = {'tinyurl.com': tinyurl_process, 'bit.ly': bitly_process, 'rb.gy': rebrandly_process}

base_name = re.compile("(?:www.|preview.)?([a-zA-z0-9\-]+\.(?:com|ly|gy))(/)?([\w]*)")


def url_resolver(inp):
    match = re.search(base_name, inp)
    if match is None:
        raise URLParsingError(f"{inp} is impossible to parse, please try again")
    web_name = match.group(1)
    web_path = match.group(3)
    x = supported_sites.get(web_name, 0)
    if x:
        if match.group(2) == '':
            print(f"Your service is {web_name}, what is your extension?")
            web_path = input(f"{web_name}/")
            if web_path != "":
                return x(web_path)
            else:
                raise URLParsingError(f"The input is impossible to parse, please try again")
        else:

            return x(web_path)
    else:
        raise UnsupportedURLError(f"We are not compatible with {web_name}")
