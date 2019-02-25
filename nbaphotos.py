import urllib2, os, time
from bs4 import BeautifulSoup

base_url = 'http://www.nba.com'

print 'Start crawling...'

page = urllib2.urlopen(base_url + '/teams')
soup = BeautifulSoup(page, 'html.parser')

print 'Got teams page!'

teams = soup.findAll('div', attrs={'class': 'team__list'})

print 'Find all teams...' + '\n'

for team in teams:
    team_url = team.find('a', href=True)
    all_team_url = base_url + team_url['href']

    print 'Start with url: ' + all_team_url

    team_page = urllib2.urlopen(all_team_url)
    team_soup = BeautifulSoup(team_page, 'html.parser')

    print 'Team page is ready!'

    city_name = team_soup.find('p', attrs={'class': 'nba-team-header__city-name'}).text.strip()
    team_name = team_soup.find('p', attrs={'class': 'nba-team-header__team-name'}).text.strip()
    nba_team_name = city_name + '_' + team_name

    print 'Start with team: ' + nba_team_name

    if not os.path.exists(nba_team_name):
        os.makedirs(nba_team_name)

    os.chdir(nba_team_name)

    print 'Team directory has been created: ' + nba_team_name

    players = team_soup.find('section', attrs={'class': 'row nba-player-index__row'})

    for player in players:
        player_name = player.find('a')['title'].lower().replace(' ', '_')
        player_link = 'https:' + str(player.find('img')['data-src'])

        print player_name
        print player_link
        print 'Start downloading...'

        resource = urllib2.urlopen(str(player_link))
        output = open(player_name + '.png', 'wb')
        output.write(resource.read())
        output.close()
        print 'Saved image!'
        time.sleep(1)

    print 'Done with team: ' + nba_team_name + '\n'

    os.chdir('..')
    time.sleep(5)
