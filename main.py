import requests
from bs4 import BeautifulSoup

# URL to scrape
url = 'https://www.w3schools.com/python/python_file_write.asp'

# Headers to include in the request
headers = {
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

# Make the GET request
# response = requests.get(url, headers=headers)




with open("index.html",'r') as f:
    html_content = f.read()


# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Print the prettified HTML
print(soup.get_text())


# with open('index.html' ,'w') as f:
#     f.write(soup.prettify())