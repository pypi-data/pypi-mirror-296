Overview
========

D-LIM (Direct-Latent Interpretable Model) is a neural network that
enhances genotype-fitness mapping by combining interpretability with
predictive accuracy. It assumes independent phenotypic influences of
genes on fitness, leading to advanced accuracy and insights into
phenotype analysis and epistasis. The model includes an extrapolation
method for better understanding of genetic interactions and integrates
multiple data sources to improve performance in low-data biological
research.

Requirements
============

The implementation has been tested on a Linux system for: Python 3.10.9;
Pytorch 2.0.1; numpy 1.23.5; pandas 2.0.2.

Installation
============

Install the package from Pypi:

``` {.bash}
pip install dlim
```

Or install it from the sources:

``` {.bash}
pip install .
```

Usage
=====

The code snippet bellow shows how to use fit D-LIM for fitness
prediction.

Load packages
-------------

``` {.python results="output"}
from dlim.model import DLIM 
from dlim.dataset import Data_model
from dlim.api import DLIM_API
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import r2_score
from numpy import mean
from numpy.random import choice
import pandas as pd
from tqdm import tqdm  
import matplotlib.pyplot as plt 
import numpy as np 
```

Read the data, there are 2 genes (or variables) here
----------------------------------------------------

    df_data = pd.read_csv("../data/data_env_1.csv", sep = ',', header = None)
    data = Data_model(data=df_data, n_variables=2)

Create DLIM model
-----------------

    # Here, we used 2 latent phenotype, the data has 37 possible mutations.
    # For D-LIM, we use here 1 hidden layer of 32 neurons.
    model = DLIM(n_variables = 2, hid_dim = 32, nb_layer = 0)
    dlim_regressor = DLIM_API(model=model, flag_spectral=True)

Split data into training and validation
---------------------------------------

    train_id = choice(range(data.data.shape[0]), int(data.data.shape[0]*0.7), replace=False)
    val_id = [i for i in range(data.data.shape[0]) if i not in train_id]
    train_data = data.subset(train_id)
    val_data = data.subset(val_id)

Train model
-----------

    # We train the model with a learning rate of 1e-2 for 300 steps with batch size
    # 16 and regularization of 1e-2
    losses = dlim_regressor.fit(train_data, lr = 1e-2, nb_epoch=300, batch_size=32, emb_regularization=1e-2)

Prediction on validation data
-----------------------------

    # Now, we compute the validation prediction
    fit, var, _  = dlim_regressor.predict(val_data.data[:,:-1], detach=True) 

    score = pearsonr(fit.flatten(), val_data.data[:, [-1]].flatten())[0]
    print(score)

Plot and get landscape
----------------------

    # Here, we plot the trained landscape
    fig, (bx, cx, dx) = plt.subplots(1, 3, figsize=(6, 2))
    dlim_regressor.plot(bx, data)

    for xx in [bx, cx, dx]:
        for el in ["top", "right"]:
            xx.spines[el].set_visible(False)

    # Plot the a00verage curve
    print(pearsonr(lat_a[:, 0], data[:, -1]))
    cx.scatter(lat_a[:, 0], data[:, -1], s=5, c="grey")
    dx.scatter(lat_a[:, 1], data[:, -1], s=5, c="grey")
    cx.set_ylabel("F")
    dx.set_xlabel("$\\varphi^1$")
    cx.set_xlabel("$\\varphi^2$")
    plt.tight_layout()
    plt.show()

```{=html}
<p align="center"><img src="https://github.com/LBiophyEvo/D-LIM-model/blob/main/reproducibility/img/spec_harry_env_1.png" /></p>
```
More details of the usage and the installation can be found in doc:
===================================================================

-   [Read the docs of D-LIM](https://d-lim.readthedocs.io/en/latest/)

Data download:
==============

-   [Datasets](https://drive.google.com/drive/folders/1hwixojm3thyYpf8X6qPG7NIvxQseFDKz?usp=sharing)

``` {.example}
None
```

Reproduction of the manuscript
==============================

Figures and analyses of the manuscript can be found in File
`reproducibility`.

License
=======

MIT
