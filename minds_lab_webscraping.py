from bs4 import BeautifulSoup
import requests
import re
from tqdm import tqdm
import json
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--numarticles', type=int, default=10)
    args = parser.parse_args()
    NO_OF_ARTICLES = args.numarticles
    Base_URL = "https://www.aljazeera.com"
    Article_list = []

    # Preparing a list of url for recent 10 articles
    html_text = requests.get(
        "https://www.aljazeera.com/where/mozambique/").text
    soup = BeautifulSoup(html_text, 'lxml')
    article_links = soup.find_all("article", {"class": re.compile(
        '^gc u-clickable-card gc--type-post.*')})[:NO_OF_ARTICLES]
    article_url = [Base_URL + link.find("a").get("href")
                   for link in article_links]

    # Collecting data from each article
    for url in tqdm(article_url):
        data = {}
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')
        data["Link"] = url
        data["Heading"] = soup.find("h1").text
        data["Sub_Heading"] = soup.find("em").text
        data["Date"] = soup.find("span", {"aria-hidden": "true"}).text
        data["Text"] = soup.find(
            "div", {"class": "wysiwyg wysiwyg--all-content css-1ck9wyi"}).text
        Article_list.append(data)

    # Saving data in a json file
    with open(f"Recent_{NO_OF_ARTICLES}_Articles.json", "w") as outfile:
        json.dump(Article_list, outfile, indent=2)


if __name__ == "__main__":
    main()
