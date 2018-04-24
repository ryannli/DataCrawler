from urllib.request import urlopen
import bs4
import re
import json
import logging
import traceback
from utils import select_bottom_k, parse_string_to_list, parse_box_office, select_top_k


def get_movie_from_actor(url):
    """
    Gets the actor information and movie information from actor url
    :param url: the actor url
    :return: actor name, actor information, movie information
    """
    respond = urlopen(url)

    webpage = bs4.BeautifulSoup(respond.read(), "html.parser")
    movie_info = []
    actor_info = {}

    movie_list = []
    actor_name = webpage.find("h1", attrs={"id": "firstHeading", "class": "firstHeading"}).get_text()
    actor_year_string = webpage.find("span", attrs={"class": "noprint ForceAgeToShow"}).get_text()
    actor_year = re.search("age\D*(\d+)\D*", actor_year_string).group(1)
    try:
        # Example: https://en.wikipedia.org/wiki/Ashley_Judd
        filmography = webpage.find("span", attrs={"id": "Film"})
        if filmography is not None:
            filmography = filmography.find_parent()
        else:
            # Example: https://en.wikipedia.org/wiki/Shirley_MacLaine
            filmography = webpage.find("span", attrs={"id": "Filmography"}).find_parent()
        table_entry = filmography.find_next_sibling()

        if len(table_entry.find_all('tr')) == 0:
            warning = 'Filmography table is not found'
            logging.warning(warning)
            raise ValueError(warning)
        for row in table_entry.find_all('tr'):
            try:
                columns = row.find_all('td')
                movie_entry_info = {}
                movie_entry_info['title'] = columns[1].get_text()
                movie_entry_info['year'] = int(columns[0].get_text())
                movie_entry_info['url'] = "https://en.wikipedia.org" + (row.find('a')).get('href')
                movie_info.append(movie_entry_info)
                movie_list.append(movie_entry_info['title'])
            except:
                pass
    except:
        try:
            # Example: https://en.wikipedia.org/wiki/Morgan_Freeman
            filmography = webpage.find("div", attrs={"class": "div-col columns column-width"})
            if filmography is None:
                # Example: https://en.wikipedia.org/wiki/Matt_Damon
                filmography = webpage.find("div", attrs={"class": "div-col columns column-count column-count-2"})
            for row in filmography.find_all('li'):
                movie_entry_info = {}

                entry = row.find('a')
                title = entry.get_text()
                year = re.search("\((.+)\)", row.get_text()).group(1)

                movie_entry_info['title'] = title
                movie_entry_info['url'] = "https://en.wikipedia.org" + entry.get('href')
                movie_entry_info['year'] = int(year)
                movie_info.append(movie_entry_info)
                movie_list.append(title)
        except:
            pass

    if not movie_list:
        warning = 'Failed to get movie data'
        raise ValueError(warning)
    actor_info['url'] = url
    actor_info['movies'] = select_bottom_k(movie_list, SELECT_MOVIE_PER_ACTOR)
    actor_info['age'] = int(actor_year)
    return actor_name, actor_info, select_bottom_k(movie_info, SELECT_MOVIE_PER_ACTOR)


def get_actor_from_movie(url):
    """
    Gets the movie information and actor information from movie url
    :param url: the movie url
    :return: movie name, movie information, actor information
    """
    respond = urlopen(url)
    webpage = bs4.BeautifulSoup(respond.read(), "html.parser")
    movie_info = {}
    actor_info = []

    actor_list = []
    movie_name = webpage.find("h1", attrs={"id": "firstHeading", "class": "firstHeading"}).get_text()
    infobox = webpage.find('table', attrs={'class': 'infobox vevent'})
    for row in infobox.find_all('tr'):
        if row.find('th') is not None:
            if row.find('th').get_text() == 'Starring':
                for entry in row.find_all('a'):
                    actor_entry_info = {}
                    actor_entry_info['url'] = "https://en.wikipedia.org" + entry.get('href')
                    actor_entry_info['name'] = entry.get_text()
                    actor_info.append(actor_entry_info)
                    actor_list.append(actor_entry_info['name'])

            elif row.find('th').get_text() == 'Country':
                movie_info['country'] = parse_string_to_list(row.find('td').get_text())
            elif row.find('th').get_text() == 'Box office':
                movie_info['gross'] = parse_box_office(row.find('td').get_text())
            elif row.find('th').get_text() == 'Language':
                movie_info['lang'] = parse_string_to_list(row.find('td').get_text())

    # only use movie with gross
    if 'gross' not in movie_info:
        warning = 'Box office of this movie is not found'
        logging.warning(warning)
        raise ValueError(warning)

    movie_info['actors'] = select_top_k(actor_list, SELECT_ACTOR_PER_MOVIE)
    movie_info['url'] = url
    return movie_name, movie_info, select_top_k(actor_info, SELECT_ACTOR_PER_MOVIE)


ACTOR_FILE_PATH = '../data/actors_small.json'
MOVIE_FILE_PATH = '../data/movies_small.json'
START_URL = 'https://en.wikipedia.org/wiki/Morgan_Freeman'
FORCE_CRAWL_A = False
FORCE_CRAWL_M = False

TARGET_MOVIE_NUMBER = 20
TARGET_ACTOR_NUMBER = 30

SELECT_MOVIE_PER_ACTOR = 5
SELECT_ACTOR_PER_MOVIE = 5

if __name__ == "__main__":
    actor_num = 0
    movie_num = 0
    actor_data = {}
    movie_data = {}
    failure_names = set()

    actor_stack = []
    movie_stack = []

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename='data_crawler.log',
                        filemode='w',
                        level=logging.INFO)

    logging.info("start crawling website %s" % START_URL)
    try:
        actor_name, actor_info, movie_info = get_movie_from_actor(START_URL)
        actor_data[actor_name] = actor_info
        actor_num += 1
        movie_stack += select_bottom_k(movie_info, SELECT_MOVIE_PER_ACTOR)
    except AttributeError:
        logging.error("Failed to get actor data from start url " + traceback.print_exc())

    # Loop for data crawling
    while movie_num < TARGET_MOVIE_NUMBER or actor_num < TARGET_ACTOR_NUMBER:
        # process a movie
        if len(movie_stack) == 0 and len(actor_stack) == 0:
            logging.error("No left urls to crawl..\n Program will exit..")
            break

        if movie_num < TARGET_MOVIE_NUMBER or FORCE_CRAWL_M:
            while 1:
                if len(movie_stack) == 0:
                    logging.warning("Movie stack is empty, need to crawl data from actors to enlarge movie stack..")
                    FORCE_CRAWL_A = True
                    break
                movie = movie_stack.pop()
                if movie['title'] not in movie_data:
                    break

            if not FORCE_CRAWL_A:
                logging.info("Crawling movie %s from %s" % (movie['title'].encode("UTF-8"), movie['url']))
                url = movie['url']
                try:
                    movie_name, movie_info, actor_info = get_actor_from_movie(url)
                    movie_info.update(movie)
                    movie_info.pop('title')
                    movie_data[movie['title']] = movie_info
                    movie_num += 1
                    actor_stack += actor_info
                    if len(actor_stack) > 0:
                        FORCE_CRAWL_M = False
                except:
                    logging.warning("Failed to get all required information from this url.. will try next one")
                    pass

        # process an actor
        if actor_num < TARGET_ACTOR_NUMBER or FORCE_CRAWL_A:
            while 1:
                if len(actor_stack) == 0:
                    logging.warning("Actor stack is empty, need to crawl data from movies to enlarge actor stack..")
                    FORCE_CRAWL_M = True
                    break
                actor = actor_stack.pop()
                if actor['name'] not in actor_data:
                    break

            if not FORCE_CRAWL_M:
                logging.info("Crawling actor %s from %s" % (actor['name'].encode("UTF-8"), actor['url']))
                url = actor['url']
                try:
                    actor_name, actor_info, movie_info = get_movie_from_actor(url)
                    actor_data[actor['name']] = actor_info
                    actor_num += 1
                    movie_stack += movie_info
                    if len(movie_stack) > 0:
                        FORCE_CRAWL_A = False
                except:
                    logging.warning("Failed to get all required information from this url.. will try next one")
                    pass

    logging.info("Writing to json files..")
    actor_file = open(ACTOR_FILE_PATH, 'w')
    movie_file = open(MOVIE_FILE_PATH, 'w')
    jsonData = json.dumps(actor_data, indent=4)
    actor_file.write(jsonData)
    jsonData = json.dumps(movie_data, indent=4)
    movie_file.write(jsonData)
    logging.info("Successfully stored data to json files")
    actor_file.close()
    movie_file.close()
