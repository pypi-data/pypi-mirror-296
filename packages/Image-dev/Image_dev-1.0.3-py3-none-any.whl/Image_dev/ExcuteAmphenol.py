
from .Resize_HashCode_Exclude import resizeImage, generate_image_hash, getExcludedHashCodes
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from io import BytesIO

class ExcuteAmphenol():
    def __init__(self, urls_and_names , output_path, down_path, exclude_path):
        self.urls_and_names= set(urls_and_names)
        self.output_path= output_path
        self.down_path= down_path
        self.exclude_path= exclude_path
        self.thread_result= {}
        self.broken_urls= []
        #run exclude
        if exclude_path:
            self.ExcludeImages()
        
    def saveOrignalDownload(self, response, image_name):
        with open(rf"{self.down_path}\{image_name}.jpg", 'wb') as file:
            file.write(response.getvalue())

    def saveResize(self, response, image_name):
        resizeImage(response, (150,150)).save(rf"{self.output_path}\Large\{image_name}.jpg", 'png')
        resizeImage(response, (70,70)).save(rf"{self.output_path}\Small\{image_name}.jpg", 'png')
        resizeImage(response, ).save(rf"{self.output_path}\Orignal\{image_name}.jpg", 'png')

    def ExcludeImages(self):
        self.exclude_hashes= getExcludedHashCodes(self.exclude_path)
        print('Excluded Images Included.')

    def getSeleniumResponse(self, url):
        try:
            self.driver.get(url)
            time.sleep(4)
            image_element = self.driver.find_element(By.TAG_NAME, "img")
            response= BytesIO(image_element.screenshot_as_png)
            return True, response
        except Exception as e:
            return False, 'BROKEN 403'
        
    def threadFunc(self, url, image_name):
        status, response= self.getSeleniumResponse(url)
        if status:
            hash_code= generate_image_hash(response)
            if self.exclude_path and hash_code and hash_code in self.exclude_hashes:
                self.thread_result[image_name]= ('EXCLUDE', hash_code)
            else:
                self.saveOrignalDownload(response, image_name)
                try:
                    self.saveResize(response, image_name)
                    self.thread_result[image_name]= ('DONE', hash_code)
                except :
                    self.broken_urls.append((url, image_name))
                    self.thread_result[image_name]= ('CANNOT IDENTIFY IMAGE', None)     
        else:
            self.broken_urls.append((url, image_name))
            self.thread_result[image_name]= (response, None)
        
    def getResults(self):
        # chrome_options = Options()
        # chrome_options.add_argument('-headless')
        self.driver = webdriver.Chrome()
        for url, name in self.urls_and_names:
            self.threadFunc(url, name)
            time.sleep(15)

        time.sleep(60)

        for url, name in self.broken_urls:
            self.threadFunc(url, name)
            time.sleep(15)
        self.driver.quit()
        return self.thread_result
        
    
    


            



    