
from urllib.request import urlopen 
from bs4 import BeautifulSoup 
  
htmldata = urlopen('https://www.geeksforgeeks.org/') 
soup = BeautifulSoup(htmldata, 'html.parser') 
images = soup.find_all('img') 
  
for item in images: 
    print(item['src']) 
