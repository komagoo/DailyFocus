import streamlit as st
import random
import time
import os # 파일 존재 여부 확인용

# --- 1. 페이지 설정 (주토피아 테마) ---
st.set_page_config(
    page_title="Zootopia: Try Everything",
    page_icon="🚔",
    layout="centered"
)

# --- 2. 과몰입 CSS 스타일링 (주토피아 분위기 연출) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&family=Noto+Sans+KR:wght@400;700&display=swap');

    /* 전체 배경: 주토피아의 밤과 새벽 사이 그라데이션 */
    .stApp {
        background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%);
        font-family: 'Fredoka', 'Noto Sans KR', sans-serif;
    }

    /* 메인 타이틀 스타일 */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: -webkit-linear-gradient(#00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        text-shadow: 0px 0px 20px rgba(0, 210, 255, 0.5);
    }

    /* 명대사 카드 (유리 같은 느낌 - Glassmorphism) */
    .quote-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 40px;
        border: 2px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        text-align: center;
        margin-bottom: 30px;
        transition: transform 0.3s ease;
    }
    .quote-card:hover {
        transform: scale(1.02);
        border-color: #ff9966; /* 닉의 오렌지색 포인트 */
    }

    /* 명대사 텍스트 */
    .quote-text {
        font-size: 1.8rem;
        color: #ffffff;
        font-weight: 600;
        line-height: 1.6;
        margin-bottom: 20px;
        font-style: italic;
    }

    /* 캐릭터 이름 */
    .character-name {
        font-size: 1.2rem;
        color: #ffcc00; /* ZPD 뱃지 골드 */
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* 버튼 스타일 (주디의 당근 볼펜 느낌) */
    .stButton>button {
        background: linear-gradient(90deg, #FF8008 0%, #FFC837 100%);
        color: white;
        font-size: 1.2rem;
        padding: 15px 30px;
        border-radius: 50px;
        border: none;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(255, 128, 8, 0.4);
        width: 100%;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(255, 128, 8, 0.6);
    }
    
    /* 이미지 스타일 */
    img {
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        transition: all 0.3s ease-in-out;
    }
    img:hover {
        transform: scale(1.01);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 데이터 준비 ---

# 3.1 명대사 데이터
quotes_data = [
    {
        "text": "When you two save the city.. maybe everyone will see reptiles ain't that different.",
        "kor": "너희 둘이 도시를 구하면.. 아마 모두가 파충류도 다르지 않다는 걸 알게 될 거야.",
        "char": "Gary (Zootopia 2)",
        "color": "#4CAF50" # 뱀(Reptile) 그린
    },
    {
        "text": "No matter what type of animal you are, change starts with you.",
        "kor": "네가 어떤 동물이든, 변화는 너로부터 시작해.",
        "char": "Judy Hopps",
        "color": "#3a7bd5" # 주디 블루
    },
    {
        "text": "Life's a little bit messy. We all make mistakes.",
        "kor": "삶은 조금 엉망진창이야. 우린 모두 실수를 하지.",
        "char": "Judy Hopps",
        "color": "#9C27B0" # 감성 퍼플
    },
    {
        "text": "It's called a hustle, sweetheart.",
        "kor": "이게 바로 인생의 기술이야, 자기야.",
        "char": "Nick Wilde",
        "color": "#FF9800" # 닉 오렌지
    },
    {
        "text": "I won't let fear divide us.",
        "kor": "난 두려움이 우리를 갈라놓도록 내버려두지 않을 거야.",
        "char": "Nick Wilde",
        "color": "#FF9800" # 닉 오렌지
    },
        {
        "text": "Never let them see that they get to you.",
        "kor": "그들이 널 괴롭히는 게 통했다는 걸 절대 들키지 마.",
        "char": "Nick Wilde",
        "color": "#FF9800" # 닉 오렌지
    },
    {
        "text": "Sometimes we come last, but we did our best.",
        "kor": "때로는 꼴찌를 할 수도 있어, 하지만 우린 최선을 다했잖아.",
        "char": "OST - Try Everything",
        "color": "#E91E63" # 가젤 핑크
    }
]

# 3.2 이미지 파일 리스트 (5장)
image_files = [
    "zootopia1.jpg",
    "zootopia2.jpg",
    "zootopia3.jpg",
    "zootopia4.jpg",
    "zootopia5.jpg"
]

# --- 4. 세션 상태 초기화 (새로고침해도 유지되도록) ---
if 'quote_index' not in st.session_state:
    st.session_state.quote_index = random.randint(0, len(quotes_data)-1)

# 이미지 인덱스도 세션에 저장
if 'image_index' not in st.session_state:
    # 파일이 하나라도 있을 때만 인덱스 생성
    if len(image_files) > 0:
        st.session_state.image_index = random.randint(0, len(image_files)-1)
    else:
        st.session_state.image_index = -1 # 이미지가 없을 경우 대비

# --- 5. 메인 화면 구성 ---

# 타이틀
st.markdown('<div class="main-title">ZOOTOPIA<br><span style="font-size:1.5rem">Motivation Station</span></div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 현재 선택된 데이터 가져오기
current_q = quotes_data[st.session_state.quote_index]

# 레이아웃 컬럼
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # --- 이미지 표시 영역 ---
    # 현재 인덱스의 이미지 파일명 가져오기
    if st.session_state.image_index != -1:
        current_image_file = image_files[st.session_state.image_index]
        
        # 파일이 실제로 존재하는지 확인 후 표시 (에러 방지)
        if os.path.exists(current_image_file):
            st.image(current_image_file, caption="Zootopia Vibes 🐾", use_container_width=True)
        else:
            # 이미지를 찾지 못했을 때 표시할 대체 텍스트 (혹은 기본 이미지 URL)
            st.warning(f"이미지 파일을 찾을 수 없습니다: {current_image_file}")
            st.info("zootopia1.jpg ~ zootopia5.jpg 파일을 파이썬 파일과 같은 폴더에 넣어주세요.")

    # --- 명대사 카드 영역 ---
    st.markdown(f"""
    <div class="quote-card" style="border-top: 5px solid {current_q['color']};">
        <div class="quote-text">"{current_q['text']}"</div>
        <div style="color: #ddd; font-size: 1rem; margin-bottom:15px;">{current_q['kor']}</div>
        <div class="character-name">- {current_q['char']} -</div>
    </div>
    """, unsafe_allow_html=True)

# --- 6. 버튼 (Try Everything) ---
_, btn_col, _ = st.columns([1, 4, 1])
with btn_col:
    if st.button("🥕 Try Everything! (새로운 영감 얻기)"):
        # 로딩 효과
        with st.spinner('🐰 주디와 닉이 새로운 영감을 찾아오고 있습니다...'):
            time.sleep(0.6) # 약간의 딜레이

            # 1. 새로운 명언 인덱스 뽑기 (중복 방지)
            new_quote_idx = random.randint(0, len(quotes_data)-1)
            while new_quote_idx == st.session_state.quote_index and len(quotes_data) > 1:
                new_quote_idx = random.randint(0, len(quotes_data)-1)
            st.session_state.quote_index = new_quote_idx

            # 2. 새로운 이미지 인덱스 뽑기 (중복 방지, 이미지가 2장 이상일 때만)
            if len(image_files) > 1:
                new_image_idx = random.randint(0, len(image_files)-1)
                while new_image_idx == st.session_state.image_index:
                    new_image_idx = random.randint(0, len(image_files)-1)
                st.session_state.image_index = new_image_idx

            st.rerun()

# 하단 푸터
st.markdown("""
<div style="text-align:center; color:rgba(255,255,255,0.5); margin-top:50px; font-size:0.8rem;">
    Anyone can be Anything. 🐾<br>
    Created with Zootopia Spirit
</div>
""", unsafe_allow_html=True)