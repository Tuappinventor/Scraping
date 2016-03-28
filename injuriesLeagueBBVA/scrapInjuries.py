from selenium import webdriver

class PlayerInjury:
  name = ''
  injury = ''
  hash = 0

def findInjuriesElement(injury):
    parent = injury.find_element_by_xpath('..')
    parent = parent.find_element_by_xpath('..') #<span style="color: #000000;"><span style="text-decoration: underline;">LESIONADOS</span><br></span>
    parent = parent.find_element_by_xpath('..') #<strong>
    parent = parent.find_element_by_xpath('..') #<td style="text-align: center; background-color: #f5f5f5; width: 100%;"
    return parent.find_element_by_xpath("following-sibling::*");

def writeFileResults(nameFile, listPlayers):
    with open(nameFile, 'w+') as fResults:
        out = "Player,Injury"
        fResults.write(out.encode('utf8') + '\n')
        for pl in listPlayers:
            out = pl.name + "," + pl.injury
            fResults.write(out.encode('utf8') + '\n')

if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.delete_all_cookies()

    url = "http://www.goal.com/es/news/27/liga-de-espa%C3%B1a/2015/12/30/4730098/sancionados-lesionados-y-apercibidos"
    driver.get(url)

    # List all players that we're storing
    listPlayers = []

    injuries = driver.find_elements_by_xpath("//*[contains(text(), 'LESIONADOS')]")
    for injury in injuries:
        # Finding the correct elements to scrap.
        injuElem = findInjuriesElement(injury)
        children = injuElem.find_elements_by_xpath('./*')
        if len(children) < 1:
            continue

        numberOfPlayers = len(children[0].text.split('\n'))
        instancelist = [PlayerInjury() for i in range(numberOfPlayers)]

        counterText = 0
        for child in children[:-1]:
            counterList = 0
            listText = child.text.split('\n')
            for text in listText:
                if counterText == 0:
                    instancelist[counterList].name = text.strip()
                else:
                    instancelist[counterList].injury = text.strip()
                counterList += 1
            counterText += 1

        for player in instancelist:
            player.hash = hash(player.name + player.injury)
            if player.hash not in listPlayers:
                listPlayers.append(player)

    nameFile = "injuriesJornada31.csv"
    writeFileResults(nameFile, listPlayers)

    driver.quit()
