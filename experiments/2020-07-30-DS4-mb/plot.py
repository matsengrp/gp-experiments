#! /usr/bin/env python

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
sns.set_context("poster")

gp_df = pd.read_csv("_output/gp-sbn-parameters.csv", names=["gpcsp", "GP probability"])
sa_df = pd.read_csv("_output/sa-sbn-params.csv", names=["gpcsp", "SA probability"])
df = pd.merge(gp_df, sa_df)
# GP should have all of the SA GPCSPs, and also the fake ones.
assert len(df) == len(sa_df)
df.to_csv("_output/sbn-parameter-comparison.csv", index=False)

print(df.corr())

ax = sns.scatterplot(x="SA probability", y="GP probability", data=df, alpha=0.2)
ax.set_aspect(1)
sns.despine()
plt.savefig("ds4-comparison.svg", bbox_inches="tight")
