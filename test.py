import streamlit as st
import random
from datetime import datetime, date

# 1. 페이지 설정 (한눈에 들어오도록 레이아웃을 'centered'로 변경)
st.set_page_config(
    page_title="오늘의 목표",
    page_icon="📝",
    layout="centered"
)

# 2. 깔끔하고 눈이 편한 모던 CSS 적용
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    
    /* 전체 폰트 적용 */
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 상단 날짜 카드 */
    .date-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: #555;
        font-weight: 700;
        margin-bottom: 20px;
    }

    /* 명언 박스 디자인 (심플하고 차분하게) */
    .quote-box {
        background-color: #ffffff;
        border-left: 5px solid #4CAF50;
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 30px;
        text-align: center;
    }
    .quote-text {
        font-size: 1.3rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 10px;
    }
    .quote-author {
        font-size: 0.9rem;
        color: #888;
    }

    /* 목표 리스트 컨테이너 */
    .goal-container {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #eee;
    }

    /* 목표 아이템 스타일 */
    .goal-item {
        font-size: 1.1rem;
        padding: 10px;
        border-bottom: 1px solid #f0f0f0;
    }
    .completed {
        text-decoration: line-through;
        color: #bbb;
    }

    /* 입력창 및 버튼 스타일 조정 */
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    .stButton > button {
        border-radius: 10px;
        width: 100%;
    }
    
    /* 프로그레스 바 색상 변경 */
    .stProgress > div > div {
        background-color: #4CAF50 !important;
    }
</style>
""", unsafe_allow_html=True)

# 명언 리스트
QUOTES = [
    ("자신을 아는 것이 모든 지혜의 시작이다", "- 아리스토텔레스"),
    ("검토되지 않은 삶은 살 가치가 없다", "- 소크라테스"),
    ("고통 없이는 얻는 것도 없다", "- 벤저민 프랭클린"),
    ("가장 큰 영광은 넘어지지 않는 것이 아니라 일어서는 것이다", "- 공자"),
    ("지금 이 순간을 살아라", "- 마르쿠스 아우렐리우스"),
    ("시작이 반이다", "- 아리스토텔레스"),
    ("멈추지 않는 한 얼마나 천천히 가는지는 중요하지 않다", "- 공자"),
    ("태도는 사소한 것이지만 그것이 만드는 차이는 엄청나다", "- 윈스턴 처칠"),
    ("행동이 없으면 결과도 없다", "- 간디"),
    ("오늘 할 수 있는 일을 내일로 미루지 마라", "- 벤저민 프랭클린")
]

# 세션 상태 초기화
if 'goals' not in st.session_state:
    st.session_state.goals = []
if 'last_date' not in st.session_state:
    st.session_state.last_date = str(date.today())
if 'today_quote' not in st.session_state:
    st.session_state.today_quote = random.choice(QUOTES)

# 날짜 변경 체크 및 초기화
today = str(date.today())
if st.session_state.last_date != today:
    st.session_state.today_quote = random.choice(QUOTES)
    st.session_state.last_date = today
    # 날짜 바뀌어도 목표는 유지할지, 초기화할지 선택 (여기선 초기화 유지)
    st.session_state.goals = []

# --- UI 구성 시작 ---

# 1. 상단 헤더 (날짜)
now = datetime.now()
date_str = f"{now.year}년 {now.month}월 {now.day}일 {['월','화','수','목','금','토','일'][now.weekday()]}요일"
st.markdown(f'<div class="date-card">📅 {date_str}</div>', unsafe_allow_html=True)

# 2. 명언 섹션 (깔끔한 박스 형태)
quote, author = st.session_state.today_quote
st.markdown(f"""
    <div class="quote-box">
        <div class="quote-text">"{quote}"</div>
        <div class="quote-author">{author}</div>
    </div>
""", unsafe_allow_html=True)

# 3. 목표 관리 섹션 (메인 카드)
st.markdown('<div class="goal-container">', unsafe_allow_html=True)
st.markdown("### 📝 오늘의 목표")

# 목표 입력창 (레이아웃 조정)
col1, col2 = st.columns([4, 1])
with col1:
    new_goal = st.text_input("목표 입력", placeholder="오늘 할 일을 입력하세요", label_visibility="collapsed", key="goal_input")
with col2:
    if st.button("추가", type="primary"): # type="primary"로 강조
        if new_goal.strip():
            st.session_state.goals.append({"text": new_goal, "completed": False})
            st.rerun()

st.markdown("---") # 구분선

# 목표 리스트 출력
if st.session_state.goals:
    for idx, goal in enumerate(st.session_state.goals):
        c1, c2, c3 = st.columns([0.5, 5, 0.5])
        
        with c1:
            # 완료 체크박스
            if st.checkbox("", value=goal["completed"], key=f"check_{idx}", label_visibility="collapsed"):
                st.session_state.goals[idx]["completed"] = not st.session_state.goals[idx]["completed"]
                st.rerun()
        
        with c2:
            # 텍스트 표시
            style_class = "completed" if goal["completed"] else ""
            # HTML 대신 Streamlit native markdown 사용하여 정렬 맞춤
            if goal["completed"]:
                st.markdown(f"<span style='color:#bbb; text-decoration:line-through;'>{goal['text']}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span>{goal['text']}</span>", unsafe_allow_html=True)
                
        with c3:
            # 삭제 버튼 (작고 심플하게)
            if st.button("✕", key=f"del_{idx}"):
                st.session_state.goals.pop(idx)
                st.rerun()

    # 진행률 표시
    st.markdown("<br>", unsafe_allow_html=True)
    completed_count = sum(1 for g in st.session_state.goals if g["completed"])
    total_count = len(st.session_state.goals)
    progress = completed_count / total_count if total_count > 0 else 0
    
    st.progress(progress)
    st.caption(f"진행률: {int(progress * 100)}% ({completed_count}/{total_count})")
    
    if progress == 1.0 and total_count > 0:
        st.success("🎉 모든 목표를 달성했습니다! 수고하셨어요!")
        st.balloons()

else:
    st.info("오늘의 첫 목표를 등록해보세요!")

st.markdown('</div>', unsafe_allow_html=True) # goal-container 닫기

# 하단 명언 새로고침 (작은 텍스트 버튼으로 변경하여 시선 분산 방지)
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 다른 명언 보기"):
    st.session_state.today_quote = random.choice(QUOTES)
    st.rerun()
#