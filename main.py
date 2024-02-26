from bs4 import BeautifulSoup
from pyppeteer import launch
import asyncio
import requests

import concurrent.futures
import threading

class WEB_STATE():

    def __init__(self, url: str):
        self.url = url
        self.images = []

    async def return_images(self, page):
        html_content = await page.content()
        
        soup = BeautifulSoup(html_content, 'html.parser')

        img_elements = soup.find_all(lambda tag: tag.name in ['img'] and (tag.has_attr('data-src') or tag.has_attr('src')))

        for element in img_elements:
            if element not in self.images:
                if element.get('data-src'):
                    self.images.append(element.get('data-src'))
                elif element.get('src'):
                    self.images.append(element.get('src'))

    async def get_images(self):
        browser = await launch(headless=False)
        page = await browser.newPage()

        await page.goto(self.url)
        
        await self.return_images(page)

        for _ in range(5):
            
            await self.return_images(page)

        #await browser.close()

        return self.images

def download_img(url, path):
    response = requests.get(url)

    if response.status_code == 200:
    
        with open(path, 'wb') as file:
            file.write(response.content)
    
        print(f"Image downloaded successfully at: {path}")
    
    else:
        print(f"Failed to download image. Status code: {response.status_code}")


async def main():
    prompt = "model face man"
    prompt.replace(' ', '+')

    google_images_link = f"https://www.google.com/search?tbm=isch&q={prompt}"
    init_state = WEB_STATE(url= google_images_link)
    images = await init_state.get_images()

    print(images)

    """ for i, img in enumerate(images):
        try:
            path = r"D:\Documentos\Proyectos\Simplify_RPA\imgs\img_" + str(i) + ".jpg"
            download_img(img, path)
        except Exception as e:
            next """

asyncio.run(main())