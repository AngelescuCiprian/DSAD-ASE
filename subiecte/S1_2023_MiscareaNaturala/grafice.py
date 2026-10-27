# Grafice - plot_varianta e al profului (seminarul 4), restul sunt in acelasi stil.

import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram


def plot_varianta(alpha: np.ndarray, std: bool = True, P: int = 80):
    m = len(alpha)
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    x = np.arange(1, m + 1)
    ax.set_xticks(x)
    ax.set_title("Plot varianta", fontdict={"fontsize": 16})
    ax.set_xlabel("Componenta", fontdict={"fontsize": 12, "color": "b"})
    ax.set_ylabel("Varianta", fontdict={"fontsize": 12, "color": "b"})
    ax.plot(x, alpha)
    ax.scatter(x, alpha, c="r", alpha=0.5)
    if std:
        ax.axhline(1, color="g", label="Kaiser")
    procent_cumulat = np.cumsum(alpha * 100 / sum(alpha))
    k2 = np.where(procent_cumulat > P)[0][0]
    ax.axhline(alpha[k2], color="m", label="Procent de varianta >" + str(P))
    ax.legend()


def plot_scoruri(s: np.ndarray, etichete, titlu="Plot scoruri", k1=0, k2=1):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(titlu, fontdict={"fontsize": 16})
    ax.set_xlabel("C" + str(k1 + 1), fontdict={"fontsize": 12, "color": "b"})
    ax.set_ylabel("C" + str(k2 + 1), fontdict={"fontsize": 12, "color": "b"})
    ax.axhline(0, color="g")
    ax.axvline(0, color="g")
    ax.scatter(s[:, k1], s[:, k2], c="r", alpha=0.5)
    for i in range(len(etichete)):
        ax.text(s[i, k1], s[i, k2], etichete[i], fontsize=7)


def plot_dendrograma(h: np.ndarray, etichete, prag=None, titlu="Dendrograma"):
    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(titlu, fontdict={"fontsize": 16})
    dendrogram(h, labels=list(etichete), color_threshold=prag, ax=ax, leaf_font_size=5)
    if prag is not None:
        ax.axhline(prag, color="r", linestyle="--", label="Prag partitie optimala")
        ax.legend()


def plot_histograme(valori: np.ndarray, etichete_clusteri: np.ndarray, variabila: str):
    clusteri = np.unique(etichete_clusteri)
    fig = plt.figure(figsize=(12, 5))
    fig.suptitle("Histograme pentru variabila " + variabila, fontsize=16)
    for i, cl in enumerate(clusteri):
        ax = fig.add_subplot(1, len(clusteri), i + 1)
        ax.set_title(cl)
        ax.hist(valori[etichete_clusteri == cl], bins=10, rwidth=0.9, range=(valori.min(), valori.max()))


def show(salveaza_in="data_out"):
    # salveaza toate graficele deschise ca PNG (ca sa le vezi si pe GitHub), apoi le afiseaza
    for nr in plt.get_fignums():
        fig = plt.figure(nr)
        if fig._suptitle is not None:
            titlu = fig._suptitle.get_text()
        elif fig.axes and fig.axes[0].get_title():
            titlu = fig.axes[0].get_title()
        else:
            titlu = "grafic"
        nume = "".join(ch if ch.isalnum() else "_" for ch in titlu).strip("_")
        fig.savefig(salveaza_in + "/" + str(nr) + "_" + nume + ".png", dpi=120, bbox_inches="tight")
    plt.show()
