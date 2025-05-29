from PIL import Image
import os
import glob
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set wide layout
st.set_page_config(layout="wide")

# Title and Introduction
st.title("📊 WhatsApp Misinformation Spread Analysis")
st.markdown("""
This dashboard presents an exploratory data analysis of image-based misinformation spread through WhatsApp groups in India.
The analysis includes post frequency trends, most shared images, user activity patterns, and heatmaps of messaging behavior.

**Contributors**: *Prof. Larsen Mandi*, **Harish Kummara**  
**Course**: *Digital Public Spheres*

This policy brief and dashboard are especially designed to support **NGOs and advocacy groups** working on the ground in India to combat misinformation.  
By offering clear visual insights into how visual content spreads on WhatsApp, it aims to help such organizations make informed decisions, plan interventions, and build public awareness.

These insights also support policy discussions aligned with the values of **truth**, **civility**, and the **common good** as emphasized in our course.
""")
st.markdown("---")


# Load Data
top_images_df = pd.read_csv("analysis_outputs/top_20_images.csv")
daily_activity_df = pd.read_csv("analysis_outputs/daily_activity.csv")
df_daily = daily_activity_df.rename(columns={daily_activity_df.columns[0]: "date", daily_activity_df.columns[1]: "count"})
df_daily['date'] = pd.to_datetime(df_daily['date'], errors='coerce')

# Sidebar - Top image selection
selected_image = st.sidebar.selectbox("🔍 Select Top Image", top_images_df["image_name"])

# Section 1: Summary Metrics
st.subheader("🧾 Key Insights Summary")
col1, col2, col3 = st.columns(3)
col1.metric("📅 Peak Posting Day", "Friday", "↗ High Activity")
col2.metric("⏰ Most Active Hour", "03:00 AM", "🔥")
col3.metric("🖼️ Top Shared Image", selected_image, "📈 Trending")

# Section 2: Daily Post Volume
st.subheader("📊 Daily Posting Activity")
fig, ax = plt.subplots()
ax.plot(df_daily['date'], df_daily['count'], marker='o')
ax.set_xlabel("Date")
ax.set_ylabel("Number of Posts")
ax.set_title("Daily Post Volume")
plt.xticks(rotation=45)
st.pyplot(fig)

# Section 3: Most Shared Misinformation Images
st.subheader("🖼️ Most Shared Misinformation Images (Top 20)")
img_dir = "top_images"
cols = st.columns(5)
for i, row in top_images_df.iterrows():
    image_name = row["image_name"]
    image_path = os.path.join(img_dir, image_name)
    if os.path.exists(image_path):
        with cols[i % 5]:
            st.image(image_path, caption=image_name, use_container_width=True)

# Section 4: Heatmap (Weekday vs Hour)
st.subheader("⏰ Posting Pattern Heatmap (Weekday vs Hour)")
main_heatmap = "plots/heatmap_weekday_hour.png"
if os.path.exists(main_heatmap):
    st.image(main_heatmap, caption="WhatsApp Misinformation Heatmap (Weekday vs Hour)", use_container_width=True)
else:
    st.warning("Main heatmap not found!")

# Section 5: Additional Heatmaps
st.markdown("---")
st.subheader("🌐 Explore Additional Posting Pattern Heatmaps")
extra_heatmaps_dir = "plots"
heatmap_files = sorted(glob.glob(f"{extra_heatmaps_dir}/*.png"))

# Filter out the main heatmap to avoid duplication
heatmap_files = [f for f in heatmap_files if not f.endswith("heatmap_weekday_hour.png")]

if heatmap_files:
    heatmap_names = [os.path.basename(f) for f in heatmap_files]
    selected_heatmap = st.selectbox("📌 Select a Heatmap to View", heatmap_names)
    heatmap_path = os.path.join(extra_heatmaps_dir, selected_heatmap)
    if os.path.exists(heatmap_path):
        st.image(heatmap_path, caption=f"Selected Heatmap - {selected_heatmap}", use_container_width=True)
    else:
        st.error("Selected heatmap file not found.")
else:
    st.warning("⚠️ No extra heatmaps found in the 'plots' folder. Please add .png files.")

# Footer
st.markdown("---")
st.markdown("📘 *This dashboard was built as part of a policy brief project in the Digital Public Spheres course.*")










