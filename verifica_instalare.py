# Ruleaza: python verifica_instalare.py  -> verifica ca toate bibliotecile pentru DSAD merg
import sys
print("Python:", sys.version.split()[0], "|", sys.executable)
for nume in ["pandas", "numpy", "scipy", "matplotlib", "seaborn", "sklearn", "factor_analyzer"]:
    try:
        modul = __import__(nume)
        print(f"  OK   {nume:16} {getattr(modul, '__version__', '')}")
    except Exception as e:
        print(f"  LIPSA {nume:15} -> {e}")

import warnings
import numpy as np
from factor_analyzer import FactorAnalyzer
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    x = np.random.default_rng(0).normal(size=(50, 4))
    FactorAnalyzer(n_factors=2, rotation="varimax").fit(x)
print("Analiza factoriala (factor_analyzer + scikit-learn): OK")
