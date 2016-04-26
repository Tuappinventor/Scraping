from selenium import webdriver
import time

if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.maximize_window()
    #driver.delete_all_cookies()

    url = "http://orteil.dashnet.org/cookieclicker/"
    driver.get(url)

    cookie = driver.find_element_by_id("bigCookie")

    if cookie:
        numTimes = 200
        for x in range(0, numTimes):
            cookie.click()
            #time.sleep(0.00005)   # Little sleep
        print "End. Cliked " + str(numTimes) + " times."
