from selenium import webdriver

def writeFileResults(nameFile, raw):
    with open(nameFile, 'w+') as fResults:
        fResults.write(raw.encode('utf8'))

if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.maximize_window()

    url = "http://unicode.org/emoji/charts/full-emoji-list.html"
    driver.get(url)

    codes = driver.find_elements_by_class_name("code")
    if codes:
        numTimes = 200
        raw = "["
        for code in codes:
            # "&#x"
            raw += '"' + code.text.replace("U+","x") + '",'
        raw = raw[:-1]
        raw += "]"

        writeFileResults("emojiList.txt", raw)