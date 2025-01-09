import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup

# 페이지 설정
st.set_page_config(
    page_title="OpenAI Text Analyzer",
    page_icon="📊",
    layout="wide"
)

# 로고 이미지 (base64로 인코딩된 간단한 막대 그래프 SVG)
logo_html = """
    <div style="display: flex; align-items: center; gap: 1rem;">
        <svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
            <rect x="5" y="20" width="6" height="15" fill="#00ff00"/>
            <rect x="17" y="10" width="6" height="25" fill="#ff00ff"/>
            <rect x="29" y="15" width="6" height="20" fill="#00ffff"/>
        </svg>
        <h1 style="margin: 0; color: var(--text-color);">OpenAI Text Analyzer</h1>
    </div>
"""

# CSS 스타일 - 다크 모드 대응
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        height: 40px;
    }
    .stTextArea > div > div > textarea {
        height: 150px;
    }
    [data-testid="stAppViewContainer"] {
        --background-color: #f8f9fa;
        --text-color: #31333F;
    }
    [data-testid="stAppViewContainer"][data-theme="dark"] {
        --background-color: #262730;
        --text-color: #FFFFFF;
    }
    .result-container {
        background-color: var(--background-color);
        padding: 20px;
        border-radius: 10px;
        line-height: 1.6;
        margin-top: 2rem;
        color: var(--text-color);
    }
    </style>
""", unsafe_allow_html=True)

# 헤더
st.markdown(logo_html, unsafe_allow_html=True)

# 사이드바 - API 설정
with st.sidebar:
    st.header("API 설정")
    api_key = st.text_input("OpenAI API Key", type="password", key="api_key")
    st.info("API 키는 안전하게 보관되며, 세션이 종료되면 자동으로 삭제됩니다.")

# 메인 영역
input_type = st.radio("분석 방식 선택", ["URL", "Text"])
input_text = st.text_area("분석할 내용을 입력하세요", height=150)

def get_webpage_content(url):
    """웹페이지 내용 가져오기"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator='\n', strip=True)
        return text
    except Exception as e:
        st.error(f"웹페이지 가져오기 실패: {str(e)}")
        return None

def analyze_text(api_key_value, text):
    """텍스트 분석 함수"""
    try:
        # OpenAI API 키 설정
        openai.api_key = api_key_value
        
        prompt = """
        다음 내용을 분석하여 아래 형식으로 정리해주세요. 각 섹션과 항목에는 적절한 이모지를 추가해주세요:

        🎯 내용 요약 (핵심 포인트 5개):
        • 각 포인트는 번호를 매기고, 명확하게 구분되도록 작성
        • 각 포인트 앞에 관련 이모지 추가

        💡 주요 키워드:
        • 각 키워드와 설명을 별도 줄에 작성
        • 키워드는 굵게 강조
        • 각 키워드 앞에 관련 이모지 추가

        분석할 내용:
        """

        response = openai.ChatCompletion.create(
            model="gpt-4-0125-preview",  # GPT-4O-mini 모델
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes text and provides structured summaries."},
                {"role": "user", "content": f"{prompt}\n\n{text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"분석 중 오류가 발생했습니다: {str(e)}")
        return None

if st.button("분석 시작", type="primary"):
    if not api_key:
        st.error("❌ API 키를 입력해주세요.")
    elif not input_text:
        st.error("❌ 분석할 내용을 입력해주세요.")
    else:
        with st.spinner("분석 중..."):
            # URL인 경우 웹페이지 내용 가져오기
            if input_type == "URL":
                content = get_webpage_content(input_text)
                if not content:
                    st.stop()
            else:
                content = input_text

            # 텍스트 분석
            result = analyze_text(api_key, content)
            if result:
                st.markdown(
                    f"""<div class='result-container'>
                        <h2 style='color: var(--text-color); text-align: center;'>📊 분석 결과 📊</h2>
                        <div style='white-space: pre-wrap; margin-top: 20px;'>
                        {result.replace('•', '◾').replace('*', '★')}
                        </div>
                    </div>""",
                    unsafe_allow_html=True
                )

# 푸터
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: var(--text-color);'>
        <p>Created with ❤️ using Streamlit and OpenAI</p>
    </div>
""", unsafe_allow_html=True)
