import requests
from urllib.request import Request, urlopen 
from bs4 import BeautifulSoup 
  
url = 'https://www.minecraftcrafting.info'
headers = {'User-Agent':'Mozilla/5.0'}
page = requests.get(url) 
soup = BeautifulSoup(page.text, "html.parser") 

images = soup.find_all('img') 
  
for item in images:
    print(item['src']) 
