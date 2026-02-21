import pandas as pd
from collections import Counter

df = pd.read_csv("dataset_llm_classified.csv")

# extrai tags
def extract_tags(tag_str):
    if pd.isna(tag_str) or tag_str.strip() == "":
        return []
    return [tag.strip() for tag in tag_str.split(",")]

all_tags = []
for tags in df["llm_topic"].apply(extract_tags):
    all_tags.extend(tags)

# conta frequencias
tag_counts = Counter(all_tags)
total_adrs = len(df)

# cria df ordenado
topic_df = pd.DataFrame(
    [(tag, count, count / total_adrs * 100) for tag, count in tag_counts.items()],
    columns=["Topic", "Count", "Percentage"]
).sort_values(by="Count", ascending=False)

topic_df.to_csv("topic_frequency.csv", index=False)
print(topic_df.to_string(index=False))