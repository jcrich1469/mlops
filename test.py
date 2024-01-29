import sys
print(sys.executable)
print(sys.path)

import requests

from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://news.ycombinator.com/ask"

# Send a GET request to the page
response = requests.get(url)
# print('response = ', response)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    # print('html text = ', soup)
    # print(type(soup))

else:
    print("Failed to retrieve the webpage")

soup_table = soup.html.body.center.find('table',id='hnmain')

rows = [row for row in soup_table.find_all('tr')]

def get_questions(rows):
    title_rows = [row.find_all('span',class_='titleline') for row in rows]
    # print(title_rows)

    title_rows = list(filter(lambda element: element != [],title_rows))[0]
    questions = [row.a.text for row in title_rows]
    # questions
    return questions

def get_time(rows):

    subtext_rows = [row.find_all('td',class_='subtext') for row in rows]
    # subtext_rows = list(filter(lambda element: element != [],subtext_rows))[0]
    subtext_rows = list(filter(lambda element: element != [],subtext_rows))

    time_data = [row[0].find_all('a')[1].text for row in subtext_rows][1:]
    return time_data

page = {'questions':get_questions(rows),'time':get_time(rows)}

def filter_time(page,time):

    questions = []
    new_times = []
    for i in range(len(page['time'])):

        if int(page['time'][i].split()[0]) < time:

            questions.append(page['questions'][i])
            new_times.append(page['time'][i])

    page['questions'] = questions
    page['time'] = new_times
    return page


page = filter_time(page,24)


def get_follow_links(rows):
    link_id_rows = [row.find_all('span',class_='titleline') for row in rows]
    # print(title_rows)
    # print(link_id_rows)
    link_id_rows = list(filter(lambda element: element != [],link_id_rows))[0]
    #print(link_id_rows)
    link_ids = [row.a.get('href') for row in link_id_rows ]
    # questions
    return link_ids

LINKROOT=url[:-3]

links = get_follow_links(rows)

print(links)

pagelinks = [LINKROOT + idl for idl in links]


#def get_comments(html_page):
#    get_row()


pages = []


for link in pagelinks[:1]:
    print('fetching page from ', link)
    # Send a GET request to the page
    response = requests.get(link)
    # print('response = ', response)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        # print('html text = ', soup)
        # print(type(soup))

    else:
        print("Failed to retrieve the webpage")

    soup_table = soup.html.body.center.find('table',id='hnmain')
    tree = soup_table.find('table',class_='comment-tree')
    #print(tree.find_all('tr',class_='athing comtr'))
    # comments = [row.find_all('tr',class_='athing comtr') for row in tree]
    # print(comments)
    # rows = [row for row in soup_table.find('table',class_='comment-tree'))]

    # print(rows)
    # page = {'questions':get_questions(rows),'time':get_time(rows)}

    # page = filter_time(page,24)

    pages.append(page)

print(pages)
