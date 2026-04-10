 import requests
import json
import os
import time
from datetime import datetime

# Base URLs for HackerNews API
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header (as required)
headers = {"User-Agent": "TrendPulse/1.0"}

# Categories and keywords (case-insensitive matching)
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Function to determine category based on title
def get_category(title):
    title_lower = title.lower()
    for category, keywords in categories.items():
        for word in keywords:
            if word in title_lower:
                return category
    return None  # skip if no category matched


def main():
    print("Fetching top stories...")

    try:
        response = requests.get(TOP_STORIES_URL, headers=headers)
        story_ids = response.json()[:500]  # first 500 IDs
    except Exception as e:
        print("Error fetching top stories:", e)
        return

    collected_stories = []
    category_count = {cat: 0 for cat in categories}

    # Loop category-wise (important for sleep condition)
    for category in categories:
        print(f"\nCollecting {category} stories...")

        for story_id in story_ids:
            # Stop when 25 stories per category reached
            if category_count[category] >= 25:
                break

            try:
                story_res = requests.get(ITEM_URL.format(story_id), headers=headers)
                story = story_res.json()
            except Exception as e:
                print(f"Failed to fetch story {story_id}")
                continue

            # Skip invalid stories
            if not story or "title" not in story:
                continue

            title = story.get("title", "")
            assigned_category = get_category(title)

            # Only collect if it matches current category
            if assigned_category == category:
                data = {
                    "post_id": story.get("id"),
                    "title": title,
                    "category": assigned_category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", "unknown"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                collected_stories.append(data)
                category_count[category] += 1

        # Sleep after each category loop
        time.sleep(2)

    # Create data folder if not exists
    if not os.path.exists("data"):
        os.makedirs("data")

    # Create filename with date
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    # Save JSON file
    with open(filename, "w") as f:
        json.dump(collected_stories, f, indent=4)

    print(f"\nCollected {len(collected_stories)} stories.")
    print(f"Saved to {filename}")


if __name__ == "__main__":
    main()


output


Fetching top stories...

Collecting technology stories...

Collecting worldnews stories...

Collecting sports stories...

Collecting science stories...

Collecting entertainment stories...

Collected 88 stories.
Saved to data/trends_20260410.json


import json
import pandas as pd
import os

# Find latest JSON file in data folder
data_folder = "data"
files = [f for f in os.listdir(data_folder) if f.endswith(".json")]

# Sort files to get latest
files.sort(reverse=True)
latest_file = os.path.join(data_folder, files[0])

print("Loading file:", latest_file)

# Load JSON
with open(latest_file, "r") as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data)

# ---------------- CLEANING ----------------

# Remove duplicates based on post_id
df = df.drop_duplicates(subset="post_id")

# Handle missing values
df["author"] = df["author"].fillna("unknown")
df["num_comments"] = df["num_comments"].fillna(0)
df["score"] = df["score"].fillna(0)

# Convert data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Convert collected_at to datetime
df["collected_at"] = pd.to_datetime(df["collected_at"])

# ---------------- SAVE CSV ----------------

output_file = latest_file.replace(".json", ".csv")
df.to_csv(output_file, index=False)

print(f"Cleaned data saved to {output_file}")
print(f"Total records: {len(df)}")



output

Loading file: data/trends_20260410.json
Cleaned data saved to data/trends_20260410.csv
Total records: 88

import pandas as pd
import numpy as np
import os

# Load latest CSV
data_folder = "data"
files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]
files.sort(reverse=True)
latest_file = os.path.join(data_folder, files[0])

print("Analyzing file:", latest_file)

df = pd.read_csv(latest_file)

# ---------------- ANALYSIS ----------------

# 1. Average score per category
avg_score = df.groupby("category")["score"].mean()

# 2. Total comments per category
total_comments = df.groupby("category")["num_comments"].sum()

# 3. Top 5 posts by score
top_posts = df.sort_values(by="score", ascending=False).head(5)

# 4. Category with highest average score
best_category = avg_score.idxmax()

# ---------------- PRINT RESULTS ----------------

print("\nAverage Score per Category:")
print(avg_score)

print("\nTotal Comments per Category:")
print(total_comments)

print("\nTop 5 Posts:")
print(top_posts[["title", "category", "score"]])

print(f"\nBest Performing Category: {best_category}")

output

Analyzing file: data/trends_20260410.csv

Average Score per Category:
category
entertainment    141.080000
science          189.200000
sports           114.454545
technology       311.120000
worldnews        135.363636
Name: score, dtype: float64

Total Comments per Category:
category
entertainment    1392
science           365
sports            468
technology       3879
worldnews        1654
Name: num_comments, dtype: int64

Top 5 Posts:
                                                title       category  score
13         Git commands I run before reading any code     technology   2253
23  Project Glasswing: Securing critical software ...     technology   1520
76    Show HN: Brutalist Concrete Laptop Stand (2024)  entertainment    782
25  France Launches Government Linux Desktop Plan ...      worldnews    663
29                GLM-5.1: Towards Long-Horizon Tasks      worldnews    616

Best Performing Category: technology

import pandas as pd
import matplotlib.pyplot as plt
import os

# Load latest CSV
data_folder = "data"
files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]
files.sort(reverse=True)
latest_file = os.path.join(data_folder, files[0])

print("Visualizing file:", latest_file)

df = pd.read_csv(latest_file)

# ---------------- VISUALS ----------------

# 1. Bar chart - Average Score per Category
avg_score = df.groupby("category")["score"].mean()

plt.figure()
avg_score.plot(kind="bar")
plt.title("Average Score per Category")
plt.xlabel("Category")
plt.ylabel("Average Score")
plt.tight_layout()
plt.show()

# 2. Bar chart - Total Comments
total_comments = df.groupby("category")["num_comments"].sum()

plt.figure()
total_comments.plot(kind="bar")
plt.title("Total Comments per Category")
plt.xlabel("Category")
plt.ylabel("Comments")
plt.tight_layout()
plt.show()

# 3. Histogram - Score Distribution
plt.figure()
df["score"].plot(kind="hist", bins=20)
plt.title("Score Distribution")
plt.xlabel("Score")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

output

Visualizing file: data/trends_20260410.csv


