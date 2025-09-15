# This script plots the CDF of application configuration parameters
# It also prints some statistics about the application configurations
# The main goal is provide examples to the user on how to use the dataset

import os
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt

PLOT_FILE = "plot_app_configs.pdf"
DATA_FILE = "../data/app_configs.pickle"

COLUMNS = [
    "AppContainerRequestCpu",
    "AppContainerRequestMemory",
    "AppMinScale",
    "AppContainerConcurrency",
]

axs = plt.figure(figsize=(10, 2.2), dpi=300, constrained_layout=True).subplots(1, 4)


def plot_app_config():
    labels = [
        "Requested CPU (Cores)",
        "Requested Memory (GB)",
        "Minimum Pod Scale",
        "Container Concurrency Limit",
    ]
    df = pd.read_pickle(DATA_FILE)

    print(df.columns)

    df["AppMinScale"] = df["AppMinScale"].apply(
        lambda x: np.median(x)
    )  # picking the median value of MinScale over time for each app

    print("Unique median values in AppMinScale column: ", df["AppMinScale"].unique())

    print(
        "Apps with AppMinScale>=1:",
        100 * (1 - df["AppMinScale"].value_counts(normalize=True).get(0)),
        "%",
    )
    print(
        "Apps with AppMinScale==1:",
        100 * df["AppMinScale"].value_counts(normalize=True).get(1),
        "%",
    )

    df["AppContainerRequestCpu"] = df["AppContainerRequestCpu"].apply(
        lambda x: [i for i in x if math.isnan(i) == False]
    )

    df["AppContainerRequestCpuChanges"] = df["AppContainerRequestCpu"].apply(
        lambda x: [x[i + 1] - x[i] for i in range(len(x) - 1)]
    )
    df["AppContainerRequestCpuChangesUnique"] = df[
        "AppContainerRequestCpuChanges"
    ].apply(lambda x: [i for i in x if i != 0])
    print(
        "Apps that saw change in ContainerRequestCpu config during lifetime: ",
        100
        * df["AppContainerRequestCpuChangesUnique"].apply(lambda x: len(x) > 0).sum()
        / df["AppContainerRequestCpuChangesUnique"].count(),
        "%",
    )

    df["AppContainerRequestCpu"] = df["AppContainerRequestCpu"].apply(
        lambda x: np.median(x)
    )  # picking the median value of ContainerRequestCpu over time for each app
    print(
        "Unique values in AppContainerRequestCpu column: ",
        df["AppContainerRequestCpu"].unique(),
    )
    print(
        "Apps with AppContainerRequestCpu<1: ",
        100
        * df["AppContainerRequestCpu"][df["AppContainerRequestCpu"] < 1].count()
        / df["AppContainerRequestCpu"].count(),
        "%",
    )
    print(
        "Apps with AppContainerRequestCpu==1: ",
        100 * df["AppContainerRequestCpu"].value_counts(normalize=True).get(1),
        "%",
    )
    print(
        "Apps with AppContainerRequestCpu>1: ",
        100
        * df["AppContainerRequestCpu"][df["AppContainerRequestCpu"] > 1].count()
        / df["AppContainerRequestCpu"].count(),
        "%",
    )

    df["AppContainerRequestMemory"] = df["AppContainerRequestMemory"].apply(
        lambda x: [i for i in x if math.isnan(i) == False]
    )

    df["AppContainerRequestMemoryChanges"] = df["AppContainerRequestMemory"].apply(
        lambda x: [x[i + 1] - x[i] for i in range(len(x) - 1)]
    )
    df["AppContainerRequestMemoryChangesUnique"] = df[
        "AppContainerRequestMemoryChanges"
    ].apply(lambda x: [i for i in x if i != 0])
    print(
        "Apps that saw change in ContainerRequestMemory config during lifetime: ",
        100
        * df["AppContainerRequestMemoryChangesUnique"].apply(lambda x: len(x) > 0).sum()
        / df["AppContainerRequestMemoryChangesUnique"].count(),
        "%",
    )

    df["AppContainerRequestMemory"] = df["AppContainerRequestMemory"].apply(
        lambda x: np.median(x)
    )
    print(
        "Unique values in AppContainerRequestMemory column: ",
        df["AppContainerRequestMemory"].unique(),
    )
    print(
        "Apps with AppContainerRequestMemory<4: ",
        100
        * df["AppContainerRequestMemory"][df["AppContainerRequestMemory"] < 4].count()
        / df["AppContainerRequestMemory"].count(),
        "%",
    )
    print(
        "Apps with AppContainerRequestMemory==4: ",
        100 * df["AppContainerRequestMemory"].value_counts(normalize=True).get(4),
        "%",
    )
    print(
        "Apps with AppContainerRequestMemory>4: ",
        100
        * df["AppContainerRequestMemory"][df["AppContainerRequestMemory"] > 4].count()
        / df["AppContainerRequestMemory"].count(),
        "%",
    )

    df["AppContainerConcurrency"] = df["AppContainerConcurrency"].apply(
        lambda x: [i for i in x if math.isnan(i) == False]
    )
    df["AppContainerConcurrency"] = df["AppContainerConcurrency"].apply(
        lambda x: np.median(x)
    )
    print(
        "Unique values in AppContainerConcurrency column: ",
        df["AppContainerConcurrency"].unique(),
    )
    print(
        "Apps with AppContainerConcurrency<100: ",
        100
        * df["AppContainerConcurrency"][df["AppContainerConcurrency"] < 100].count()
        / df["AppContainerConcurrency"].count(),
        "%",
    )
    print(
        "Apps with AppContainerConcurrency==100: ",
        100 * df["AppContainerConcurrency"].value_counts(normalize=True).get(100),
        "%",
    )
    print(
        "Apps with AppContainerConcurrency>100: ",
        100
        * df["AppContainerConcurrency"][df["AppContainerConcurrency"] > 100].count()
        / df["AppContainerConcurrency"].count(),
        "%",
    )

    axs[0].vlines(
        x=1,
        color="k",
        linestyle="--",
        label="Default: 1",
        ymin=-0.05,
        ymax=1.05,
        zorder=1,
    )
    axs[1].vlines(
        x=4,
        color="k",
        linestyle="--",
        label="Default: 4",
        ymin=-0.05,
        ymax=1.05,
        zorder=1,
    )
    axs[2].vlines(
        x=0,
        color="k",
        linestyle="--",
        label="Default: 0",
        ymin=-0.05,
        ymax=1.05,
        zorder=1,
    )
    axs[3].vlines(
        x=100,
        color="k",
        linestyle="--",
        label="Default: 100",
        ymin=-0.05,
        ymax=1.05,
        zorder=1,
    )

    for i, col in enumerate(COLUMNS):
        data = df[col].tolist()

        cdfx = np.sort(data)
        cdfy = np.linspace(0, 1, len(cdfx))

        if i == 0:
            axs[i].set_ylabel("Fraction of Workloads")

        if i > 0:
            axs[i].set_yticklabels([])
            axs[i].tick_params(left=False)

        axs[i].set_xlabel(labels[i])
        axs[i].grid(alpha=0.2, zorder=0)
        axs[i].set_ylim(ymin=-0.05, ymax=1.05)
        if i == -1:
            pass
        else:
            axs[i].plot(cdfx, cdfy, zorder=2)
        if (i == 0) or (i == 1):
            axs[i].set_xscale("log")
        axs[i].legend(loc="lower right", fontsize=9)


if __name__ == "__main__":
    plot_app_config()
    plt.tight_layout()
    plt.savefig(PLOT_FILE)
