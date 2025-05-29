import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from PIL import Image

# Define path to the file
data_path = r"whatsapp_misinfo\india\misinfo_anonymized.txt"

# Choose columns and set chunk size
columns_to_read = ['group_id', 'user_id', 'image_id', 'cluster_image_name', 'timestamp']
chunk_size = 5000

# Create an empty list to store partial DataFrames
chunks = []

print("✅ Reading file in chunks...")

# Read in chunks and only specific columns
for chunk in pd.read_csv(data_path, sep="\t", usecols=columns_to_read, chunksize=chunk_size):
    chunks.append(chunk)

# Combine all chunks into a full DataFrame
df = pd.concat(chunks, ignore_index=True)

# ✅ Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

# ✅ Print confirmation
print("✅ Loaded DataFrame shape:", df.shape)
print(df.head())

# OPTIONAL: Save filtered version
df.to_csv("misinfo_clean.csv", index=False)
print("💾 Saved cleaned data to misinfo_clean.csv")

# Create necessary directories
os.makedirs("analysis_outputs", exist_ok=True)
os.makedirs("plots", exist_ok=True)

# --- User & Group Engagement ---
top_users = df['user_id'].value_counts().head(10).reset_index()
top_users.columns = ['user_id', 'post_count']
top_users.to_csv("analysis_outputs/top_users.csv", index=False)

top_groups = df['group_id'].value_counts().head(10).reset_index()
top_groups.columns = ['group_id', 'message_count']
top_groups.to_csv("analysis_outputs/top_groups.csv", index=False)

# --- Temporal Activity ---
df['hour'] = df['timestamp'].dt.hour
df['weekday'] = df['timestamp'].dt.day_name()

# Daily activity
daily_activity = df['timestamp'].dt.date.value_counts().sort_index()
daily_activity.to_csv("analysis_outputs/daily_activity.csv")

# Hourly activity
hourly = df['hour'].value_counts().sort_index()
hourly.to_csv("analysis_outputs/hourly_activity.csv")

# Plot hourly activity
plt.figure(figsize=(10, 4))
hourly.plot(kind='line', title='Hourly Posting Activity')
plt.xlabel("Hour of Day")
plt.ylabel("Number of Posts")
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/hourly_activity.png")

# Heatmap: Hour vs Weekday
heatmap_data = df.groupby(['weekday', 'hour']).size().unstack(fill_value=0)
heatmap_data = heatmap_data.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.figure(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap="YlGnBu")
plt.title("WhatsApp Misinformation Heatmap (Weekday vs Hour)")
plt.tight_layout()
plt.savefig("plots/heatmap_weekday_hour.png")

# --- Most Shared Images ---
top_images = df['cluster_image_name'].value_counts().head(20).reset_index()
top_images.columns = ['image_name', 'share_count']
top_images.to_csv("analysis_outputs/top_20_images.csv", index=False)

# --- Image Spread Trend ---
top5 = top_images['image_name'].head(5)
df_top5 = df[df['cluster_image_name'].isin(top5)]
df_top5.loc[:, 'date'] = df_top5['timestamp'].dt.date

spread_trend = df_top5.groupby(['date', 'cluster_image_name']).size().unstack(fill_value=0)
spread_trend.to_csv("analysis_outputs/top_5_image_spread_trend.csv")

# --- Image Preview Grid ---
print("🖼️ Generating top 20 misinformation image preview...")
img_folder = "top_images"
os.makedirs(img_folder, exist_ok=True)

# Load the images
image_names = top_images['image_name'].tolist()
img_list = []
for name in image_names:
    path = os.path.join(img_folder, name)
    if os.path.exists(path):
        img = Image.open(path).resize((200, 200))
        img_list.append(img)

# Create a grid of 5x4
cols = 5
rows = (len(img_list) + cols - 1) // cols
grid_w = cols * 200
grid_h = rows * 200
grid_img = Image.new('RGB', (grid_w, grid_h), color='white')

for i, img in enumerate(img_list):
    x = (i % cols) * 200
    y = (i // cols) * 200
    grid_img.paste(img, (x, y))

grid_img.save("plots/top_20_images_preview.png")

print("✅ Deep analysis complete. Results saved to 'analysis_outputs/' and 'plots/' folders.")


