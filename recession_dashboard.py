import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 정의
data = {
    "Date": ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06", "2025-07"],
    "LEI": [-1.07, -1.46, -1.76, -2.56, -2.08, -2.18, None],
    "CEI": [2.15, 2.14, 2.59, 2.68, 2.23, 2.31, None],
    "Sahm Rule": [0.37, 0.27, 0.27, 0.27, 0.27, 0.17, 0.10],
    "Global Recession Probability": [34.51, 29.03, 28.54, 26.96, 33.36, 38.97, 41.96],
    "PMI 제조업": [50.9, 50.3, 49, 48.7, 48.5, 49, 48],
    "PMI 서비스업": [52.8, 53.5, 50.8, 51.6, 49.9, 50.8, 48],
    "미국 기대 성장률": [2.18, 2.25, 1.93, 1.43, 1.44, 1.55, 1.56]
}
df = pd.DataFrame(data)

us_df = pd.DataFrame({
    "Date": ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10"],
    "Probability": [61.47, 58.31, 58.31, 50.04, 51.82, 55.83, 56.29, 61.79, 57.06, 42.05]
})

# 평가 함수 정의
def evaluate_lei(df):
    latest, prev = df["LEI"].dropna().iloc[-1], df["LEI"].dropna().iloc[-2]
    return "위험" if latest < 0 and latest < prev else "양호"

def evaluate_cei(df):
    cei_vals = df["CEI"].dropna()
    return "위험" if len(cei_vals) >= 3 and all(cei_vals.iloc[-i] < cei_vals.iloc[-i - 1] for i in range(1, 3)) else "양호"

def evaluate_sahm(df):
    return "위험" if df["Sahm Rule"].dropna().iloc[-1] >= 0.5 else "양호"

def evaluate_global(df):
    global_vals = df["Global Recession Probability"].dropna()
    return "위험" if len(global_vals) >= 3 and all(global_vals.iloc[-i] > global_vals.iloc[-i - 1] for i in range(1, 3)) else "양호"

def evaluate_pmi(series):
    return "위험" if len(series) >= 3 and all(val < 50 for val in series[-3:]) else "양호"

# 지표 평가 및 신뢰도 설정
results = {
    "LEI (선행지수, 신뢰도 매우 높음)": evaluate_lei(df),
    "CEI (동행지수, 신뢰도 낮음)": evaluate_cei(df),
    "Sahm Rule (신뢰도 높음)": evaluate_sahm(df),
    "세계 침체 확률 (신뢰도 중상)": evaluate_global(df),
    "제조업 PMI (신뢰도 중간)": evaluate_pmi(df["PMI 제조업"]),
    "서비스업 PMI (신뢰도 중간)": evaluate_pmi(df["PMI 서비스업"])
}

danger_count = list(results.values()).count("위험")
probability = int((danger_count / len(results)) * 100)

if danger_count <= 1:
    conclusion = "매우 안전"
elif danger_count == 2:
    conclusion = "안전"
elif danger_count == 3:
    conclusion = "투자 주의 요망"
elif danger_count in [4, 5]:
    conclusion = "침체 진입 주의"
else:
    conclusion = "침체 확정"

# Streamlit 앱 구성
st.set_page_config(page_title="침체신호기", layout="wide")
st.title("경제 침체 리스크 대시보드")

st.subheader("주요 지표 평가 결과")
for name, status in results.items():
    color = "red" if status == "위험" else "green"
    st.markdown(f"- **{name}** → <span style='color:{color}'>{status}</span>", unsafe_allow_html=True)

st.subheader("종합 진단 결과")
st.markdown(f"<h4 style='color:red'>{conclusion}</h4>", unsafe_allow_html=True)
st.markdown(f"**현재 침체 확률: {probability}%**")

st.subheader("미국 1년 내 침체 확률")
fig1, ax1 = plt.subplots()
ax1.plot(us_df["Date"], us_df["Probability"], marker="o", color="crimson")
ax1.set_ylim(0, 70)
ax1.set_ylabel("확률 (%)")
ax1.set_xticks(us_df["Date"])
ax1.set_xticklabels(us_df["Date"], rotation=45)
ax1.grid(True, linestyle="--", alpha=0.5)
st.pyplot(fig1)

st.subheader("미국 기대 성장률")
fig2, ax2 = plt.subplots()
ax2.plot(df["Date"], df["미국 기대 성장률"], marker="o", color="navy")
ax2.set_ylim(0, 3)
ax2.set_ylabel("성장률 (%)")
ax2.set_xticks(df["Date"])
ax2.set_xticklabels(df["Date"], rotation=45)
ax2.grid(True, linestyle="--", alpha=0.5)
st.pyplot(fig2)

st.caption("제작: 투자하는아빠곰 | 무단 배포 금지")
