# OpenAI Text Analyzer

OpenAI API를 활용한 텍스트 분석 도구입니다. URL 또는 직접 입력한 텍스트를 분석하여 핵심 포인트와 주요 키워드를 추출합니다.

## 기능

- URL 또는 텍스트 입력을 통한 컨텐츠 분석
- OpenAI GPT-4O-mini 모델을 사용한 텍스트 분석
- 핵심 포인트 5개 추출
- 주요 키워드 분석
- 사용자 친화적인 웹 인터페이스

## 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/[your-username]/openai-text-analyzer.git
cd openai-text-analyzer
```

2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

3. Jupyter Notebook 실행
```bash
jupyter notebook
```

4. `analyzer.ipynb` 파일을 열고 실행

## 사용 방법

1. OpenAI API 키 준비
   - [OpenAI 웹사이트](https://openai.com)에서 API 키를 발급받습니다.

2. 분석 방식 선택
   - URL: 웹페이지 내용을 분석
   - Text: 직접 입력한 텍스트를 분석

3. 내용 입력
   - URL 또는 분석할 텍스트를 입력 필드에 입력

4. '분석 시작' 버튼 클릭
   - 분석 결과가 자동으로 표시됩니다.

## 라이센스

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
