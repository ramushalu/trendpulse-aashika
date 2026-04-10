 import pandas as pd
import json
import os

# ---------------- STEP 1: LOAD JSON ----------------

data_folder = "data"

# Find JSON file (latest one)
json_files = [f for f in os.listdir(data_folder) if f.endswith(".json")]
json_files.sort(reverse=True)

file_path = os.path.join(data_folder, json_files[0])

# Load JSON into DataFrame
with open(file_path, "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

print(f"Loaded {len(df)} stories from {file_path}")

# ---------------- STEP 2: CLEAN DATA ----------------

# 1. Remove duplicates based on post_id
before = len(df)
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# 2. Remove rows with missing important fields
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# 3. Fix data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# 4. Remove low-quality stories (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# 5. Strip whitespace from title
df["title"] = df["title"].str.strip()

# ---------------- STEP 3: SAVE CSV ----------------

output_path = os.path.join(data_folder, "trends_clean.csv")

df.to_csv(output_path, index=False)

print(f"\nSaved {len(df)} rows to {output_path}")

# ---------------- SUMMARY ----------------

print("\nStories per category:")
print(df["category"].value_counts()) 

output

Loaded 122 stories from data/trends_20260410.json

After removing duplicates: 120
After removing nulls: 118
After removing low scores: 114

Saved 114 rows to data/trends_clean.csv

Stories per category:
technology        22
worldnews         24
sports            21
science           24
entertainment     23
