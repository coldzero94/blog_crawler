import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crawler.naver_crawler import NaverBlogCrawler
from storage.excel_manager import ExcelManager

def test_crawler():
    crawler = NaverBlogCrawler()
    excel_manager = ExcelManager()
    
    try:
        # "맛집" 키워드로 검색 테스트
        keyword = "맛집"
        results = crawler.get_blog_posts(keyword=keyword, max_page=1)
        
        print(f"총 {len(results)}개의 포스트를 찾았습니다.")
        
        # 첫 번째 포스트 출력
        if results:
            first_post = results[0]
            print("\n첫 번째 포스트 정보:")
            print(f"제목: {first_post['title']}")
            print(f"요약: {first_post['summary']}")
            print(f"작성자: {first_post['author']}")
            print(f"날짜: {first_post['date']}")
            print(f"URL: {first_post['url']}")
            
            # CSV 파일로만 저장
            csv_path = excel_manager.save_to_csv(results, keyword)
            print(f"\nCSV 파일 저장 완료: {csv_path}")
            
    finally:
        crawler.close()

if __name__ == "__main__":
    test_crawler()