import pandas as pd
import json
import matplotlib.pyplot as plt
import os

here = os.path.dirname(__file__)
csv_path = os.path.join(here, "uc_n4.csv")
df = pd.read_csv(csv_path)


df["antichain"] = df["antichain_minimals"].apply(json.loads)
df["freqs_before"] = df["freqs_before"].apply(json.loads)
df["freqs_after"] = df["freqs_after"].apply(json.loads)

df_sorted = df.sort_values("min_freq_before")
df_sorted[["index", "family_size", "min_freq_before", "var_before"]].head(10)

plt.hist(df["min_freq_before"], bins=20)
plt.title("Distribution of minimum element frequency (n=4)")
plt.xlabel("min frequency")
plt.ylabel("count")
plt.show()

row = df_sorted.iloc[0]
print("Antichain minimal sets:", row["antichain"])
print("freqs before:", row["freqs_before"])
print("freqs after:", row["freqs_after"])
