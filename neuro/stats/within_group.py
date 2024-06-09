from utils import get_data
import matplotlib.pyplot as plt
import seaborn as sns
import statannot
import matplotlib.patches as mpatches



def stat_withingroup():
    """
    Compare match-run within each group, e.g.,
    2sample x 4subject => 8 sample / group
        Fx_run1_4-6_m1  Fx_run2_4-6_m1
        Fx_run1_6-8_m1  Fx_run2_6-8_m1
        ...
    """
    method = "SparseFBCSP+LDA"
    df = get_data(method)


    # ## ---------stats------------##
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15,10))
    list_model_name = ["MI_2class_hand", "MI_2class_foot"]
    list_group = ["G1", "G2", "G3"]
    list_palette = ["Reds", "Blues"]
    
    for i, model_name in enumerate(list_model_name):
        for j, group in enumerate(list_group):
        
            ## ---------plot------------##
            data = df.loc[df["model_name"]==model_name] \
                        .loc[df["group"] == group]
            ax = axes[i,j]

            box = sns.boxplot(
                ax=ax, 
                data=data,
                x="runs", y="score",
                width=0.4,
                showmeans=True,
                boxprops=dict(linestyle='-', linewidth=2),
                medianprops=dict(linestyle='-', linewidth=2),
                whiskerprops=dict(linestyle='--', linewidth=2),
                capprops=dict(linestyle='-', linewidth=2),
                meanprops=dict(markerfacecolor='white',markeredgecolor='black', markersize=8),
                palette=list_palette[i],
            )
            ax.set_ylim((0,1))
            ax.grid(False)
            fontsize = 18
            ax.tick_params(axis='both', labelsize=fontsize)
            ax.set_xlabel("", fontsize=fontsize)
            if (i==0 and j==0) or (i==1 and j==0):
                ax.set_ylabel("(mean ROC)", fontsize=fontsize)
            ax.set_title(group, fontsize=fontsize, fontweight='bold')

            ## ---------statannot------------##
            if (i==0 and j==2):
                box_pairs=[("run1", "run2")]
                stat_test = "Wilcoxon"
                statannot.add_stat_annotation(
                    ax=ax,
                    data=data,
                    x="runs", y="score",
                    box_pairs=box_pairs,
                    test=stat_test,
                    loc="inside",
                    text_format="star", 
                    comparisons_correction=None,
                    verbose=2
                )

            if (i==0 and j==2) or (i==1 and j==2):
                ax.legend(handles=[
                    mpatches.Patch(color=sns.color_palette(list_palette[i])[2], 
                                label=f'[{model_name}] run1'),
                    mpatches.Patch(color=sns.color_palette(list_palette[i])[4], 
                                label=f'[{model_name}] run2'),
            
                                    ],
                    loc='lower right', fontsize=12
                )
    # plt.legend(loc='upper right', fontsize=14)
    
    plt.tight_layout()
    plt.savefig(f"[withingroup]_{method}_2model.png")
    plt.close()
    plt.show()
