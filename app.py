import streamlit as st
import numpy as np
from tensorflow import keras
import time

# ——— Load Model ———
model = keras.models.load_model("vision_correction_model.keras")

# ——— Manual Encoders ———
gender_map = {"Female": 0, "Male": 1}
occupation_map = {
    'Business': 0,
    'Employed': 1,
    'House Maker': 2,
    'Student': 3,
    'Unemployed / Seeking Employment': 4
}
education_map = {
    "Bachelor's Degree": 0,
    "Diploma / Vocational Training": 1,
    "Doctoral Degree": 2,
    "Higher Secondary": 3,
    "Higher Secondary (11th - 12th Grade)": 4,
    "Master's Degree": 5,
    "No Formal Education": 6,
    "SYLLB": 7,
    "Undergraduate": 8
}
outdoor_activity_map = {'No': 0, 'Yes': 1}
eyestrain_map = {
    "2-3 times a week": 0,
    "4-5 times a week": 1,
    "Every day": 2,
    "I do not exercise at all": 3,
    "I prefer other forms of physical activity (e.g., walking, yoga, etc.)": 4,
    "Once a week or less": 5
}
lighting_map = {
    'Bright, natural light': 0,
    'Dim lighting': 1,
    'I use a combination of natural and artificial lighting': 2,
    'Moderate lighting': 3,
    'Poor lighting': 4,
    'Well-lit with artificial light': 5
}

# ——— Normalization Ranges ———
norm_bounds = {
    'age': (17.0, 45.0),
    'screen_hours': (1.0, 18.0),
    'sleep_hours': (4.0, 11.0),
    'reading_hours': (0.0, 9.0),
    'dark_usage': (1.0, 24.0),
    'sunlight_hours': (0.0, 24.0),
    'device_before_bedtime': (0.0, 120.0)
}

def normalize(val, min_val, max_val):
    return (val - min_val) / (max_val - min_val)

def determine_vision_category(p):
    if p < .2:
        return "✅ Low risk — great habits! 😎"
    if p < .5:
        return "🟡 Moderate risk — a few tweaks could help."
    if p < .8:
        return "🟠 Elevated risk — consider more breaks and adjustments."
    return "🔴 High risk — it's advisable to consult an eye care specialist."

# ——— Chat-style Questions ———
questions = [
    ("age", "How old are you?", "number"),
    ("sleep_hours", "How many hours of sleep do you typically get per night?", "number"),
    ("screen_hours", "On average, how many hours per day do you spend using screens (including phone, computer, TV)?", "number"),
    ("reading_hours", "How many hours per day do you spend reading (printed or digital)?", "number"),
    ("dark_usage", "How many hours per day do you usually use dark theme on your devices and applications?", "number"),
    ("sunlight_hours", "How many hours per week do you go outside?", "number"),
    ("occupation", "What is your current occupation?", list(occupation_map.keys())),
    ("education", "What is your highest level of education?", list(education_map.keys())),
    ("outdoor_activity", "Do you engage in outdoor activities regularly?", list(outdoor_activity_map.keys())),
    ("exercise_frequency", "Do you regularly practice any eye strain reduction techniques (e.g., the 20-20-20 rule)?", list(eyestrain_map.keys())),
    ("lighting_conditions", "Please describe your usual lighting conditions when working or using screens:", list(lighting_map.keys()))
]

# ——— Streamlit App Layout ———
def cool_title(title_text):
    st.markdown(
        f"""
        <div style="background-color:#f63366;padding:10px;border-radius:10px;font-family: 'Times New Roman', Times, serif;">
        <h1 style="color:white;text-align:center;">{title_text}</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.set_page_config(page_title="VisionPredictor", layout="centered")
cool_title("ClarityCare")
st.markdown("Welcome! Let's chat about your vision health to assess potential risks.")

# ——— Initialize Session State ———
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = {}
    st.session_state.chat_history = []

# ——— Display Chat History ———
for msg in st.session_state.chat_history:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

# ——— Chat Interaction ———
if st.session_state.step < len(questions):
    key, prompt, opts = questions[st.session_state.step]

    if not st.session_state.chat_history or st.session_state.chat_history[-1]['role'] != 'assistant':
        st.session_state.chat_history.append({"role": "assistant", "content": prompt})
        st.rerun()

    if opts == "number":
        user_input = st.chat_input("Type your answer here...")
        if user_input:
            try:
                val = float(user_input)
                st.session_state.answers[key] = val
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                st.session_state.step += 1
                st.rerun()
            except ValueError:
                st.chat_message("assistant").markdown("⚠️ Please enter a valid number.")
    else:
        for option in opts:
            if st.button(option, key=f"btn_{key}_{option}"):
                st.session_state.answers[key] = option
                st.session_state.chat_history.append({"role": "user", "content": option})
                st.session_state.step += 1
                st.rerun()
else:
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown("Thank you for your responses! Please wait while I analyze the information...")
        with st.spinner("Analyzing..."):
            time.sleep(2)

        feature_order = [
            'age', 'screen_hours', 'sleep_hours', 'reading_hours', 'dark_usage','sunlight_hours',
            'occupation','education','outdoor_activity','lighting_conditions','exercise_frequency'
        ]

        feature_vals = []
        for key in feature_order:
            val = st.session_state.answers[key]
            if key in norm_bounds:
                mn, mx = norm_bounds[key]
                feature_vals.append(normalize(val, mn, mx))
            elif key == 'occupation':
                feature_vals.append(occupation_map[val])
            elif key == 'education':
                feature_vals.append(education_map[val])
            elif key == 'outdoor_activity':
                feature_vals.append(outdoor_activity_map[val])
            elif key == 'lighting_conditions':
                feature_vals.append(lighting_map[val])
            elif key == 'exercise_frequency':
                feature_vals.append(eyestrain_map[val])

        features = np.array(feature_vals).reshape(1, -1)
        prob = float(model.predict(features)[0][0])
        category = determine_vision_category(prob)

        st.success(f"**Assessment Result:** {category}")
        st.info(f"**Confidence Level:** {prob:.2%}")
        st.markdown("---")
        st.markdown("Please note: This assessment is based on the information you provided and prior knowledge used to train the system. It is not a substitute for professional medical advice. If you have concerns about your vision, consult with an eye care specialist.")

        if st.button("Start Over"):
            st.session_state.step = 0
            st.session_state.answers = {}
            st.session_state.chat_history = []
            st.rerun()
