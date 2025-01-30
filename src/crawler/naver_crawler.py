import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse
from typing import List, Dict

class NaverBlogCrawler:
    BASE_URL = "https://section.blog.naver.com/Search/Post.naver"
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        }
    
    def get_search_url(self, keyword: str, page_no: int) -> str:
        """검색 URL 생성"""
        encoded_keyword = urllib.parse.quote(keyword)
        return f"{self.BASE_URL}?pageNo={page_no}&rangeType=ALL&orderBy=sim&keyword={encoded_keyword}"
    
    def crawl_page(self, keyword: str, page_no: int) -> List[Dict]:
        """한 페이지의 블로그 포스트 크롤링"""
        url = self.get_search_url(keyword, page_no)
        response = self.session.get(url, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f"페이지 접근 실패: {response.status_code}")
            
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.select('.list_search_post > li')
        
        results = []
        for post in posts:
            try:
                # 블로그 제목
                title = post.select_one('.title_post').text.strip()
                
                # 포스트 내용 요약
                summary = post.select_one('.text').text.strip()
                
                # 작성자
                author = post.select_one('.writer').text.strip()
                
                # 작성일
                date_str = post.select_one('.date').text.strip()
                
                # URL
                url = post.select_one('.title_post > a')['href']
                
                # 현재 수집 시간
                collected_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                results.append({
                    'title': title,
                    'summary': summary,
                    'author': author,
                    'date': date_str,
                    'url': url,
                    'collected_at': collected_at
                })
                
            except Exception as e:
                print(f"포스트 파싱 중 오류 발생: {str(e)}")
                continue
                
        return results
    
    def crawl_multiple_pages(self, keyword: str, start_page: int, end_page: int, 
                           progress_callback=None) -> List[Dict]:
        """여러 페이지의 블로그 포스트 크롤링"""
        all_results = []
        total_pages = end_page - start_page + 1
        
        for i, page_no in enumerate(range(start_page, end_page + 1), 1):
            try:
                results = self.crawl_page(keyword, page_no)
                all_results.extend(results)
                
                # 진행률 업데이트 (GUI 연동용)
                if progress_callback:
                    progress = (i / total_pages) * 100
                    progress_callback(progress)
                    
            except Exception as e:
                print(f"페이지 {page_no} 크롤링 중 오류 발생: {str(e)}")
                continue
                
        return all_results

# 테스트 코드
if __name__ == "__main__":
    crawler = NaverBlogCrawler()
    results = crawler.crawl_multiple_pages("맛집", 1, 2)
    
    # 결과 출력
    for result in results:
        print("\n=== 포스트 정보 ===")
        print(f"제목: {result['title']}")
        print(f"작성자: {result['author']}")
        print(f"작성일: {result['date']}")
        print(f"URL: {result['url']}")
        print(f"요약: {result['summary'][:100]}...")