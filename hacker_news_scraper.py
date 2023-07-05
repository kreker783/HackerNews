import requests
from bs4 import BeautifulSoup
import pprint

# Send a GET request to the Hacker News website to get list of news
res = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(res.text, 'html.parser')


# Select all elements with the class 'titleline' to get info about Title and link
links = soup.select('.titleline')
# Select all elements with the class 'subtext' to get info about Votes
subtext = soup.select('.subtext')


# Function to sort the list of Hacker News stories by votes in descending order
def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k:k['votes'], reverse=True)


# Function to create a custom Hacker News list
def create_custom_hn(links, votes):
    hn = []
    
    # Loop through each item in the links list
    for idx, item in enumerate(links):
        # Get the title of news
        title = item.getText()
        # Get the link to news
        href = item.find('a', href=True)
        # Get the number of votes
        vote = subtext[idx].select('.score')

        # Check if the number of votes more than 0 (not every news have votes) 
        if len(vote):
            # Get the votes by extracting the text and removing " points"
            points = int(vote[0].getText().replace(" points", ''))
            if points > 99:
                # Append the title, link, and votes to the hn list
                hn.append({'title': title, 'link': href['href'], 'votes': points})
                
    return sort_stories_by_votes(hn)


pprint.pprint(create_custom_hn(links, subtext))
