import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import scipy
import statannot


PATH_STAT = "results/check_stats"

#############
def stat_survey():
    """
    """

    ## CONFIG
    df = pd.read_csv(os.path.join(PATH_STAT, "survey_bci2.csv"))
    subject_group = {
        "G1": [10, 11, 12, 13], # image
        "G2": [25, 26, 27, 29], # arrow (split run)
        "G3": [15, 16, 18, 20], # arrow + feedback (split run)

        # "G1": [10, 11, 12, 13], # image
        # "G2+G3": [25, 26, 27, 29, 15, 16, 18, 20], # arrow (split run)
    }
    list_metric = df.columns[2:-1]

    ## process df
    df1 = pd.DataFrame()
    j = 0
    for group in subject_group.keys():
        for subject in subject_group[group]:
            for run in [1,2]:
                for metric in list_metric:
                    if metric == "Interest": 
                        continue

                    df1.loc[j, "group"] = group
                    df1.loc[j, "subject"] = subject
                    df1.loc[j, "run"] = run
                    df1.loc[j, "metric"] = metric

                    tmp = df.loc[df["ID"] == f"F{subject}"] \
                            .loc[df["Run"] == run]
                    df1.loc[j, "score"] = tmp[metric].values
                    j+=1
    print(df1)
    print(np.unique(df1["metric"]))

    # ## SCIPY.STATS
    # rng = np.random.default_rng()
    # for metric in d.keys():
    #     for p in box_pairs:
    #         a = d[metric][p[0]]
    #         b = d[metric][p[1]]
    #         # r = scipy.stats.ttest_ind(a, b,
    #         #     equal_var=False, permutations=1000, random_state=rng)
    #         r = scipy.stats.mannwhitneyu(a, b, method="exact")

    #         print(f"\n{metric}")
    #         print(f"{p}, result: {r}")

    # ======= PLOT SUBPLOT =========# 
    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(15,7))
    for i in range(3):
        for j in range(3):
            metric = list_metric[i*3+j]
            data = df1.loc[df1["metric"] == metric]
            ax = axes[i,j]
        
            sns.boxplot(
                data=data, 
                ax=ax, 
                x="group", y="score",
                width=0.4,
                showmeans=True,
                meanprops=dict(markerfacecolor='white',markeredgecolor='black', markersize=8),
                boxprops=dict(linestyle='-', linewidth=2),
                medianprops=dict(linestyle='-', linewidth=2),
                whiskerprops=dict(linestyle='--', linewidth=2),
                capprops=dict(linestyle='-', linewidth=2),
        
            )
            ax.set_ylim((0,5))
            ax.set_ylabel("")
            ax.set_xlabel("")
            ax.set_title(metric, fontsize=15, fontweight='bold')
            
            # box_pairs = [("G1", "G2+G3")]
            box_pairs = [("G1", "G2"), ("G2", "G3"), ("G1", "G3")]
            stat_test = "Mann-Whitney"
            statannot.add_stat_annotation(
                data=data, 
                ax=ax, 
                x="group", y="score",
                box_pairs=box_pairs,
                test=stat_test,
                text_format="star", # simple, 
                loc="inside",
                verbose=2
            )

    ## ======= PLOT SUBPLOT =========# 
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(12,5))
    sns.barplot(
        data=df1, 
        ax=axes, 
        x="metric", y="score", hue="group",
        width=0.4,
    )
    axes.set_ylim((0,5))
    axes.set_xlabel("")
    axes.tick_params(axis='both', labelsize=12)
    
    # box_pairs = []
    # for metric in list_metric:
    #     if metric == "Interest": 
    #         continue
    #     tmp = [
    #         ((metric, "G1"), (metric, "G2")),
    #         ((metric, "G2"), (metric, "G3")),
    #         ((metric, "G3"), (metric, "G1")),
    #     ]
    #     box_pairs.extend(tmp)

    # stat_test = "Mann-Whitney"
    # statannot.add_stat_annotation(
    #     data=df1, 
    #     ax=axes, 
    #     x="metric", y="score", hue="group",
    #     box_pairs=box_pairs,
    #     test=stat_test,
    #     text_format="star", # simple, 
    #     loc="inside",
    #     verbose=2
    # )


    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(f"[survey].png")
    plt.close()
    plt.show()










if __name__ == "__main__":

    # stat_survey()
    # stat_betweengroup()
    stat_withingroup()