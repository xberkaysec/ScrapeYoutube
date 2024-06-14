import json
from time import sleep
from rich import print
from playwright.sync_api import sync_playwright
from colorama import Fore, Style


print("""

        ⠀⠀⠀⢲⣦⠀⢠⣶⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠘⣿⡄⣼⡟⢀⣤⣤⣄⠀⢠⣄⠀⣠⡄⠀⠀⠀⠀
        ⠀⠀⠀⠀⢹⣷⣿⠁⣿⡏⠙⣿⡆⢸⣿⠀⣿⡇⠀⠀⠀⠀
        ⠀⠀⠀⠀⠈⣿⡏⠀⣿⡇⠀⣿⡇⢸⣿⠀⣿⡇⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⣿⡇⠀⢿⣧⣰⣿⠇⢸⣿⣤⣿⡇⠀⠀⠀⠀
        ⠀⠀⣀⣀⣀⣉⣁⣀⣀⣉⣉⣁⣀⣀⣉⣁⣈⣁⣀⣀⠀⠀
        ⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶
        ⣿⣿⣿⣉⠉⠉⣉⣿⣿⣿⣿⠉⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⡇⢸⡟⠛⣿⠛⢻⠀⠘⠛⠻⡿⠛⡛⠻⣿⣿⣿
        ⣿⣿⣿⣿⡇⢸⡇⠀⣿⠀⢸⠀⢸⡇⠀⡇⠀⠿⠀⣿⣿⣿
        ⣿⣿⣿⣿⡇⢸⡇⠀⣿⠀⢸⠀⢸⡇⠀⡇⠀⣶⠒⣿⣿⣿
        ⣿⣿⣿⣿⣧⣼⣷⣤⣴⣦⣾⣤⣶⣤⣼⣿⣦⣤⣴⣿⣿⣿
        ⠙⠻⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟⠋

""")


url = input(Fore.RED + "Enter the URL of the Youtube account to scrape : " + Style.RESET_ALL)


# Do Not Track = Active
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
}

videosData = []


def launch_browser():
    with sync_playwright() as play:
        browser = play.chromium.launch(headless=False) # Browser Chrome
        page = browser.new_page() # New page
        page.set_viewport_size({"width": 1920, "height": 1080}) # 1920x1080
        page.set_extra_http_headers(headers) # Add HTTP headers
        page.context.set_default_timeout(600000) # timeout 600,000 milliseconds (10 minutes)
        page.goto(url) # Go To Url
        page.wait_for_load_state('networkidle') # It waits when all resources of the page are fully loaded.
        sleep(10)

        title = page.title() # title of the page is taken.

        # Indicates rejection of YouTube's cookie policy notice.
        if title == "Before you continue to YouTube":
            button = page.locator('button[aria-label="Reject all"]').first
            button.click()

        page.wait_for_load_state('networkidle')
        page.focus("body") # focus on the content of the page
        moreToLoad = True 

        # video > selects the video using the CSS selector.
        # videoBefore > represents items that come before the video. 
        video = page.locator('#content.style-scope.ytd-rich-item-renderer').first 
        videoBefore = page.locator('#content.style-scope.ytd-rich-item-renderer') 
        
        while moreToLoad:
            # Represents the number of video elements present on the page prior to uploads.
            # End > scroll to the end of the page.
            videoBefore = page.locator('#content.style-scope.ytd-rich-item-renderer').count()
            page.keyboard.press('End')
            page.keyboard.press('End')
            page.keyboard.press('End')
            sleep(2)

            videoAfter = page.locator('#content.style-scope.ytd-rich-item-renderer').count()
            
            print("Video Before : ", videoBefore)
            print("Video After  : ", videoAfter)

            if videoBefore == videoAfter:
                moreToLoad = False
                print('We have reached the end! \n')

        # represents all video elements found on the page
        videos = page.locator('#content.style-scope.ytd-rich-item-renderer')
        
        # take the number of video elements and create a loop
        for idx in range(videos.count()):

            # represents the video element being handled during the current loop.
            video = videos.nth(idx)

            # represents an image element related to the thumbnail of the video and retrieves the URL of the image
            thumbnail_img = video.locator('#thumbnail img').first
            thumbnail = thumbnail_img.get_attribute('src')
            print(f"thumbnail {thumbnail}")

            details = video.locator('#details #meta') # represents HTML elements containing details of the video.
            title = video.locator('h3 #video-title').text_content() # to obtain the video title
            print(f"title {title}")


            views = video.locator('#metadata #metadata-line span').first.text_content() # get the number of views
            views = views.replace('views', '').strip().lower() 

            # k = number of thousands | m = number of millions
            if 'k' in views:
                views = float(views.replace('k', '').strip()) * 1000
            elif 'm' in views:
                views = float(views.replace('m', '').strip()) * 1000000
            else:
                views = float(views.strip())

            print(f"views {views}")


            # take loading time
            upload = video.locator('#metadata #metadata-line span').last.text_content()
            print(f"upload {upload}")

            # obtaining video duration 
            durationSelector = '#thumbnail #overlays ytd-thumbnail-overlay-time-status-renderer #time-status span#text'
            duration = video.locator(durationSelector).first.text_content()
            duration = duration.replace('\n', '').strip()
            print(f"duration {duration}")

            video_obj = {
                'thumbnail': thumbnail,
                'title': title,
                'views': views,
                'upload': upload,
                'duration': duration
            }

            print(video_obj)
            videosData.append(video_obj)

        sleep(10)
        print(videosData)
        browser.close()

launch_browser()