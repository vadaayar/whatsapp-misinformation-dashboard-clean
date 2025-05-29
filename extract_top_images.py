import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Paths
csv_path = "misinfo_clean.csv"
image_dir = os.path.join("whatsapp_misinfo", "india", "misinfo")  # Image folder from dataset
output_dir = "top_images"
output_grid_path = os.path.join("plots", "top_20_images_grid.png")

# Create folders if not exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs("plots", exist_ok=True)

# Load data
df = pd.read_csv(csv_path, parse_dates=["timestamp"])

# Get top 20 most repeated misinformation images
top_images = df["cluster_image_name"].value_counts().head(20).index.tolist()

# Save individual copies into 'top_images' folder
for img_name in top_images:
    src_path = os.path.join(image_dir, img_name)
    dst_path = os.path.join(output_dir, img_name)
    if os.path.exists(src_path):
        with open(src_path, "rb") as src_file, open(dst_path, "wb") as dst_file:
            dst_file.write(src_file.read())

# Plot grid of images
fig, axes = plt.subplots(4, 5, figsize=(15, 10))  # 4 rows x 5 cols = 20
axes = axes.flatten()

for i, img_name in enumerate(top_images):
    img_path = os.path.join(output_dir, img_name)
    if os.path.exists(img_path):
        img = mpimg.imread(img_path)
        axes[i].imshow(img)
        axes[i].set_title(img_name[:8], fontsize=8)
        axes[i].axis("off")

for j in range(len(top_images), len(axes)):
    axes[j].axis("off")  # Hide empty subplots if any

plt.tight_layout()
plt.savefig(output_grid_path)
plt.show()

print(f"✅ Extracted top 20 images and saved grid to {output_grid_path}")
