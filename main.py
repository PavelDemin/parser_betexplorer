from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from time import localtime, strftime
from pprint import pprint
from time import sleep

ofset_min = 60
url = 'https://www.betexplorer.com'

chrome_options = Options()

#chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

CHROMEDRIVER_PATH = 'C:\\chromedriver.exe'
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
driver.get(url)

def main():
    #elem = webdriver.find_element_by_xpath("//header[@class='wrap-section__header']/h2[@class='wrap-section__header__title']")
    elem = driver.find_element_by_xpath("//div[@class='container']/div[@class='header__top__right']/div[@id='js-timezone']/span[@class='timezone__current']")
    #Create the object for Action Chains
    actions = ActionChains(driver)
    actions.move_to_element(elem)
    # perform the operation on the element
    actions.perform()
    driver.find_element_by_xpath("//div[@class='header__top']/div[@class='container']/div[@class='header__top__right']/div[@id='js-timezone']/ul[@class='timezone__list']/li[4]/a").click()
    driver.find_element_by_xpath("//div[@class='container']/nav[@class='header__navigation']/ul[@class='menu']/li[@class='menu__item'][4]/a").click()
    driver.find_element_by_xpath("//div[@class='container']/ul[@id='js-submenu']/li[@class='submenu__item'][3]/a").click()

    table = driver.find_element_by_xpath("//table[@class='table-main js-nrbanner-t']").get_attribute('innerHTML')
    soup = BeautifulSoup(table, 'html.parser')
    #soup.find_all("a", attrs={"class": "table-main__tournament"}).get_text()
    #soup.find_all('tbody',class_='js-nrbanner-tbody h-display-none').decompose()

    for banner in soup.select('tbody.js-nrbanner-tbody'):
        banner.decompose()

    tbody_list = soup.find_all("tbody")
    real_time = strftime("%H:%M", localtime())
    ofset_minutes = int(real_time[:2])*60 + int(real_time[4:6]) + ofset_min
    game_list = []
    for tbody in tbody_list:
        tr = tbody.find_all("tr")
        for row in tr:
            game = []
            time = row.find("span", attrs={"class": "table-main__time"})
            
            if time != None:
                if int(time.get_text()[:2])*60 + int(time.get_text()[4:6]) >= ofset_minutes:
                    country = tbody.find("a", attrs={"class": "table-main__tournament"}).get_text()
                    game.append(country)
                    time = row.find("span", attrs={"class": "table-main__time"}).get_text()
                    game.append(time)
                    comands_list = row.find("td", attrs={"class": "table-main__tt"})
                    link = comands_list.find('a')['href']
                    game.append(link)
                    comands1 = comands_list.find_all("span")[1].get_text()
                    comands2 = comands_list.find_all("span")[2].get_text()
                    game.append(comands1)
                    game.append(comands2)
                    ratio_list = row.find_all("td", attrs={"class": "table-main__odds"})
                    for ratio_item in ratio_list:
                        if ratio_item.find('a') != None:
                            game.append(ratio_item.find('a').get_text())
            game_list.append(game)
    gm = [i for i in game_list if i]
    print(gm)
    for match in gm:
        driver.get(url + match[2])
        sleep(5)


if __name__ == '__main__':
    main()
    driver.close()