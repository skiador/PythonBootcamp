import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇

connection = requests.get(url=URL)
html = connection.text

website_soup = BeautifulSoup(html, 'html.parser')


# Get all list elements
film_gallery = website_soup.find(class_="gallery")
film_containers = film_gallery.find_all(name="section")

film_titles = []
for film_container in film_containers[::-1]:
    title = film_container.find_next(class_="title").getText()
    film_titles.append(title)

print(film_titles)


