import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
# Assuming MoodTracker is accessible, either imported or passed

def render_mood_heatmap(mood_data, mood_tracker_instance, st):
    """
    Generates and displays the 'Year in Pixels' mood heatmap in Streamlit.
    Dynamically generates the score map and colors from the MoodTracker instance.
    """
    if mood_data.empty or mood_data['date'].isnull().all():
        st.info("No mood entries found yet. Log your first feelings to see the heatmap!")
        return

    # 1. Prepare Data and Mood Score Mapping (DYNAMICALLY GENERATED)
    mood_data['date'] = pd.to_datetime(mood_data['date'])

    # --- DYNAMICALLY Generate Map and Legend from MoodTracker ---
    mood_to_score = {m.name: m.score for m in mood_tracker_instance.moods}
    score_to_name_color = {m.score: (m.name, m.color) for m in mood_tracker_instance.moods}

    # Ensure all scores from 1 to 5 are present
    valid_scores = sorted(score_to_name_color.keys())
    max_score = valid_scores[-1] if valid_scores else 0

    # Define a list of colors mapped to score index (0, 1, 2, 3, 4, 5)
    # The list index MUST match the score for the colormap.
    cmap_colors = ['#f0f0f0'] * (max_score + 1)  # Initialize with 'No Entry' color for all, max_score+1 size
    cmap_colors[0] = '#f0f0f0' # Explicitly set color for score 0 (No Entry)

    mood_legend_labels = {0: 'No Entry (0)'}

    # Fill the list and the legend map based on actual scores
    for score in score_to_name_color:
        name, color = score_to_name_color[score]
        if score <= max_score:
            cmap_colors[score] = color
            mood_legend_labels[score] = f'{name} ({score})'

    # Trim cmap_colors list to only include used indices
    cmap_colors = cmap_colors[:max_score + 1]

    # Apply the dynamic score map
    mood_data['mood_score'] = mood_data['category'].map(mood_to_score)
    # -------------------------------------------------------------------


    # Determine the year to visualize (using the year of the latest entry)
    current_year = mood_data['date'].max().year

    # Create a full date range for the selected year
    start_of_year = pd.to_datetime(f'{current_year}-01-01')
    end_of_year = pd.to_datetime(f'{current_year}-12-31')
    full_year_dates = pd.date_range(start=start_of_year, end=end_of_year, freq='D')

    # Create a DataFrame with all dates
    daily_mood = pd.DataFrame({'date': full_year_dates})

    # Merge with mood data
    merged_data = daily_mood.merge(
        mood_data[['date', 'mood_score']].drop_duplicates(subset=['date'], keep='last'),
        on='date',
        how='left'
    )

    # Fill days with no entry (NaN) with 0
    merged_data['mood_score'] = merged_data['mood_score'].fillna(0)
    merged_data.set_index('date', inplace=True)

    # 2. Reshape Data into Month vs. Day Matrix
    heatmap_df = merged_data.copy()
    heatmap_df['month'] = heatmap_df.index.month
    heatmap_df['day'] = heatmap_df.index.day

    # Pivot the table to get the desired format
    heatmap_data = heatmap_df.pivot_table(
        index='month',
        columns='day',
        values='mood_score'
    )

    # Reindex and Reverse the order of months (Dec at the top)
    heatmap_data = heatmap_data.reindex(index=np.arange(1, 13), columns=np.arange(1, 32))
    heatmap_data = heatmap_data.iloc[::-1]

    # 3. Create Heatmap Visualization with Seaborn/Matplotlib
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)

    # Use dynamically generated colors
    cmap = ListedColormap(cmap_colors)

    sns.heatmap(
        heatmap_data,
        ax=ax,
        cmap=cmap,
        vmin=0,
        vmax=max_score, # Use the dynamic max score
        linewidths=0.5,
        linecolor="white",
        cbar=False,
        square=True
    )

    # 4. Customizing Labels and Title
    ax.set_title(f"Year in Pixels - {current_year} Mood Tracker", fontsize=18, pad=18, weight='bold', color="#194E1D", fontname='DejaVu Sans', family='serif')
    ax.set_xlabel("Day Of Month")
    ax.set_ylabel("Month")

    # Month Labels (Y-axis) - Reversed to match data
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    reversed_month_names = month_names[::-1]

    ax.set_yticks(np.arange(0.5, 12.5))
    ax.set_yticklabels(reversed_month_names, rotation=0)

    # Day Labels (X-axis)
    ax.set_xticks(np.arange(0.5, 31.5))
    ax.set_xticklabels([day if day % 5 == 1 or day == 31 else '' for day in np.arange(1, 32)])
    ax.tick_params(axis='x', length=0)

    # 5. Custom Legend using Matplotlib Patches (FIXED INDEXING)
    # Sort the items back to display order (0, 1, 2, 3, 4, 5)
    sorted_legend_items = sorted(mood_legend_labels.items())

    legend_handles = []
    legend_labels = []

    for score, label in sorted_legend_items:
        # The color is now reliably indexed by the score itself
        color_index = score
        legend_handles.append(Patch(facecolor=cmap_colors[color_index], edgecolor='white', label=label))
        legend_labels.append(label)

    ax.legend(
        handles=legend_handles,
        labels=legend_labels,
        title="Mood Score",
        bbox_to_anchor=(1.01, 1),
        loc='upper left',
        frameon=False,
        fontsize='small',
        title_fontsize='medium'
    )

    # Use tight layout to make space for the legend
    plt.tight_layout(rect=[0, 0, 0.85, 1])

    # Render the plot in Streamlit
    st.pyplot(fig)

    # IMPORTANT: Close the plot to free memory
    plt.close(fig)
