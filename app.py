import streamlit as st
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score, cross_val_predict
from sklearn.metrics import recall_score, precision_score
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

features = ["ER40_CR", "PicSeq_AgeAdj", "Flanker_AgeAdj", "PSQI_Score"]

@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    return df.dropna(subset=features + ["PMAT24_A_CR", "LifeSatisf_Unadj"])

@st.cache_data
def run_models(df):
    df = df.copy()

    # regression
    reg = LinearRegression().fit(df[features], df["PMAT24_A_CR"])

    # clustering into segments
    X = StandardScaler().fit_transform(df[features])
    df["cluster"] = KMeans(n_clusters=3, random_state=42, n_init=10).fit_predict(X)
    means = df.groupby("cluster")[["PSQI_Score", "PMAT24_A_CR"]].mean()
    burnout = means["PSQI_Score"].idxmax()
    high = means["PMAT24_A_CR"].drop(burnout).idxmax()
    names = {c: "Low-Focus Average" for c in means.index}
    names[burnout] = "Burnout-Risk"
    names[high] = "High Performers"
    df["segment"] = df["cluster"].map(names)

    # random forest for top performers
    df["top"] = (df["PMAT24_A_CR"] >= df["PMAT24_A_CR"].quantile(0.8)).astype(int)
    cols = features + ["LifeSatisf_Unadj"]
    X_train, X_test, y_train, y_test = train_test_split(
        df[cols], df["top"], test_size=0.2, random_state=42, stratify=df["top"])
    rf = RandomForestClassifier(random_state=42).fit(X_train, y_train)
    report = classification_report(y_test, rf.predict(X_test), output_dict=True)

    return reg, rf, report, df

df = load_data()
reg, rf, report, df = run_models(df)

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Cognitive Intelligence Portfolio", layout="wide", initial_sidebar_state="expanded")

# --- 2. SIDEBAR NAVIGATION ---
st.sidebar.title("🧠 The Biological Engines of Intelligence")
st.sidebar.markdown("Navigate through the findings of the cognitive data analysis project.")

page = st.sidebar.radio(
"Select Analysis Phase:",
("Welcome & Overview",
 "Business Overview (KPIs)",
 "Segments & Actions",
 "What Drives Performance",
 "Recommendations & Limitations",
 "The Interactive Biological Engine (All Angles)")
)

# --- GLOBAL CSS OVERRIDE (APPLIES TO ALL PAGES) ---
# --- GLOBAL CSS OVERRIDE (APPLIES TO ALL PAGES) ---
st.markdown(
    """
    <style>
    /* Faded Background Image using CSS Gradient Blending */
    /* This paints a 90% dark overlay directly on top of the image to give it exactly 10% opacity */
    [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(rgba(14, 17, 23, 0.90), rgba(14, 17, 23, 0.90)), 
                          url("https://t4.ftcdn.net/jpg/04/30/43/27/360_F_430432733_8Bx9ZSqRWXurfGIRlpBHgL1b1mk2D86C.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Ensures the sidebar remains perfectly dark and readable */
    [data-testid="stSidebar"] {
        background-color: #0E1117;
    }

    /* Custom slide container styling */
    .slide-container {
        background-color: rgba(30, 34, 43, 0.7);
        padding: 40px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if page == "Business Overview (KPIs)":
    st.title("Cognitive Performance & Wellness Analytics")
    st.markdown("Which performance profiles are at risk, and which levers matter most?")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg Logic Score", round(df["PMAT24_A_CR"].mean(), 1))
    c2.metric("High Performers", f"{df['top'].mean():.0%}")
    c3.metric("Burnout-Risk Segment", f"{(df['segment'] == 'Burnout-Risk').mean():.0%}")
    c4.metric("Avg Sleep Problem Score", round(df["PSQI_Score"].mean(), 1))
    st.caption("High performer = logic score at or above the 80th percentile. Sleep problem score: lower is better.")

    st.subheader("Workforce split by segment")
    st.bar_chart(df["segment"].value_counts())

# --- 3. PAGE: THE GRAND SYNTHESIS ---
# --- 3. PAGE: WELCOME & OVERVIEW ---
if page == "Welcome & Overview":
    
    # 1. Session State for the Slider Pages
    if "slide_index" not in st.session_state:
        st.session_state.slide_index = 0

    def next_slide():
        if st.session_state.slide_index < 3:
            st.session_state.slide_index += 1

    def prev_slide():
        if st.session_state.slide_index > 0:
            st.session_state.slide_index -= 1

    # 2. Slide Content (Headers are now strictly inside the boxes)
    if st.session_state.slide_index == 0:
        st.markdown("""
        <div class="slide-container">
            <h1 style='text-align: center; color: #4DA8DA; margin-bottom: 20px;'>Welcome to the Cognitive Carnival</h1>
            <div style='font-size: 20px; line-height: 1.6; text-align: center;'>
            Intelligence isn't just about how well you score on a test. It is a biological engine driven by your daily habits, your emotional state, and your environment. <br><br>
            This interactive data science dashboard explores a critical question: <b>How do factors like toxic sleep, emotional awareness, environmental stress, and the brain's raw capacity to retain and manipulate active information physically dictate our logical computing power?</b><br><br>
            <i>Click <b>Next</b> to see how we decoded the human brain.</i>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.slide_index == 1:
        st.markdown("""
        <div class="slide-container">
            <h2 style='color: #4DA8DA;'>Where Did the Data Come From?</h2>
            <hr style="border-color: rgba(255,255,255,0.1);">
            <div style='font-size: 18px; line-height: 1.6;'>
            This project strictly utilizes data from the <b>Human Connectome Project (HCP) 1200 Subjects Release</b>, a major neuroscience initiative funded by the National Institutes of Health (NIH). <br><br>
            The HCP's core objective was to construct a comprehensive map of human brain circuitry and its relationship to behavior. The metrics used in this dashboard are not self-reported guesses; they are rigorous, standardized clinical assessments (utilizing the NIH Toolbox) that measure exact cognitive output, psychological well-being, and biological maintenance in healthy adults.
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.slide_index == 2:
        st.markdown("""
        <div class="slide-container">
            <h2 style='color: #4DA8DA;'>Translating the Science</h2>
            <hr style="border-color: rgba(255,255,255,0.1);">
            <div style='font-size: 18px; line-height: 1.8;'>
            Before we analyze the brain, here is exactly what our scientific variables mean in plain English:<br><br>
             🧠 <b style='color: #A2D5F2;'>Fluid Intelligence (PMAT24):</b> <i style='color: white;'>The ultimate logic and problem-solving score. This is the "brain power" we are trying to predict.</i><br>
             💤 <b style='color: #FF6B6B;'>The Sleep Penalty (PSQI):</b> <i style='color: white;'>A measure of sleep deprivation. A high score indicates toxic, poor-quality sleep.</i><br>
             ❤️ <b style='color: #FF8E8B;'>Emotional Intelligence (ER40):</b> <i style='color: white;'>The subject's ability to accurately read and process human emotions.</i><br>
             💾 <b style='color: #A2D5F2;'>Working Memory (PicSeq):</b> <i style='color: white;'>The brain's raw hardware capacity to store and recall visual information.</i><br>
             🎯 <b style='color: #A2D5F2;'>Pure Focus (Flanker):</b> <i style='color: white;'>The biological ability to maintain strict attention and ignore outside distractions.</i><br>
             🧘 <b style='color: #6BCB77;'>Stress-Free Metric (LifeSatisf):</b> <i style='color: white;'>Overall life satisfaction, used as a baseline indicator of a low-stress, low-cortisol environment.</i>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.slide_index == 3:
        st.markdown("""
        <div class="slide-container">
            <h2 style='color: #4DA8DA;'>How We Decoded the Data</h2>
            <hr style="border-color: rgba(255,255,255,0.1);">
            <div style='font-size: 18px; line-height: 1.6;'>
            This project uses three distinct machine learning algorithms to uncover different layers of human performance:<br><br>
            <b>1. Finding the Baseline</b> <i><span style='color: #888;'>(Multiple Linear Regression)</span></i>: We first looked at the entire population to find out which biological traits drive our average, everyday problem-solving skills.<br><br>
            <b>2. Discovering Hidden Tribes</b> <i><span style='color: #888;'>(K-Means Clustering)</span></i>: We used an unsupervised algorithm to group subjects based purely on their biological similarities. This revealed a fascinating "Burnout Override" group.<br><br>
            <b>3. Sorting the Elite</b> <i><span style='color: #888;'>(Random Forest Classification)</span></i>: Finally, we isolated the top 20% of the smartest individuals to figure out the exact biological bottleneck required to reach genius-level logic.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 3. Navigation Buttons (Previous / Next)
    col1, col2, col3 = st.columns([1, 8, 1])
    with col1:
        st.button("⬅️ Prev", on_click=prev_slide, disabled=(st.session_state.slide_index == 0))
    with col3:
        st.button("Next ➡️", on_click=next_slide, disabled=(st.session_state.slide_index == 3))
if page == "Recommendations & Limitations":
    st.title("Recommendations & Limitations")

    poor = df["PSQI_Score"] > 5
    mem_top = df["PicSeq_AgeAdj"] >= df["PicSeq_AgeAdj"].quantile(0.75)
    mem_low = df["PicSeq_AgeAdj"] <= df["PicSeq_AgeAdj"].quantile(0.25)
    burnout_share = (df["segment"] == "Burnout-Risk").mean()

    st.subheader("What the data supports")
    st.success(f"**1. Make sleep support a priority.** {poor.mean():.0%} of people score above 5 on the sleep problems scale, a common cut-off for poor sleep. Only {df[poor]['top'].mean():.0%} of them are high performers, against {df[~poor]['top'].mean():.0%} of everyone else.")
    st.success(f"**2. Invest in memory and focus training.** {df[mem_top]['top'].mean():.0%} of people in the top quarter for memory are high performers, against {df[mem_low]['top'].mean():.0%} in the bottom quarter.")
    st.success(f"**3. Target support by segment.** {burnout_share:.0%} of people fall in the Burnout-Risk segment. Start sleep and workload support there (see Segments & Actions).")

    st.subheader("Limitations")
    st.warning("""
- This is correlation, not proof of cause and effect.
- The data is from healthy adults in the Human Connectome Project, not employees. It is used here as a stand-in for a workforce.
- The models explain only part of logic scores (see What Drives Performance).
- Logic score is one measure of performance, not the whole picture.
""")

# --- 4. PAGE:segments and actions---
elif page == "Segments & Actions":
    st.title("Performance Segments and Recommended Actions")
    st.markdown("K-Means grouped people into three segments using memory, focus, emotion recognition and sleep.")

    cols = ["PMAT24_A_CR", "PicSeq_AgeAdj", "Flanker_AgeAdj", "ER40_CR", "PSQI_Score"]
    summary = df.groupby("segment")[cols].mean().round(1)
    summary.insert(0, "People", df["segment"].value_counts())
    summary = summary.rename(columns={
        "PMAT24_A_CR": "Logic Score",
        "PicSeq_AgeAdj": "Memory",
        "Flanker_AgeAdj": "Focus",
        "ER40_CR": "Emotion Recognition",
        "PSQI_Score": "Sleep Problems"})
    st.dataframe(summary)

    st.subheader("Average logic score by segment")
    st.bar_chart(summary["Logic Score"])
    st.caption("Sleep Problems: higher is worse. Score gaps between segments are small, so read these as risk profiles, not proof that one factor alone drives performance.")

    st.subheader("Recommended actions")
    st.error("**Burnout-Risk:** Sleep problems stand out in this group. Make it the priority for sleep and workload support, such as flexible hours and a wellness programme.")
    st.info("**Low-Focus Average:** Sleep is fine, but memory and focus are the lowest of the three groups. Try focus training and fewer interruptions.")
    st.success("**High Performers:** Strong memory and focus with healthy sleep. Protect their workload and use them as mentors on complex tasks.")


# --- 5. PAGE: what drives performance ---
elif page == "What Drives Performance":
    st.title("What Drives Performance")
    st.markdown("Two views: what moves the average logic score, and what separates high performers.")

    st.subheader("1. Average logic score (regression)")
    X_scaled = StandardScaler().fit_transform(df[features])
    reg_model = LinearRegression().fit(X_scaled, df["PMAT24_A_CR"])
    st.metric("R-squared", f"{reg_model.score(X_scaled, df['PMAT24_A_CR']):.1%}")
    weights = pd.Series(reg_model.coef_, index=["Emotion", "Memory", "Focus", "Sleep Problems"])
    st.bar_chart(weights)
    st.caption("Weights are standardized, so bars are directly comparable. Negative means lower logic scores.")

    st.subheader("2. High performers (classification)")
    cols = features + ["LifeSatisf_Unadj"]
    model = make_pipeline(StandardScaler(), LogisticRegression(class_weight="balanced", max_iter=1000))
    cv = StratifiedKFold(5, shuffle=True, random_state=42)
    auc = cross_val_score(model, df[cols], df["top"], cv=cv, scoring="roc_auc").mean()
    pred = cross_val_predict(model, df[cols], df["top"], cv=cv)

    c1, c2, c3 = st.columns(3)
    c1.metric("AUC (0.5 = random guess)", f"{auc:.2f}")
    c2.metric("Recall", f"{recall_score(df['top'], pred):.0%}")
    c3.metric("Precision", f"{precision_score(df['top'], pred):.0%}")

    model.fit(df[cols], df["top"])
    importance = pd.Series(model[-1].coef_[0],
                           index=["Emotion", "Memory", "Focus", "Sleep Problems", "Life Satisfaction"])
    st.bar_chart(importance)
    st.caption("Recall = share of real high performers caught. Precision = share of the model's picks that are right. All scores are 5-fold cross-validated.")

    st.info("**Takeaway:** Memory is the strongest lever, emotion recognition and life satisfaction help, and sleep problems pull scores down. These factors explain only part of logic scores, so use them to spot patterns, not to judge individuals.")

# --- 6. NEW PAGE: INTERACTIVE BIOLOGICAL ENGINE ---
elif page == "The Interactive Biological Engine (All Angles)":
    st.title("⚙️ The Interactive Biological Engine")
    st.markdown("Explore how the brain's reliance on different cognitive tools shifts depending on the environment and the required task.")
    
    # Interactive Selector
   # --- START OF REPLACEMENT CODE ---
    
    # Interactive Selector (Fixed and Stabilized)
    cognitive_state = st.radio(
        "**Select the Cognitive State to Analyze:**",
        options=["The Burnout State (Angle 2)", "The Everyday Baseline (Angle 1)", "The Elite State (Angle 3)"],
        horizontal=True
    )
    
    st.divider()
    
    # Engine Output Panels
    if cognitive_state == "The Everyday Baseline (Angle 1)":
        st.subheader("State: The Everyday Baseline")
        st.markdown("*Represented by the Multiple Linear Regression Model.*")
        st.info("**Biological Reality:** To survive average daily logic puzzles, the brain relies on its social operating system. Emotional intelligence handles the heavy lifting, while basic sleep ensures the system doesn't crash. Raw memory capacity takes a back seat.")
        
        st.markdown("#### Active Biological Engines:")
        st.progress(80, text="🟢 Emotional Processing Engine (80% Power)")
        st.progress(60, text="🟢 Basic Rest & Maintenance (60% Power)")
        st.progress(20, text="⚪ Working Memory Hardware (20% Power)")
        
    elif cognitive_state == "The Burnout State (Angle 2)":
        st.subheader("State: The Burnout Override")
        st.markdown("*Represented by Tribe 1 in the K-Means Clustering Model.*")
        st.error("**Biological Reality:** The subject has superior working memory and focus hardware, but toxic sleep deprivation (PSQI = 9.2) has triggered a system override. The brain physically cannot access its own hardware, causing logic scores to crash below average levels.")
        
        st.markdown("#### Active Biological Engines:")
        st.progress(95, text="🔴 Sleep Deprivation Toxin Level (CRITICAL OVERRIDE)")
        st.progress(10, text="🔴 Accessible Logic Output (10% Power)")
        st.progress(85, text="⚪ Blocked Memory Hardware (Offline due to fatigue)")

    elif cognitive_state == "The Elite State (Angle 3)":
        st.subheader("State: The Elite Bottleneck")
        st.markdown("*Represented by the Random Forest Classification Model.*")
        st.success("**Biological Reality:** To solve the most complex 20% of logic puzzles, the brain requires massive, undisturbed hardware. Working Memory and a completely stress-free mind (Life Satisfaction) ignite at maximum power, pushing the brain to its absolute limits.")
        
        st.markdown("#### Active Biological Engines:")
        st.progress(95, text="🟢 Working Memory Hardware (95% Maximum Capacity)")
        st.progress(85, text="🟢 Stress-Free Environment Engine (85% Power)")
        st.progress(25, text="⚪ Basic Emotional Processing (25% Background Power)")
        
    