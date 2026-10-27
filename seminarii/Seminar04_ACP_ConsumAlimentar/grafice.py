import numpy as np
from matplotlib import pyplot as plt

def plot_varianta(alpha:np.ndarray,std:bool=True,P:int=80):
    m=len(alpha)
    fig=plt.figure(figsize=(10,6))
    ax=fig.add_subplot(1,1,1)
    x=np.arange(1,m+1)
    ax.set_xticks(x)
    ax.set_title("Plot varianta",fontdict={"fontsize":16})
    ax.set_xlabel("Componenta",fontdict={"fontsize":12,"color":"b"})
    ax.set_ylabel("Varianta",fontdict={"fontsize":12,"color":"b"})
    ax.plot(x,alpha)
    ax.scatter(x,alpha,c="r",alpha=0.5)
    # plt.show()
    #Aplicare criterii de selectie
    #Criteriul Kaiser (se aplica pt modelul standardizat)
    if std:
        k1=len(np.where(alpha>1)[0])
        ax.axhline(1,color="g",label="Kaiser")
    else:
        k1=None

    #Criteriul variantei
    procent_cumulat=np.cumsum(alpha*100/sum(alpha))
    k2=np.where(procent_cumulat>P)[0][0]
    ax.axhline(alpha[k2],color="m",label="Procent de varianta >"+str(P))
    ax.legend()
    plt.show()
