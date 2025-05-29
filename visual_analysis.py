import pandas as pd
import matplotlib.pyplot as plt
import os

# Create a folder to store the plots
os.makedirs("plots", exist_ok=True)

# Load the cleaned dataset
df = pd.read_csv("misinfo_clean.csv", parse_dates=["timestamp"])

# ========== Plot 1: Hourly Posting Pattern ==========
df['hour'] = df['timestamp'].dt.hour
plt.figure(figsize=(10, 4))
df['hour'].value_counts().sort_index().plot(kind="line", title="Hourly Posting Activity")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Posts")
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/hourly_activity.png")
plt.show()

# ========== Plot 2: Weekly Posting Pattern ==========
df['weekday'] = df['timestamp'].dt.day_name()
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
plt.figure(figsize=(8, 5))
df['weekday'].value_counts().reindex(weekday_order).plot(kind="bar", color="green", title="Posts by Weekday")
plt.ylabel("Posts")
plt.tight_layout()
plt.savefig("plots/weekday_activity.png")
plt.show()

# ========== Plot 3: Most Repeated Misinformation Images ==========
plt.figure(figsize=(10, 6))
df['cluster_image_name'].value_counts().head(15).plot(kind="barh", title="Most Repeated Misinformation Images")
plt.xlabel("Occurrences")
plt.tight_layout()
plt.savefig("plots/top_misinfo_images.png")
plt.show()

# ========== Plot 4: User Post Distribution ==========
plt.figure(figsize=(10, 5))
df['user_id'].value_counts().hist(bins=50)
plt.title("Distribution of Post Counts per User")
plt.xlabel("Number of Posts")
plt.ylabel("User Count")
plt.tight_layout()
plt.savefig("plots/user_post_distribution.png")
plt.show()

print("✅ All plots saved in the 'plots' folder.")

import seaborn as sns

# Extract additional time info
df['month'] = df['timestamp'].dt.month
df['day'] = df['timestamp'].dt.day_name()

# Create pivot table (weekday vs. month)
pivot = df.pivot_table(index='day', columns='month', aggfunc='size', fill_value=0)

# Sort days to look better
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
pivot = pivot.reindex(day_order)

# Plot the heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(pivot, cmap="YlGnBu", annot=True, fmt="d")
plt.title("📊 Heatmap of Posts by Weekday and Month")
plt.xlabel("Month")
plt.ylabel("Weekday")
plt.tight_layout()
plt.savefig("plots/heatmap_weekday_month.png")
plt.show()

top_users = df['user_id'].value_counts().head(10)
plt.figure(figsize=(10, 5))
top_users.plot(kind="bar", color="orange")
plt.title("Top 10 Most Active Users")
plt.xlabel("User ID")
plt.ylabel("Number of Posts")
plt.tight_layout()
plt.savefig("plots/top_users.png")
plt.show()

