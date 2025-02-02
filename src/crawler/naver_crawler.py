from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class NaverBlogCrawler:
    def __init__(self):
        # Chrome 옵션 설정
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')  # 헤드리스 모드
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        
        # WebDriver 초기화
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.chrome_options
        )
        
    def get_blog_posts(self, keyword, max_page=1):
        all_results = []
        
        for page in range(1, max_page + 1):
            url = f"https://section.blog.naver.com/Search/Post.naver?pageNo={page}&rangeType=ALL&orderBy=sim&keyword={keyword}"
            
            try:
                self.driver.get(url)
                print(f"{page}페이지 크롤링 중...")
                
                # 페이지가 완전히 로드될 때까지 대기
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "area_list_search"))
                )
                
                # 스크롤을 아래로 조금씩 내려 동적 컨텐츠 로드
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                while True:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)  # 로딩 대기
                    new_height = self.driver.execute_script("return document.body.scrollHeight") 
                    if new_height == last_height:
                        break
                    last_height = new_height
                
                # 블로그 포스트 목록 가져오기
                posts = self.driver.find_elements(By.CLASS_NAME, "list_search_post")
                
                results = []
                for post in posts:
                    try:
                        title = post.find_element(By.CLASS_NAME, "desc_inner").text
                        summary = post.find_element(By.CLASS_NAME, "text").text
                        author = post.find_element(By.CLASS_NAME, "author").text
                        date = post.find_element(By.CLASS_NAME, "date").text
                        url = post.find_element(By.CLASS_NAME, "desc_inner").get_attribute("href")
                        
                        results.append({
                            "title": title,
                            "summary": summary,
                            "author": author,
                            "date": date,
                            "url": url
                        })
                    except Exception as e:
                        print(f"포스트 파싱 중 오류 발생: {str(e)}")
                        continue
                
                all_results.extend(results)
                
            except Exception as e:
                print(f"페이지 {page} 크롤링 중 오류 발생: {str(e)}")
                continue
                
        return all_results
        
    def close(self):
        self.driver.quit()
