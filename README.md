**SOUL STATE: PERSONAL WELLNESS HUB**

**SoulState** is a Python & Streamlit application designed to help users track and improve their **mental, physical, and spiritual well-being**. Log your daily moods, sleep patterns, and prayer habits while getting visual insights into your wellness journey.

**Features**

* **Mood Tracker** 🌈 – Log daily moods, journal thoughts, and view your "Year in Pixels" heatmap.
* **Sleep Tracker** 💤 – Track hours slept and rest quality with trends over time.
* **Salah / Spiritual Tracker** 🕌 – Record prayers and visualize consistency with completion metrics.
* **Journal & Edit** – Edit past entries through an interactive data editor.
* **Sidebar Motivation** – Displays daily quotes, images, and optional videos.
* **Data Persistence** – All trackers save to CSV for continuity.
* **Abstract Tracker Design** – Uses an abstract base class (`Tracker`) for modularity and scalability.

**DEMO**
https://github.com/rafiahashmi/Soul-State-Python/issues/1#issue-3652250668

**INSTALLATION**

1. Clone the repository:

-bash
git clone https://github.com/yourusername/SoulState.git
cd SoulState
```

2. (Optional) Create a virtual environment:

-bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:

-bash
pip install -r requirements.txt
```

4. Run the app:
-bash
streamlit run SoulState.py
```




**USAGE**
1. Open the app in your browser.
2. Navigate through **tabs**: Mood, Sleep, or Salah.
3. Log daily entries and notes.
4. Review visual trends: heatmaps, line charts, and metrics.
5. Edit past entries in the **Full Journal Review** section.

**TRACKER CLASSES**

* **Tracker** (Abstract Base Class) – Defines common interface: `add_entry`, `get_entries`, `load_data`, `save_data`.
* **MoodTracker** – Handles mood logging and mood types.
* **SleepTracker** – Handles sleep logging and trends.
* **SalahTracker** – Handles prayer tracking and completion metrics.



**FUTURE ENHANCEMENTS**

* Add **customizable habits tracker** for daily routines.
* Integrate **reminders/notifications** for consistency.
* Weekly/monthly analytics reports for insights.
* Multi-user support with authentication.


**CONTRIBUTING**

1. Fork the repository
2. Create a branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m "Add feature"`
4. Push: `git push origin feature-name`
5. Open a Pull Request

**LICENSE**

This project is licensed under the MIT License.
