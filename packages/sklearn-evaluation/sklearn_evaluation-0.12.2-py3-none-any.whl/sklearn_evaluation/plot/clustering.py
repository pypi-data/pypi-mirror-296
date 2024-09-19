"""
Plots for clustering models

NOTE: this is largely based in the scikit-plot cluster module. License below.

MIT License

Copyright (c) [2018] [Reiichiro Nakano]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import time

import matplotlib.pyplot as plt
import numpy as np

from sklearn.base import clone
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.preprocessing import LabelEncoder
from joblib import Parallel, delayed

from ploomber_core.exceptions import modify_exceptions
from sklearn_evaluation.plot.style import apply_theme


@apply_theme()
def _generate_axes(cluster, figsize, ax):
    if ax is not None:
        if not isinstance(ax, list):
            ax = [ax]
        if len(cluster) != len(ax):
            raise ValueError(
                f"Received lengths, cluster : {len(cluster)},"
                f"axes : {len(ax)}."
                f"Number of axes passed should match number of clusters"
            )
    else:
        ax = []
        for i in range(len(cluster)):
            _, axes = plt.subplots(1, 1, figsize=figsize)
            ax.append(axes)
    return ax


@modify_exceptions
def elbow_curve(
    X,
    clf,
    range_n_clusters=None,
    n_jobs=1,
    show_cluster_time=True,
    ax=None,
):
    """Plots elbow curve of different values of K of a clustering algorithm.

    Parameters
    ----------
    X : array-like, shape = [n_samples, n_features]:
        Data to cluster, where n_samples is the number of samples and
        n_features is the number of features.
        Refer https://numpy.org/doc/stable/glossary.html#term-array-like

    clf
        Clusterer instance that implements ``fit``,``fit_predict``, and
        ``score`` methods, and an ``range_n_clusters`` hyperparameter.
        e.g. :class:`sklearn.cluster.KMeans` instance

    range_n_clusters : None or :obj:`list` of int, optional
        List of n_clusters for which to plot the explained variances.
        Defaults to ``[1, 3, 5, 7, 9, 11]``.

    n_jobs : int, optional
        Number of jobs to run in parallel. Defaults to 1.

    show_cluster_time : bool, optional
        Include plot of time it took to cluster for a particular K.

    ax : :class:`matplotlib.axes.Axes`, optional
        The axes upon which to plot the curve. If None, the plot is drawn
        on the current Axes

    Returns
    -------
    ax: matplotlib Axes
        Axes containing the plot

    Examples
    --------

    Plot the Elbow Curve:

    .. plot:: ../examples/elbow_curve.py

    """

    if range_n_clusters is None:
        range_n_clusters = range(1, 10, 2)
    else:
        range_n_clusters = sorted(range_n_clusters)

    if not hasattr(clf, "n_clusters"):
        raise TypeError(
            '"n_clusters" attribute not in classifier. ' "Cannot plot elbow method."
        )

    if not hasattr(clf, "score"):
        raise AttributeError(
            """clf does not have a score method. Ensure it's one of the following:
            KMeans, MiniBatchKMeans, or BisectingKMeans"""
        )

    tuples = Parallel(n_jobs=n_jobs)(
        delayed(_clone_and_score_clusterer)(clf, X, i) for i in range_n_clusters
    )
    clfs, times = zip(*tuples)
    sum_of_squares = np.absolute(clfs)
    return elbow_curve_from_results(
        range_n_clusters, sum_of_squares, times if show_cluster_time else None, ax=ax
    )


@apply_theme()
@modify_exceptions
def elbow_curve_from_results(n_clusters, sum_of_squares, times, ax=None):
    """
    Same as `elbow_curve`, but it takes the number of clusters and sum of
    squares as inputs. Useful if you want to train the models yourself.

    Examples
    --------

    Plot the Elbow Curve from the results:

    .. plot:: ../examples/elbow_curve_from_results.py

    """

    idx = np.argsort(n_clusters)
    n_clusters = np.array(n_clusters)[idx]
    sum_of_squares = np.array(sum_of_squares)[idx]

    if ax is None:
        _, ax = plt.subplots()

    ax.set_title("Elbow Plot")
    ax.grid(True)
    ax.plot(n_clusters, sum_of_squares, label="Elbow")

    ax.set_xlabel("Number of clusters")
    ax.set_ylabel("Sum of Squared Errors")

    handles, labels = ax.get_legend_handles_labels()
    if times is not None:
        times = np.array(times)[idx]
        ax2_color = "green"
        ax2 = ax.twinx()
        ax2.plot(
            n_clusters, times, ":", alpha=0.75, color=ax2_color, label="Fitting time"
        )
        ax2.set_ylabel("Clustering duration (seconds)", color=ax2_color, alpha=0.75)
        ax2.tick_params(colors=ax2_color)

        handles2, labels2 = ax2.get_legend_handles_labels()
        handles = handles + handles2
        labels = labels + labels2

    ax.legend(handles, labels)

    return ax


def _clone_and_score_clusterer(clf, X, n_clusters):
    """Clones and scores a clustering model"""
    start = time.time()
    clf = clone(clf)
    setattr(clf, "n_clusters", n_clusters)
    return clf.fit(X).score(X), time.time() - start


@modify_exceptions
def silhouette_analysis(
    X,
    clf,
    range_n_clusters=None,
    metric="euclidean",
    figsize=None,
    cmap=None,
    text_fontsize="medium",
    ax=None,
):
    """Plots silhouette analysis of clusters provided.

    Parameters
    -----------

    X : array-like, shape = [n_samples, n_features]:
        Cluster data, where n_samples is the number of samples and
        n_features is the number of features.
        Refer https://numpy.org/doc/stable/glossary.html#term-array-like

    clf
        Clusterer instance that implements ``fit``,``fit_predict``, and
        ``score`` methods, and an ``n_clusters`` hyperparameter.
        e.g. :class:`sklearn.cluster.KMeans` instance

    range_n_clusters : None or :obj:`list` of int, optional
        List of n_clusters for which to plot the silhouette scores.
        Defaults to ``[2, 3, 4, 5, 6]``.

    metric : string or callable, optional:
        The metric to use when calculating distance between instances in
        a feature array. If metric is a string, it must be one of the
        options allowed by sklearn.metrics.pairwise.pairwise_distances.
        If X is the distance array itself, use "precomputed" as the metric.

    figsize : 2-tuple, optional:
        Tuple denoting figure size of the plot
        e.g. (6, 6). Defaults to ``None``.

    cmap : string or :class:`matplotlib.colors.Colormap` instance, optional:
        Colormap used for plotting the projection. View Matplotlib Colormap
        documentation for available options.
        https://matplotlib.org/users/colormaps.html

    text_fontsize : string or int, optional:
        Matplotlib-style fontsizes.
        Use e.g. "small", "medium", "large" or integer-values. Defaults to
        "medium".

    ax : :class:`matplotlib.axes.Axes`, optional:
        The axes upon which to plot the curve. If None, the plot is drawn on
        a new set of axes.

    Returns
    -------
    ax: matplotlib Axes
        Axes containing the plot


    Examples
    --------

    Plot the Silhouette Analysis:

    .. plot:: ../examples/silhouette_plot_basic.py

    Notes
    -----
    .. versionadded:: 0.8.3

    """
    if range_n_clusters is None:
        range_n_clusters = [2, 3, 4, 5, 6]
    else:
        range_n_clusters = sorted(range_n_clusters)

    if not hasattr(clf, "n_clusters"):
        raise TypeError(
            '"n_clusters" attribute not in classifier. '
            "Cannot plot silhouette analysis ."
        )

    # if no ax is passed by user generate new plot
    # for each model

    ax = _generate_axes(range_n_clusters, figsize, ax)

    for ax, n_clusters in zip(ax, range_n_clusters):
        clf = clone(clf)
        setattr(clf, "n_clusters", n_clusters)
        cluster_labels = clf.fit_predict(X)
        _silhouette_analysis_one_model(
            X, cluster_labels, metric, figsize, cmap, text_fontsize, ax
        )
    return ax


@apply_theme(cmap_style="gradient")
@modify_exceptions
def _silhouette_analysis_one_model(
    X,
    cluster_labels,
    metric="euclidean",
    figsize=None,
    cmap=None,
    text_fontsize="medium",
    ax=None,
):
    """
    Generate silhouette plot for one value of n_cluster.
    """
    cluster_labels = np.asarray(cluster_labels)

    le = LabelEncoder()
    cluster_labels_encoded = le.fit_transform(cluster_labels)

    n_clusters = len(np.unique(cluster_labels))

    silhouette_avg = silhouette_score(X, cluster_labels, metric=metric)

    sample_silhouette_values = silhouette_samples(X, cluster_labels, metric=metric)

    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=figsize)

    ax.set_xlim([-0.1, 1])

    if hasattr(X, "shape"):
        length = X.shape[0]
    else:
        length = len(X)
    ax.set_ylim([0, length + (n_clusters + 1) * 10 + 10])

    ax.set_xlabel("Silhouette coefficient values", fontsize=text_fontsize)
    ax.set_ylabel("Cluster label", fontsize=text_fontsize)

    y_lower = 10

    for i in range(n_clusters):
        ax.set_title(f"Silhouette Analysis (n_clusters={n_clusters})", fontsize="large")

        ith_cluster_silhouette_values = sample_silhouette_values[
            cluster_labels_encoded == i
        ]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = plt.cm.get_cmap(cmap)(float(i) / n_clusters)

        ax.fill_betweenx(
            np.arange(y_lower, y_upper),
            0,
            ith_cluster_silhouette_values,
            facecolor=color,
            edgecolor=color,
            alpha=0.7,
        )

        ax.text(
            -0.05,
            y_lower + 0.5 * size_cluster_i,
            str(le.classes_[i]),
            fontsize=text_fontsize,
        )

        y_lower = y_upper + 10

    ax.axvline(
        x=silhouette_avg,
        color="red",
        linestyle="--",
        label="Silhouette score: {0:0.3f}".format(silhouette_avg),
    )

    ax.set_yticks([])  # Clear the y-axis labels / ticks
    ax.set_xticks(np.arange(-0.1, 1.0, 0.2))

    ax.tick_params(labelsize=text_fontsize)
    ax.legend(loc="best", fontsize=text_fontsize)
    return ax


@modify_exceptions
def silhouette_analysis_from_results(
    X,
    cluster_labels,
    metric="euclidean",
    figsize=None,
    cmap=None,
    text_fontsize="medium",
    ax=None,
):
    """
    Same as `silhouette_plot` but takes list of cluster_labels as input.
    Useful if you want to train the model yourself

    Examples
    --------

    Plot the Silhouette Analysis from the results:

    .. plot:: ../examples/silhouette_plot_from_results.py

    """

    # if no ax is passed by user generate new plot
    # for each model

    ax = _generate_axes(cluster_labels, figsize, ax)

    for ax, label in zip(ax, cluster_labels):
        _silhouette_analysis_one_model(
            X, label, metric, figsize, cmap, text_fontsize, ax
        )
    return ax
