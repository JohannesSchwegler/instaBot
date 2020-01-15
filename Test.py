from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()

        self.driver.maximize_window()
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(text(), 'Melde dich an.')]")\
            .click()
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(4)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Jetzt nicht')]")\
            .click()
        sleep(3)


    def like_TenPosts(self, hashtag):
        self.driver.find_element_by_xpath("//input[@placeholder=\"Suchen\"]") \
            .send_keys('#'+hashtag+'')
        sleep(6)
        url="/explore/tags/"+hashtag+"/"
        self.driver.find_element_by_xpath('//a[@href="'+url+'"]') \
            .click()
        sleep(5)
        neuste = self.driver.find_element_by_xpath("//h2[contains(text(), 'Neueste')]")
        actions = ActionChains(self.driver)
        actions.move_to_element(neuste).perform()
        sleep(1)
        elements = self.driver.find_elements_by_css_selector("h2 + div .v1Nh3.kIKUG._bz0w")

        print(len(elements))
        for element in range(len(elements)):
            elements[element].click()
            sleep(2)
            isPresentImage= len(self.driver.find_elements_by_css_selector(".zZYga ._97aPb")) > 0
            #isPresentVideo = len(self.driver.find_elements_by_css_selector(".zZYga .tWeCl"))> 0
            if isPresentImage == True:
              overlay = self.driver.find_element_by_css_selector(".zZYga ._97aPb ")
              actionchains = ActionChains(self.driver)
              actionchains.double_click(overlay).perform()
            else:
                overlay = self.driver.find_element_by_css_selector(".zZYga .tWeCl ")
                actionchains = ActionChains(self.driver)
                actionchains.double_click(overlay).perform()
                break
            sleep(2)
            self.driver.find_element_by_xpath("//button[contains(text(), 'Schließen')]") \
            .click()
            sleep(2)



    def like_All_Feed(self):
        elements = self.driver.find_elements_by_css_selector(".M9sTE, ._8Rm4L")
        for element in range(len(elements)):
            # heart = len(self.driver.find_elements_by_xpath("//span[@aria-label='Gefällt mir']"))>0
            #if heart == True:
              overlay = self.driver.find_element_by_css_selector("._9AhH0")
              actionchains = ActionChains(self.driver)
              actionchains.double_click(overlay).perform()

    def get_unfollowers(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
            .click()
        following = self._get_names()
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        followers = self._get_names()
        not_following_back = [user for user in following if user not in followers]
        print(not_following_back)

    def _get_names(self):
        sleep(2)
        sugs = self.driver.find_element_by_xpath('//h4[contains(text(), Suggestions)]')
        self.driver.execute_script('arguments[0].scrollIntoView()', sugs)
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[3]/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/div[2]/button")\
            .click()
        return names


my_bot = InstaBot('webdeveloper.ux', 'Gibson96')
#my_bot.like_All_Feed()
my_bot.like_TenPosts('html')
#my_bot.get_unfollowers()