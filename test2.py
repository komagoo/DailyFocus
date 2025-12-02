import streamlit as st
import random
import time

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
    
    /* 이미지 둥글게 */
    img {
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 데이터 준비 (명대사 & 이미지 매칭) ---
# 로컬 이미지를 사용하려면 같은 폴더에 이미지를 넣고 파일명을 맞춰주세요.
# 일단 웹 URL을 사용하여 바로 작동되도록 설정했습니다. 필요하면 파일명으로 바꾸세요!

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
        "text": "Never let them see that they get to you.",
        "kor": "그들이 널 괴롭히는 게 통했다는 걸 절대 들키지 마.",
        "char": "Nick Wilde",
        "color": "#FF9800" # 닉 오렌지
    },
    {
        "text": "Sometimes we come last, but we did our best.",
        "kor": "때로는 꼴찌를 할 수도 있어, 하지만 우린 최선을 다했잖아.",
        "char": "Gazelle & Zootopia Citizens",
        "color": "#E91E63" # 가젤 핑크
    }
]

# 세션 상태 초기화
if 'quote_index' not in st.session_state:
    st.session_state.quote_index = random.randint(0, len(quotes_data)-1)

# --- 4. 메인 화면 구성 ---

# 타이틀
st.markdown('<div class="main-title">ZOOTOPIA<br><span style="font-size:1.5rem">Motivation Station</span></div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 현재 선택된 명대사 가져오기
current_q = quotes_data[st.session_state.quote_index]

# 이미지 영역 (보여주신 이미지 2장 중 랜덤 또는 분위기에 맞는 것 출력)
# 실제 배포 시에는 'zootopia1.jpg', 'zootopia2.jpg' 처럼 파일을 업로드해서 쓰세요.
# 여기서는 예시로 플레이스홀더를 사용합니다.
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # 닉과 주디 이미지 (보여주신 이미지 1번 느낌)
    if current_q['char'] == "Nick Wilde" or "reptiles" in current_q['text']:
        # 닉이거나 2편 느낌이면 살짝 와일드한 이미지
        st.image("zootopia2.jpg", caption="Zootopia 2 Vibes", use_container_width=True)
    else:
        # 주디거나 감성적인 느낌
        st.image("zootopia1.jpg", caption="Try Everything!", use_container_width=True)

    # 명대사 카드 영역
    st.markdown(f"""
    <div class="quote-card" style="border-top: 5px solid {current_q['color']};">
        <div class="quote-text">"{current_q['text']}"</div>
        <div style="color: #ddd; font-size: 1rem; margin-bottom:15px;">{current_q['kor']}</div>
        <div class="character-name">- {current_q['char']} -</div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. 버튼 (Try Everything) ---
_, btn_col, _ = st.columns([1, 4, 1])
with btn_col:
    if st.button("🥕 Try Everything! (새로운 명언 보기)"):
        # 로딩 효과 (주디가 뛰어가는 느낌)
        with st.spinner('🐰 주디가 명언을 배달하고 있습니다...'):
            time.sleep(0.8) # 0.8초 딜레이로 기대감 조성
            # 새로운 랜덤 인덱스 (같은 거 안 나오게)
            new_idx = random.randint(0, len(quotes_data)-1)
            while new_idx == st.session_state.quote_index:
                new_idx = random.randint(0, len(quotes_data)-1)
            st.session_state.quote_index = new_idx
            st.rerun()

# 하단 푸터
st.markdown("""
<div style="text-align:center; color:rgba(255,255,255,0.5); margin-top:50px; font-size:0.8rem;">
    Anyone can be Anything. 🐾<br>
    Created with Zootopia Spirit
</div>
""", unsafe_allow_html=True)