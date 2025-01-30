from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QSpinBox, QComboBox, QProgressBar, QTableWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("네이버 블로그 크롤러")
        self.setup_ui()
    
    def setup_ui(self):
        # 메인 위젯 설정
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        
        # 검색어 입력
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("검색어 입력")
        
        # 페이지 수 설정 (1-100)
        self.page_count = QSpinBox()
        self.page_count.setRange(1, 100)
        
        # 저장 방식 선택
        self.save_type = QComboBox()
        self.save_type.addItems(["엑셀 파일", "구글 스프레드시트"])
        
        # 진행 상황 표시바
        self.progress_bar = QProgressBar()
        
        # 결과 미리보기 테이블
        self.preview_table = QTableWidget()
        
        # 레이아웃에 위젯 추가
        layout.addWidget(self.search_input)
        layout.addWidget(self.page_count)
        layout.addWidget(self.save_type)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.preview_table)
        
        main_widget.setLayout(layout)