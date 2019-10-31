from bs4 import BeautifulSoup
import urllib.request


def parser(url, cls, elem):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    teams_content = soup.find_all(elem, class_=cls)

    teams = []
    for li in teams_content:
        elem = li.getText().replace("\n", "").replace("\t", "") \
            .replace("\r", "").replace(u'\xa0', u'') \
            .replace("  ", " ").replace("Home (Goals) ", "").replace("Away (Goals) ", "").replace(
            "Away (Special bets) ", "").replace("Home (Special bets) ", "")
        if elem != '':
            if " - " in elem:
                elem = elem.split(" - ")
                teams.extend(elem)
            elif " v " in elem:
                elem = elem.split(" v ")
                teams.extend(elem)
            else:
                teams.append(elem.strip())

    return teams
