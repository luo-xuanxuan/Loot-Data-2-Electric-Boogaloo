import requests
from bs4 import BeautifulSoup

def getCharacterID(character_name,world):
    url = f"https://na.finalfantasyxiv.com/lodestone/character/?q=%22{character_name}%22&worldname={world}"
    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html, "html.parser")

    img = soup.find("img", {"alt": character_name})
    id = img.parent.parent["href"].split("/")[-2]
    return id

def getFreeCompanyID(character_name,world):
    character_id = getCharacterID(character_name,world)
    url = f"https://na.finalfantasyxiv.com/lodestone/character/{character_id}/"
    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html, "html.parser")
    free_company_id = soup.find("div", {"class": "character__freecompany__name"}).find("h4").find("a")["href"].split("/")[-2]
 # type: ignore # type: ignore # type: ignore # type: ignore # type: ignore # type: ignore
    return free_company_id

def getFreeCompanyName(character_name,world):
    url = f"https://na.finalfantasyxiv.com/lodestone/character/?q=%22{character_name}%22&worldname={world}"
    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html, "html.parser")

    free_company_link = soup.find("a", {"class": "entry__freecompany__link"})

    if free_company_link:
        free_company_name = free_company_link.find("span").text
        return free_company_name
    else:
        return None

def getFreeCompanyNameByID(id):
    name = ""
    url = f"https://na.finalfantasyxiv.com/lodestone/freecompany/{id}/"
    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html, "html.parser")
    
    name = soup.find("p", {"class":"entry__freecompany__name"}).text

    return name

def getIconURL(character_name,world):
    url = f"https://na.finalfantasyxiv.com/lodestone/character/?q=%22{character_name}%22&worldname={world}"
    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html, "html.parser")

    img = soup.find("img", {"alt": character_name})

    if img:
        return img["src"]
    else:
        return None