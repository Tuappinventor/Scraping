from selenium import webdriver

class PlayerInjury:
  name = ''
  injury = ''
  hash = 0


def findInjuriesElement(injury):
    parent = injury.find_element_by_xpath('..')
    parent = parent.find_element_by_xpath('..') #<span style="color: #000000;"><span style="text-decoration: underline;">LESIONADOS</span><br></span>
    parent = parent.find_element_by_xpath('..') #<strong>
    parent = parent.find_element_by_xpath('..') #<td style="text-align: center; background-color: #f5f5f5; width: 100%;" colspan="3"><strong><span style="color: #000000;"><span style="text-decoration: underline;">LESIONADOS</span><br></span></strong></td>
    return parent.find_element_by_xpath("following-sibling::*");

if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.delete_all_cookies()

    listURLs = [
        #"http://www.goal.com/es/news/27/liga-de-espa%C3%B1a/2015/12/30/4730098/sancionados-lesionados-y-apercibidos",#31
        "https://www.google.com/url?q=http://www.goal.com/es/news/27/liga-de-espa%25C3%25B1a/2016/03/24/4730098/sancionados-lesionados-y-apercibidos-en-la-liga-bbva-jornada&sa=U&ved=0ahUKEwj-7IuI_OHLAhWFnA8KHWLFAqsQFggFMAA&client=internal-uds-cse&usg=AFQjCNE_Y51Ehc8eiUVUyliW4EUVRsU6Ag",#31
        "https://www.google.com/url?q=http://www.goal.com/es/news/27/liga-de-espa%25C3%25B1a/2016/03/19/4730098/sancionados-lesionados-y-apercibidos-en-la-liga-bbva-jornada&sa=U&ved=0ahUKEwj-7IuI_OHLAhWFnA8KHWLFAqsQFggIMAE&client=internal-uds-cse&usg=AFQjCNG4oH1soF_mRpWJI8fpNkBJojZd1A",#30
        "https://www.google.com/url?q=http://www.goal.com/es/news/27/liga-de-espa%25C3%25B1a/2016/03/17/4730098/sancionados-lesionados-y-apercibidos-en-la-liga-bbva-jornada&sa=U&ved=0ahUKEwj-7IuI_OHLAhWFnA8KHWLFAqsQFggLMAI&client=internal-uds-cse&usg=AFQjCNGVGIdZ-MXSCyJBzyFgsx4Jwv2t6g",#29
        "https://www.google.com/url?q=http://www.goal.com/es/news/27/liga-de-espa%25C3%25B1a/2015/12/30/4730098/sancionados-lesionados-y-apercibidos&sa=U&ved=0ahUKEwj-7IuI_OHLAhWFnA8KHWLFAqsQFggOMAM&client=internal-uds-cse&usg=AFQjCNH2kzIL7_tVwxvzgHcJGW83zxUTxw",#21
        "https://www.google.com/url?q=http://www.goal.com/es/news/27/liga-de-espa%25C3%25B1a/2015/12/09/4730098/sancionados-lesionados-y-apercibidos-en-la-liga-bbva-jornada&sa=U&ved=0ahUKEwj-7IuI_OHLAhWFnA8KHWLFAqsQFggRMAQ&client=internal-uds-cse&usg=AFQjCNEf6nff95lL_CznUHBXQhuP0_FKCg",#28
        "https://www.google.com/url?q=http://www.goal.com/es/news/27/liga-de-espa%25C3%25B1a/2016/01/08/4730098/sancionados-lesionados-y-apercibidos&sa=U&ved=0ahUKEwj-7IuI_OHLAhWFnA8KHWLFAqsQFggUMAU&client=internal-uds-cse&usg=AFQjCNH-NL8AVh7nFfvnWsBcqcCchYDErA",#24
        "https://www.google.com/url?q=http://www.goal.com/es/news/27/liga-de-espa%25C3%25B1a/2016/01/06/4730098/sancionados-lesionados-y-apercibidos-en-la-liga-bbva-jornada&sa=U&ved=0ahUKEwj-7IuI_OHLAhWFnA8KHWLFAqsQFggXMAY&client=internal-uds-cse&usg=AFQjCNHCoJceMKoFTLyBS5LIz7dOlTPgcg",#25
        "https://www.google.com/url?q=http://www.goal.com/es/news/27/liga-de-espa%25C3%25B1a/2015/01/15/4730098/sancionados-lesionados-y-apercibidos-en-la-liga-bbva-jornada&sa=U&ved=0ahUKEwj-7IuI_OHLAhWFnA8KHWLFAqsQFggaMAc&client=internal-uds-cse&usg=AFQjCNHPCfXjyfxB2tb9rKwUMU9Ip9BkZQ",#20
        "https://www.google.com/url?q=http://www.goal.com/es/news/27/liga-de-espa%25C3%25B1a/2015/09/23/4730098/sancionados-lesionados-y-apercibidos-en-la-liga-bbva-jornada&sa=U&ved=0ahUKEwj-7IuI_OHLAhWFnA8KHWLFAqsQFgggMAk&client=internal-uds-cse&usg=AFQjCNEzeZ0qJm3da1lZWofGevB7hO3YhQ",#15
    ]

    listPlayers = []

    #url = "http://www.goal.com/es/news/27/liga-de-espa%C3%B1a/2015/12/30/4730098/sancionados-lesionados-y-apercibidos"
    for url in listURLs:
        driver.get(url)


        injuries = driver.find_elements_by_xpath("//*[contains(text(), 'LESIONADOS')]")
        for injury in injuries:
            injuElem = findInjuriesElement(injury)

            children = injuElem.find_elements_by_xpath('./*')
            if len(children) < 1:
                continue

            numberOfPlayers = len(children[0].text.split('\n'))
            instancelist = [PlayerInjury() for i in range(numberOfPlayers)]

            counterText = 0
            for child in children[:-1]:
                counterList = 0
                # .encode('utf8')
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

    for pl in listPlayers:
        print pl.name + "," + pl.injury

    driver.quit()
