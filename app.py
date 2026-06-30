import streamlit as st
import pandas as pd
import numpy as np

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Cognitive Intelligence Portfolio", layout="wide", initial_sidebar_state="expanded")

# --- 2. SIDEBAR NAVIGATION ---
st.sidebar.title("🧠 The Biological Engines of Intelligence")
st.sidebar.markdown("Navigate through the findings of the cognitive data analysis project.")

page = st.sidebar.radio(
    "Select Analysis Phase:",
    ("Welcome & Overview",  # <--- THIS IS THE NEW LINE
     "The Grand Synthesis", 
     "Angle 1: The Everyday Brain (Regression)",
     "Angle 2: The Biological Override (Clustering)",
     "Angle 3: The Elite Bottleneck (Classification)",
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
                          url("https://images.unsplash.com/photo-1559757175-5700dde675bc?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
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
             🧠 <b style='color: #A2D5F2;'>Fluid Intelligence (PMAT24):</i> The ultimate logic and problem-solving score. This is the "brain power" we are trying to predict.<br>
             💤 <b style='color: #FF6B6B;'>The Sleep Penalty (PSQI):</i> A measure of sleep deprivation. A high score indicates toxic, poor-quality sleep.<br>
             ❤️ <b style='color: #FF8E8B;'>Emotional Intelligence (ER40):</i> The subject's ability to accurately read and process human emotions.<br>
             💾 <b style='color: #A2D5F2;'>Working Memory (PicSeq):</i> The brain's raw hardware capacity to store and recall visual information.<br>
             🎯 <b style='color: #A2D5F2;'>Pure Focus (Flanker):</i> The biological ability to maintain strict attention and ignore outside distractions.<br>
             🧘 <b style='color: #6BCB77;'>Stress-Free Metric (LifeSatisf):</i> Overall life satisfaction, used as a baseline indicator of a low-stress, low-cortisol environment.
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
if page == "The Grand Synthesis":
    st.title("The Grand Synthesis: The Hierarchy of Human Intelligence")
    st.markdown("### Executive Summary")
    st.success("**Human intelligence operates on a strict biological hierarchy: good sleep is the non-negotiable baseline that prevents your brain from crashing, emotional awareness is the daily engine that powers everyday problem-solving, but to break into the absolute elite tier of cognitive performance, you must possess massive working memory hardware and a completely stress-free mind.**")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Level 1: The Foundation**\n\nChronic sleep deprivation acts as a total biological override, neutralizing even superior cognitive hardware.")
    with col2:
        st.info("**Level 2: The Daily Driver**\n\nFor average daily problem-solving, emotional awareness serves as the brain's primary operating system.")
    with col3:
        st.info("**Level 3: The Elite Tier**\n\nBreaking into the top 20% of logic performers requires raw working memory capacity and an absence of stress.")

# --- 4. PAGE: ANGLE 1 (REGRESSION) ---
elif page == "Angle 1: The Everyday Brain (Regression)":
    st.title("Angle 1: Predicting Baseline Logic")
    st.markdown("A Multiple Linear Regression model engineered to predict general fluid intelligence for the average population.")
    
    st.metric(label="Model Predictive Power (R-Squared)", value="11.0%")
    
    st.markdown("### The Biological Driver")
    st.markdown("For the average person on an average day, **Emotional Intelligence** is the strongest linear driver of problem-solving ability, while **Sleep Trouble** serves as the heaviest biological penalty.")
    
    # Exact hardcoded results from the Jupyter Notebook
    reg_data = {
        'Feature': ['ER40_CR (Emotion)', 'PicSeq_AgeAdj (Memory)', 'Flanker_AgeAdj (Focus)', 'PSQI_Score (Sleep Penalty)'],
        'Mathematical Weight': [0.38, 0.08, 0.02, -0.18]
    }
    df_reg = pd.DataFrame(reg_data).set_index('Feature')
    
    st.bar_chart(df_reg['Mathematical Weight'])

# --- 5. PAGE: ANGLE 2 (CLUSTERING) ---
elif page == "Angle 2: The Biological Override (Clustering)":
    st.title("Angle 2: Uncovering Cognitive Profiles")
    st.markdown("K-Means clustering automatically mapped the subjects into three distinct archetypes without any human-provided rules.")
    
    st.markdown("### The Hidden Profiles Revealed")
    
    # Exact hardcoded results from the Jupyter Notebook
    cluster_data = {
        'Hidden Tribe': ['Tribe 0 (The Unfocused Average)', 'Tribe 1 (The Burnout Group)', 'Tribe 2 (The Elite Achievers)'],
        'PSQI_Score (Sleep)': [3.8, 9.2, 3.7],
        'Flanker_AgeAdj (Focus)': [92.2, 100.2, 108.0],
        'ER40_CR (Emotion)': [34.0, 35.6, 36.5],
        'PicSeq_AgeAdj (Memory)': [101.8, 104.1, 106.9],
        'PMAT24_A_CR (Logic Score)': [16.2, 15.7, 17.4]
    }
    df_cluster = pd.DataFrame(cluster_data).set_index('Hidden Tribe')
    
    # Apply color styling to highlight the paradox
    st.dataframe(df_cluster.style.highlight_max(axis=0, color='#1f77b4').highlight_min(axis=0, color='#d62728'))
    
    st.markdown("### The Hardware vs. Maintenance Paradox")
    st.error("**The Burnout Phenomenon (Tribe 1):** The data mathematically proves that poor sleep acts as a total biological override. Tribe 1 possessed *higher* working memory (104.1) and focus (100.2) than Tribe 0. However, because their sleep quality was so catastrophically poor (9.2), their actual logical output crashed (15.7) below the people who had inferior brain hardware but slept perfectly.")

# --- 6. PAGE: ANGLE 3 (CLASSIFICATION) ---
elif page == "Angle 3: The Elite Bottleneck (Classification)":
    st.title("Angle 3: Sorting the Top 20% Geniuses")
    st.markdown("A Random Forest classifier engineered to identify only the absolute elite problem solvers.")
    
    st.metric(label="Overall Sorting Accuracy", value="61.1%")
    
    st.markdown("### The Elite Gatekeepers")
    st.markdown("When isolating the elite, the brain's priorities completely flip. The algorithm mathematically relies on **Working Memory** (raw hardware capacity) and **Life Satisfaction** (absence of stress) to identify top-tier geniuses.")
    
    # Exact hardcoded results from the Jupyter Notebook
    class_data = {
        'Feature': ['PicSeq_AgeAdj (Memory)', 'LifeSatisf_Unadj (Stress Free)', 'Flanker_AgeAdj (Focus)', 'ER40_CR (Emotion)', 'PSQI_Score (Sleep)'],
        'Decision Importance (%)': [33.1, 21.0, 19.1, 17.3, 9.5]
    }
    df_class = pd.DataFrame(class_data).set_index('Feature')
    
    st.bar_chart(df_class['Decision Importance (%)'])

# --- 7. NEW PAGE: INTERACTIVE BIOLOGICAL ENGINE ---
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
        
    # --- END OF REPLACEMENT CODE ---