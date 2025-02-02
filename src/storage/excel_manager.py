import pandas as pd
from datetime import datetime
import os

class ExcelManager:
    def __init__(self, base_dir="results"):
        self.base_dir = base_dir
        # 결과 저장할 디렉토리 생성
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
            
    def save_to_csv(self, data, keyword):
        """
        크롤링 결과를 CSV 파일로 저장
        
        Args:
            data (list): 크롤링한 블로그 포스트 데이터 리스트
            keyword (str): 검색 키워드
        
        Returns:
            str: 저장된 파일 경로
        """
        if not data:
            print("저장할 데이터가 없습니다.")
            return None
            
        # DataFrame 생성
        df = pd.DataFrame(data)
        
        # 파일명 생성 (검색어_날짜시간.csv)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{keyword}_{timestamp}.csv"
        filepath = os.path.join(self.base_dir, filename)
        
        # CSV 파일로 저장
        df.to_csv(filepath, index=False, encoding='utf-8-sig')  # utf-8-sig는 한글 깨짐 방지
        
        print(f"데이터가 {filepath}에 저장되었습니다.")
        return filepath
        
    def save_to_excel(self, data, keyword):
        """
        크롤링 결과를 Excel 파일로 저장
        
        Args:
            data (list): 크롤링한 블로그 포스트 데이터 리스트
            keyword (str): 검색 키워드
            
        Returns:
            str: 저장된 파일 경로
        """
        if not data:
            print("저장할 데이터가 없습니다.")
            return None
            
        # DataFrame 생성
        df = pd.DataFrame(data)
        
        # 파일명 생성 (검색어_날짜시간.xlsx)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{keyword}_{timestamp}.xlsx"
        filepath = os.path.join(self.base_dir, filename)
        
        # Excel 파일로 저장
        df.to_excel(filepath, index=False, engine='openpyxl')
        
        print(f"데이터가 {filepath}에 저장되었습니다.")
        return filepath 