from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Match:
  date = ''
  competition = ''
  teams = ''
  local = True
  link = ''

def isLocalTeam(teams):
    defaultTeam = u'Atl\xe9tico'
    teamsArr = teams.split("-")
    return True if (teamsArr[0] == defaultTeam) else False

def getMatches(team_name):
    driver.implicitly_wait(5)
    driver.set_page_load_timeout(11)
    
    #url = "http://www.marca.com/deporte/futbol/equipos/atletico/resultados-temporada.html"
    #url = "http://www.marca.com/deporte/futbol/equipos/real-madrid/resultados-temporada.html
    url = "http://www.marca.com/deporte/futbol/equipos/" + team_name + "/resultados-temporada.html"
    try:
        driver.get(url)
    except:
        print "Time out because of ads... but trying to go ahead!"

    table_id = driver.find_element_by_id('resultadosCompletos');
    rows = table_id.find_elements_by_tag_name("tr") # get all of the rows in the table
    for row in rows:
        # Get the columns (all the column 2)
        if row.get_attribute("class") == "encabezado":
            continue

        cols = row.find_elements_by_tag_name("td")

        match = Match()
        match.date = cols[0].text
        match.competition = cols[1].text
        match.teams = cols[2].text
        match.local = isLocalTeam(match.teams)
        match.link = cols[3].find_element_by_tag_name("a").get_attribute("href")

        listMatches.append(match)

    driver.quit()

def addOverlayImage(file):
    textFile = os.path.basename(file)
    text = textFile[textFile.index('_') + 1:]
    text = text.replace(".png", "")

    img = Image.open(file)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("TektonPro-BoldExt.otf", 18)
    draw.text((70, 0), text, (0,0,0), font=font)

    #size = 128, 128
    #img.thumbnail(size)
    #img.save(textFile + ".thumbnail", "JPEG")

    img.save(file)

def saveScreenshot(element, namePNG, driver):
    location = element.location
    size = element.size
    driver.save_screenshot(namePNG) # saves screenshot of entire page
    driver.quit()

    im = Image.open(namePNG) # uses PIL library to open image in memory

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save(namePNG) # saves new cropped image

    addOverlayImage(namePNG)

def getMatchInfo(match, current_match, team_name):
    #if not driver:
        #driver.quit()
    driver = None
    time.sleep(10)

    driver = webdriver.Firefox()
    driver.set_window_position(0,0)
    #driver.delete_all_cookies()

    #url = "http://www.marca.com/eventos/marcador/futbol/2015_16/champions/semifinal/ida/atm_bay/"
    driver.get(match.link)

    time.sleep(10)

    raw = ""

    try:
        if driver.find_element_by_xpath("//*[contains(text(), 'O. INICIALES')]"):
            oncesIniciales = driver.find_elements_by_xpath("//*[contains(text(), 'O. INICIALES')]");

            if len(oncesIniciales) > 0:
                oncesIniciales[0].click()

                raw += match.teams + ","

                # Local team = lTeamAlign
                teamElement = "lTeamAlign" if (match.local) else "vTeamAlign"
                teamElement = driver.find_elements_by_class_name("green")[0].find_element_by_class_name("iniciales").find_element_by_class_name(teamElement)

                alignmentText = None
                alineacionElem = "alignment" if (match.local) else "vAlignment"
                if teamElement.find_element_by_class_name(alineacionElem):
                    alignment = teamElement.find_element_by_class_name(alineacionElem).text
                    raw += alignment + ","

                lines = teamElement.find_elements_by_class_name("plLine");
                for line in lines:
                    players = line.find_elements_by_class_name("player");
                    for player in players:
                        name = player.find_element_by_class_name("pl-name").text.encode("utf-8");
                        raw += name.encode('utf-8') + "\t"

                raw += "\n"
                #saveScreenshot(teamElement, "Atleti/" + str(current_match) + "_" + match.teams + ".png", driver);
                if not os.path.exists(team_name):
                    os.makedirs(team_name)
                saveScreenshot(teamElement, team_name + "/" + str(current_match) + "_" + match.teams + ".png", driver);

    except:
        print "Element not found. Continue..."
        driver.quit()

    return raw


def writeFileResults(nameFile, raw):
    with open(nameFile, 'w+') as fResults:
        fResults.write(raw.encode('utf8'))


if __name__ == "__main__":

    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.delete_all_cookies()
    
    raw = ""

    listMatches = []
    #team_name = "atletico"
    team_name = "real-madrid"
    getMatches(team_name)
    i = 1
    for match in listMatches:
        current_match = len(listMatches) - i
        raw += getMatchInfo(match, current_match, team_name)
        i += 1

    writeFileResults('atleti.csv', raw)

    driver.quit()

    print "- end -"
