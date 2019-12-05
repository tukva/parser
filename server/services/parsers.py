import re
import urllib.request

from bs4 import BeautifulSoup


def team_parser(url, cls, elem):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    teams_content = soup.find_all(elem, class_=cls)

    teams = []
    for li in teams_content:
        elem = li.getText().strip()
        elem = re.sub('[\t\n\r\xa0]', '',  elem)

        if 'Goals' in elem:
            continue

        elem = re.split(' [v-] ', elem)
        teams.extend(elem)

    return teams
