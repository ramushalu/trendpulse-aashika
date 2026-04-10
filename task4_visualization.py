import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------------- STEP 1: LOAD DATA ----------------

file_path = "data/trends_analysed.csv"
df = pd.read_csv(file_path)

# Create outputs folder if not exists
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# ---------------- CHART 1: TOP 10 STORIES ----------------

# Get top 10 by score
top10 = df.sort_values(by="score", ascending=False).head(10)

# Shorten long titles (max 50 chars)
top10["short_title"] = top10["title"].apply(lambda x: x[:50] + "..." if len(x) > 50 else x)

plt.figure()
plt.barh(top10["short_title"], top10["score"])
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()  # highest on top

plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")
plt.show()

# ---------------- CHART 2: STORIES PER CATEGORY ----------------

category_counts = df["category"].value_counts()

plt.figure()
plt.bar(category_counts.index, category_counts.values,
        color=["red", "blue", "green", "purple", "orange"])  # different colors

plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.show()

# ---------------- CHART 3: SCATTER PLOT ----------------

# Separate popular and non-popular
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure()
plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()

plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.show()

# ---------------- BONUS: DASHBOARD ----------------

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Chart 1 in dashboard
axes[0].barh(top10["short_title"], top10["score"])
axes[0].set_title("Top Stories")
axes[0].invert_yaxis()

# Chart 2 in dashboard
axes[1].bar(category_counts.index, category_counts.values)
axes[1].set_title("Category Count")

# Chart 3 in dashboard
axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axes[2].set_title("Score vs Comments")
axes[2].legend()

fig.suptitle("TrendPulse Dashboard")

plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.show()
 
print("All charts saved in 'outputs/' folder") 

output
outputs/
├── chart1_top_stories.png
├── chart2_categories.png
├── chart3_scatter.png
└── dashboard.png

