import pandas as pd
from collections import Counter

def generate_multilabel_distribution():

    df = pd.read_csv("../../experiment/dataset_llm_classified.csv")

    def count_tags(tag_str):
        if pd.isna(tag_str) or tag_str.strip() == "":
            return 0
        return len([tag.strip() for tag in tag_str.split(",")])

    df['num_tags'] = df['llm_topic'].apply(count_tags)

    tag_count_distribution = Counter(df['num_tags'])

    distribution_df = pd.DataFrame(
        [(num_tags, count, count / len(df) * 100)
         for num_tags, count in sorted(tag_count_distribution.items())],
        columns=["Number_of_Tags", "Count", "Percentage"]
    )

    return df, distribution_df