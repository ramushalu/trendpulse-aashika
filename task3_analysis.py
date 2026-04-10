import pandas as pd
import numpy as np
import os

# ---------------- STEP 1: LOAD DATA ----------------

file_path = "data/trends_clean.csv"

df = pd.read_csv(file_path)

print(f"Loaded data: {df.shape}")

# First 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Average score and comments
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {int(avg_score)}")
print(f"Average comments: {int(avg_comments)}")

# ---------------- STEP 2: NUMPY ANALYSIS ----------------

scores = df["score"].values
comments = df["num_comments"].values

print("\n--- NumPy Stats ---")

# Mean, median, std deviation
print(f"Mean score   : {int(np.mean(scores))}")
print(f"Median score : {int(np.median(scores))}")
print(f"Std deviation: {int(np.std(scores))}")

# Max and min
print(f"Max score    : {np.max(scores)}")
print(f"Min score    : {np.min(scores)}")

# Category with most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Story with most comments
max_comments_index = np.argmax(comments)
top_story = df.iloc[max_comments_index]

print("\nStory with most comments:")
print(f"Title: {top_story['title']}")
print(f"Comments: {top_story['num_comments']}")

# ---------------- STEP 3: ADD NEW COLUMNS ----------------

# Engagement = comments per upvote
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Popular if score > average score
df["is_popular"] = df["score"] > avg_score

# ---------------- STEP 4: SAVE RESULT ----------------

output_path = "data/trends_analysed.csv"
df.to_csv(output_path, index=False)

print(f"\nSaved analysed data to {output_path}")
