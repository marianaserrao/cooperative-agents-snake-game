import math
from typing import Optional, Sequence

import numpy as np
import matplotlib.pyplot as plt


def z_table(confidence):
    """Hand-coded Z-Table

    Parameters
    ----------
    confidence: float
        The confidence level for the z-value.

    Returns
    -------
        The z-value for the confidence level given.
    """
    return {
        0.99: 2.576,
        0.95: 1.96,
        0.90: 1.645
    }[confidence]


def confidence_interval(mean, n, confidence):
    """Computes the confidence interval of a sample.

    Parameters
    ----------
    mean: float
        The mean of the sample
    n: int
        The size of the sample
    confidence: float
        The confidence level for the z-value.

    Returns
    -------
        The confidence interval.
    """
    return z_table(confidence) * (mean / math.sqrt(n))


def standard_error(std_dev, n, confidence):
    """Computes the standard error of a sample.

    Parameters
    ----------
    std_dev: float
        The standard deviation of the sample
    n: int
        The size of the sample
    confidence: float
        The confidence level for the z-value.

    Returns
    -------
        The standard error.
    """
    return z_table(confidence) * (std_dev / math.sqrt(n))


def plot_confidence_bar(names, means, std_devs, N, title, x_label, y_label, confidence, show=False, filename=None, colors=None, yscale=None):
    """Creates a bar plot for comparing different agents/teams.

    Parameters
    ----------

    names: Sequence[str]
        A sequence of names (representing either the agent names or the team names)
    means: Sequence[float]
        A sequence of means (one mean for each name)
    std_devs: Sequence[float]
        A sequence of standard deviations (one for each name)
    N: Sequence[int]
        A sequence of sample sizes (one for each name)
    title: str
        The title of the plot
    x_label: str
        The label for the x-axis (e.g. "Agents" or "Teams")
    y_label: str
        The label for the y-axis
    confidence: float
        The confidence level for the confidence interval
    show: bool
        Whether to show the plot
    filename: str
        If given, saves the plot to a file
    colors: Optional[Sequence[str]]
        A sequence of colors (one for each name)
    yscale: str
        The scale for the y-axis (default: linear)
    """

    errors = [standard_error(std_devs[i], N[i], confidence) for i in range(len(means))]
    fig, ax = plt.subplots()
    x_pos = np.arange(len(names))
    ax.bar(x_pos, means, yerr=errors, align='center', alpha=0.5, color=colors if colors is not None else "gray", ecolor='black', capsize=10)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(names, fontsize=8)
    ax.set_title(title)
    ax.yaxis.grid(True)
    if yscale is not None:
        plt.yscale(yscale)
    plt.tight_layout()
    if filename is not None:
        plt.savefig(filename)
    if show:
        plt.show()
    plt.close()


def compare_results(results, confidence=0.95, title="Agents Comparison", metric="Steps Per Episode", colors=None):

    """Displays a bar plot comparing the performance of different agents/teams.

        Parameters
        ----------

        results: list
            
        confidence: float
            The confidence level for the confidence interval
        title: str
            The title of the plot
        metric: str
            The name of the metric for comparison
        colors: Sequence[str]
            A sequence of colors (one for each agent/team)

        """

    names = ["Random", "Fuly Greedy", "Partially Greedy", "Social Convention", "Intention Comm", "Roles"]
    means = [np.mean(result) for result in results]
    stds = [np.std(result) for result in results]
    N = [len(result) for result in results]

    plot_confidence_bar(
        names=names,
        means=means,
        std_devs=stds,
        N=N,
        title=title,
        x_label="", y_label=f"Avg. {metric}",
        confidence=confidence, show=True, colors=colors
    )

def count_deaths(deaths):
    death_counts = np.zeros((len(deaths), 2))

    for i in range(len(deaths)):
        for death in deaths[i]:
            if death == "WALL":
                death_counts[i][0] += 1 
            elif death == "SNAKE":
                death_counts[i][1] += 1
    
    return death_counts

def plot_deaths(results, colors):
    names = ["Random", "Fully Greedy", "Partially Greedy", "Social Convention", "Intention Comm", "Roles"]
    teams = len(names)
    deaths = ["WALL", "SNAKE"]
    
    values = count_deaths(results)

    plt.figure(figsize=(15, 5))

    for team in range(teams):
        plot = plt.subplot(1, teams, team+1)
        plt.xlabel("Loss Type")
        plt.ylabel("Number of Occurrences")
        plt.title(names[team])
        plt.bar(deaths, values[team], color=colors[team])

    plt.suptitle("Causes of Loss")
    plt.show()


