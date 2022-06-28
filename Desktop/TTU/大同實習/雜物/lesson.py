from selenium.webdriver.chrome.options import Options #初始化瀏覽器
from splinter.browser import Browser                  #加載splinter與頁面交互
from browsermobproxy import Server                    #瀏覽器驅動
from time import sleep                                #時間模塊

server=Server('C:/Users/TatungSS/Downloads/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat')
server.start()
proxy=server.create_proxy()
chrome_options=Options()
chrome_options.add_argument('--proxy-server={host}:{port}'.format(host='localhost',port=proxy.port))

class HuoChe(object):
    driver_name='Chrome'
    executable_path='D:/pyt/chromedriver_win32/chromedriver.exe'
    username = u"410606224"
    passwd = u"loverock12"
    list1 = ['I3450\n','I4260\n','I5550\n','I5900\n','I3160']
    list2 = ['I3640\n','G1613C\n','G2280\n','G3020B\n','I2000B']
    select_url = "https://stucis.ttu.edu.tw/selcourse/FastSelect.php"
    login_url = "https://stucis.ttu.edu.tw/login.php"

    def __init__(self):
        print("Welcome To Use The Tool")

    def login(self):
        proxy.new_har()
        self.driver.visit(self.login_url)
        self.driver.fill('ID',self.username)
        self.driver.fill('PWD',self.passwd)
        self.driver.find_by_name('Submit').first.click()

    def start(self):
        self.driver = Browser(driver_name='chrome')
        self.driver.driver.set_window_size(1400,1000)
        self.login()
        sleep(1)
        self.driver.visit(self.select_url)
        self.driver.fill('EnterSbj',self.list1)
        self.driver.find_by_name('Submit').first.click()
        sleep(1)
        self.driver.visit(self.select_url)
        self.driver.fill('EnterSbj',self.list2)
        self.driver.find_by_name('Submit').first.click()
        
if __name__=="__main__":
    train = HuoChe()
    train.start()