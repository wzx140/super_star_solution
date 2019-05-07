from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import json


class SuperStar(object):
    LOGIN_URL = 'https://passport2.chaoxing.com/login'
    INDEX_URL = 'http://i.mooc.chaoxing.com/space/index'

    def __init__(self) -> None:
        options = Options()
        self.__cookies = None
        options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--mute-audio')  # 关闭声音
        options.add_argument('--log-level=3')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument(
            'user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"')
        self.__driver = webdriver.Chrome(options=options)

    def login(self):
        options = Options()
        options.add_argument(
            'user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"')
        driver = webdriver.Chrome(options=options)
        driver.get(self.LOGIN_URL)
        try:
            print('请在100s内完成登录')
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.ID, "zne_kc_icon"))
            )
            print('登录成功')
            self.__cookies = driver.get_cookies()
        finally:
            driver.quit()

    def get_lessons(self) -> list:
        self.__driver.get(self.INDEX_URL)
        for cookie in self.__cookies:
            self.__driver.add_cookie({k: cookie[k] for k in cookie.keys()})
        self.__driver.get(self.INDEX_URL)
        element = WebDriverWait(self.__driver, 5).until(
            EC.presence_of_element_located((By.ID, "zne_kc_icon"))
        )
        element.click()
        frame = WebDriverWait(self.__driver, 5).until(
            EC.presence_of_element_located((By.ID, "frame_content"))
        )
        self.__driver.switch_to.frame(frame)
        videos = self.__driver.find_elements_by_css_selector('.zmodel li[style]')
        video_list = []
        for video in videos:
            detail = video.find_element_by_css_selector('h3.clearfix a')
            video_list.append((detail.get_attribute('href'), detail.get_attribute('title')))
        return video_list

    def auto_video(self, target: tuple):
        link, lesson_name = target
        tasks = []
        self.__driver.get(link)
        WebDriverWait(self.__driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".timeline .units"))
        )
        units = self.__driver.find_elements_by_css_selector(".timeline .units")
        for unit in units:
            sections = unit.find_elements_by_css_selector('.leveltwo')
            for section in sections:
                chapter_id = section.find_element_by_css_selector('.chapterNumber').text
                link = section.find_element_by_css_selector('a').get_attribute('href')
                sign = section.find_element_by_css_selector('.clearfix em').get_attribute('class')
                tasks.append((chapter_id, link, sign))
        for task in tasks:
            chapter_id, link, sign = task
            if sign == 'orange':
                self.__driver.get(link)
                f_iframe = WebDriverWait(self.__driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'iframe'))
                )
                self.__driver.switch_to.frame(f_iframe)
                # 获取页面中的视频
                videos = self.__driver.find_elements_by_css_selector('iframe')
                objectids = [video.get_attribute('objectid') for video in videos]
                if len(videos) > 1:
                    # 一个页面多个视频
                    for i, objectid in enumerate(objectids):
                        if not i == 0:
                            # 播放第二个，不刷新会出错
                            self.__driver.refresh()
                            f_iframe = WebDriverWait(self.__driver, 10).until(
                                EC.presence_of_element_located((By.ID, 'iframe'))
                            )
                            self.__driver.switch_to.frame(f_iframe)
                        self.__driver.switch_to.frame(
                            self.__driver.find_element_by_css_selector(
                                'iframe[objectid="{objectid}"]'.format(objectid=objectid)))
                        self.__driver.find_element_by_css_selector('button[title="播放视频"]').click()
                        # 网络不好时，增长暂停时间
                        time.sleep(5)
                        self.__driver.find_element_by_css_selector('button[title="暂停"]').click()
                        # 网络不好时，增长暂停时间
                        time.sleep(5)
                        # 计算等待时间
                        end_time = self.__driver.find_element_by_css_selector('.vjs-duration-display').text
                        start_time = self.__driver.find_element_by_css_selector('.vjs-current-time-display').text
                        count_ = start_time.count(':')
                        if count_ == 1:
                            start_time = datetime.strptime(start_time, '%M:%S')
                        elif count_ == 2:
                            start_time = datetime.strptime(start_time, '%H:%M:%S')
                        count_ = end_time.count(':')
                        if count_ == 1:
                            end_time = datetime.strptime(end_time, '%M:%S')
                        elif count_ == 2:
                            end_time = datetime.strptime(end_time, '%H:%M:%S')

                        delta = (end_time - start_time).seconds + 10
                        self.__driver.find_element_by_css_selector('button[title="播放"]').click()
                        print('正在学习 ' + lesson_name + ' ' + chapter_id + ' 第' + str(i + 1) + '个视频')
                        for j in range(delta):
                            print("\r{time}s 后完成".format(time=delta), end="")
                            time.sleep(1)
                            delta -= 1
                        print('\r', end="")
                        print('完成 ' + lesson_name + ' ' + chapter_id + ' 第' + str(i + 1) + '个视频')
                else:
                    # 一个页面一个视频
                    self.__driver.switch_to.frame(
                        self.__driver.find_element_by_css_selector('iframe[src="{src}"]'.format(src=videos[0])))
                    self.__driver.find_element_by_css_selector('button[title="播放视频"]').click()
                    time.sleep(2)
                    self.__driver.find_element_by_css_selector('button[title="暂停"]').click()
                    # 计算等待时间
                    end_time = self.__driver.find_element_by_css_selector('.vjs-duration-display').text
                    start_time = self.__driver.find_element_by_css_selector('.vjs-current-time-display').text
                    count_ = start_time.count(':')
                    if count_ == 1:
                        start_time = datetime.strptime(start_time, '%M:%S')
                    elif count_ == 2:
                        start_time = datetime.strptime(start_time, '%H:%M:%S')
                    count_ = end_time.count(':')
                    if count_ == 1:
                        end_time = datetime.strptime(end_time, '%M:%S')
                    elif count_ == 2:
                        end_time = datetime.strptime(end_time, '%H:%M:%S')

                    delta = (end_time - start_time).seconds + 10

                    self.__driver.find_element_by_css_selector('button[title="播放"]').click()
                    print('正在学习 ' + lesson_name + ' ' + chapter_id)
                    for i in range(delta):
                        print("\r{time}s 后完成".format(time=delta), end="")
                        time.sleep(1)
                        delta -= 1
                    print()
                    print('完成 ' + lesson_name + ' ' + chapter_id)
        print('完成 ' + lesson_name)

    def save(self, file: str):
        with open(file, 'w') as f:
            json.dump(self.__cookies, f)

    def load(self, file: str):
        with open(file, 'r') as f:
            self.__cookies = json.load(f)
