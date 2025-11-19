import pandas as pd
from datetime import date
import streamlit as st
import numpy as np

# --- Import Tracker Classes and Heatmap Function ---
from models.mood_tracker import MoodTracker
from models.sleep_tracker import SleepTracker
from models.salah_tracker import SalahTracker
from Year_In_Pixels import render_mood_heatmap

# --- CONFIGURATION & INITIALIZATION ---

st.set_page_config(
    page_title="SoulState: Your Personal Wellness Hub",
    layout="wide"
)

# --- Data Loading Functions (Assumed to be defined and working) ---
@st.cache_resource
def initialize_trackers():
    """Initializes and caches all tracker objects."""
    return MoodTracker(), SleepTracker(), SalahTracker()

def safe_load_df(tracker, cols):
    entries = tracker.get_entries()
    df = pd.DataFrame(entries, columns=cols) if entries else pd.DataFrame(columns=cols)
    if not df.empty and 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

def load_all_data():
    mood_tracker, sleep_tracker, salah_tracker = initialize_trackers()
    mood_cols = ['date', 'category', 'note', 'mood_score']
    sleep_cols = ['date', 'sleep hours', 'note']
    salah_cols = ['date', 'fajr', 'dhuhr', 'asr', 'maghrib', 'isha', 'notes']
    st.session_state['mood_data'] = safe_load_df(mood_tracker, mood_cols)
    st.session_state['sleep_data'] = safe_load_df(sleep_tracker, sleep_cols)
    st.session_state['salah_data'] = safe_load_df(salah_tracker, salah_cols)

if 'mood_data' not in st.session_state:
    load_all_data()

mood_tracker, sleep_tracker, salah_tracker = initialize_trackers()
mood_data = st.session_state['mood_data']
sleep_data = st.session_state['sleep_data']
salah_data = st.session_state['salah_data']

# --- SIDEBAR (Friendly Guide) ---

with st.sidebar:
    st.title("🌱 SoulState: Your Hub")
    st.markdown("### Get Started!")
    st.caption(f"Hello! Today is **{date.today().strftime('%A, %b %d, %Y')}**")
    st.divider()
    pinterest_image_url = "https://i.pinimg.com/736x/b0/67/83/b0678354eadc2dac54a2a952b1ef9915.jpg"
    st.header("Inspiration for Today")
    st.image(
    pinterest_image_url,
    caption="***Only compare yourself to who you were yesterday.***",
    width=200 # Adjust width as needed
    )
    st.markdown("---")
    st.markdown("💡 *Small steps lead to big change!*")


# ==============================================================================
# 1. PRIMARY SECTION: LOGGING & CONTEXTUAL ANALYSIS
# ==============================================================================

st.header("Your Daily Flow Check-in 🧘‍♀️")
st.markdown("##### Log your entry and instantly review the related data trend within each tab.")
st.divider()

# Using horizontal tabs for logging AND review
tab_mood, tab_sleep, tab_salah = st.tabs(["🌈 Mood & Thoughts", "🌙 Rest & Recharge", "🕌 Inner Connection"])

# ------------------------------------------------------------------------------
# TAB 1: MOOD (Log + Heatmap)
# ------------------------------------------------------------------------------
with tab_mood:
    col_log, col_visual = st.columns([1,2])

    with col_log:
        with st.container(border=True):
            st.subheader("How's the vibe today?")
            mood_names = [m[0] for m in mood_tracker.get_available_moods()]
            selected_mood = st.selectbox("Pick the feeling that fits best:", mood_names, key="flow_mood")

            note = st.text_area("Journal it out: What's one positive thought or goal for today?", key="flow_note", height=150)

            if st.button("Save My Mood Check-in", type="primary",use_container_width=True):
                mood_tracker.add_entry(selected_mood, note)
                load_all_data()
                st.success("Mood saved! Check your Year in Pixels on the right.")

    with col_visual:
        st.subheader("Your Annual Mood Calendar (Year in Pixels)")
        st.markdown("_This visualization changes instantly as you log your day!_")
        if not mood_data.empty:
            # 🟢 HEATMAP INTEGRATION (Contextual placement)
            render_mood_heatmap(mood_data, mood_tracker, st)

            st.markdown("---")
            # Secondary analysis: Mood Distribution
            st.markdown("##### Mood Distribution:")
            st.bar_chart(mood_data['category'].value_counts())
        else:
            st.info("Log a few days to see your unique visual calendar here.")

    st.markdown("---")
    # Editing is placed at the bottom of its relevant tab
    st.subheader("Full Journal Review & Edit")
    if not mood_data.empty:
        editable_df = st.data_editor(
            mood_data[['date', 'category', 'note']].sort_values('date', ascending=False),
          use_container_width=True,
            num_rows="dynamic",
            hide_index=True
        )
        if st.button("Save Journal Edits", type="primary"):
            editable_df.to_csv(mood_tracker.filename, index=False)
            mood_tracker.__init__()
            load_all_data()
            st.success("Updates saved successfully!")
    else:
        st.info("Nothing to review yet. Start journaling!")

# ------------------------------------------------------------------------------
# TAB 2: SLEEP (Log + Trend Chart)
# ------------------------------------------------------------------------------
with tab_sleep:
    col_log, col_visual = st.columns([1, 2])

    with col_log:
        with st.container(border=True):
            st.subheader("How well did you recharge?")
            sleep_hours = st.number_input("Hours slept last night (Aim for 7-9!):", min_value=0.0, max_value=24.0, value=8.0, step=0.25, key="flow_sleep")
            note= st.text_area("Any thoughts on your rest? (e.g., dreams, interruptions)", key="flow_sleep_note", height=150)


            if st.button("Log My Sleep Hours", type="primary",use_container_width=True):
                sleep_tracker.add_entry(sleep_hours, note)
                load_all_data()
                st.success("Sleep logged! See your trend update on the right.")

    with col_visual:
        st.subheader("😴 Sleep Trend Over Time")
        if not sleep_data.empty and 'sleep hours' in sleep_data.columns:
            st.metric("Overall Average Sleep Time", f"{sleep_data['sleep hours'].astype(float).mean():.1f} hours")
            st.line_chart(sleep_data.set_index('date')['sleep hours'].astype(float))

            st.markdown("---")
            st.markdown("##### Latest Sleep Records:")
            st.dataframe(sleep_data[['date', 'sleep hours', 'note']].sort_values('date', ascending=False).head(10),use_container_width=True, hide_index=True)
        else:
            st.info("Keep logging your rest to build your trend data!")

# ------------------------------------------------------------------------------
# TAB 3: SALAH (Log + Consistency Chart)
# ------------------------------------------------------------------------------
with tab_salah:
    col_log, col_visual = st.columns([1, 2])

    with col_log:
        with st.container(border=True):
            st.subheader("How was your spiritual rhythm?")
            st.markdown("_Click the box for each prayer completed today._")

            cols = st.columns(5)
            fajr = cols[0].checkbox("Fajr", key="flow_fajr")
            dhuhr = cols[1].checkbox("Dhuhr", key="flow_dhuhr")
            asr = cols[2].checkbox("Asr", key="flow_asr")
            maghrib = cols[3].checkbox("Maghrib", key="flow_maghrib")
            isha = cols[4].checkbox("Isha", key="flow_isha")

            notes = st.text_area("Any reflections or notes for today?", key="flow_salah_notes", height=150)

            if st.button("Finish Daily Prayer Log", type="primary",use_container_width=True):
                salah_tracker.add_entry(int(fajr), int(dhuhr), int(asr), int(maghrib), int(isha), str(notes))
                load_all_data()
                st.success("Prayers saved! Check your consistency trend on the right.")

    with col_visual:
        st.subheader("🕌 Consistency Over Time")
        if not salah_data.empty:
            salah_data['completed'] = salah_data[['fajr', 'dhuhr', 'asr', 'maghrib', 'isha']].astype(int).sum(axis=1)
            salah_data['completion_rate'] = salah_data['completed'] / 5 * 100

            st.metric("Overall Success Rate", f"{salah_data['completion_rate'].mean():.1f}%")
            st.line_chart(salah_data.set_index('date')['completion_rate'])

            st.markdown("---")
            st.markdown("##### Latest Prayer Records:")
            st.dataframe(salah_data[['date', 'completed', 'notes']].sort_values('date', ascending=False).head(10),use_container_width=True, hide_index=True)
        else:
            st.info("Log prayer entries to see your consistency trend here.")
