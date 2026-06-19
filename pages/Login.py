import streamlit as st

# ----------------------------------
# Page Config
# ----------------------------------
st.set_page_config(
    page_title="Talent Logic X",
    page_icon="🧠",
    layout="wide"
)

# ----------------------------------
# Global CSS
# ----------------------------------
st.markdown("""
<style>
/* Hide Streamlit UI */
[data-testid="stSidebar"] {display: none;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Navbar */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 40px;
    border-bottom: 1px solid #eaeaea;
}
.brand {
    font-size: 1.4rem;
    font-weight: 700;
}
.nav-buttons button {
    margin-left: 10px;
}

/* Hero */
.hero {
    padding: 80px 40px;
}
.hero h1 {
    font-size: 3.2rem;
    margin-bottom: 10px;
}
.hero p {
    font-size: 1.3rem;
    color: #6c757d;
}

/* Feature cards */
.card {
    padding: 25px;
    border-radius: 14px;
    background: #ffffff;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    height: 100%;
}

/* Footer */
.footer {
    margin-top: 80px;
    padding: 20px 0;
    color: #999;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# NAVBAR
# ----------------------------------
nav_left, nav_right = st.columns([6, 2])

with nav_left:
    st.markdown("<div class='brand'>🧠 Talent Logic X</div>", unsafe_allow_html=True)

with nav_right:
    col_login, col_signup = st.columns(2)
    with col_login:
        if st.button("Login"):
            st.switch_page("pages/Login.py")
    with col_signup:
        if st.button("Sign Up", type="primary"):
            st.switch_page("pages/Signup.py")

st.divider()

# ----------------------------------
# HERO SECTION
# ----------------------------------
st.markdown("""
<div class="hero">
    <h1>Explainable AI for Resume Screening</h1>
    <p>
        Hire smarter with transparent, bias-aware, and auditable AI decisions.
        Built for recruiters who care about fairness and clarity.
    </p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------
# FEATURES
# ----------------------------------
f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("""
    <div class="card">
        <h3>🔍 Transparent Scoring</h3>
        <p>
            Every resume score comes with a clear explanation —
            skills, education, and experience fully visible.
        </p>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="card">
        <h3>⚖️ Bias Mitigation</h3>
        <p>
            Designed to reduce hidden bias and unfair filtering
            using ethical AI principles.
        </p>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="card">
        <h3>🚀 Recruiter Ready</h3>
        <p>
            Fast screening, scalable pipelines, and dashboard-ready
            insights for hiring teams.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------
# CTA SECTION
# ----------------------------------
st.markdown("<br><br>", unsafe_allow_html=True)

cta_col1, cta_col2, _ = st.columns([1, 1, 2])

with cta_col1:
    if st.button("Get Started →", type="primary", use_container_width=True):
        st.switch_page("pages/Signup.py")

with cta_col2:
    if st.button("View Demo", use_container_width=True):
        st.switch_page("pages/Login.py")

# ----------------------------------
# FOOTER
# ----------------------------------
st.markdown("""
<div class="footer">
    Talent Logic X · Ethical AI for Hiring · © 2026
</div>
""", unsafe_allow_html=True)