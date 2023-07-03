# mwplotlib
An extension to Matplotlib that plots the shape of the Milky Way.

# Installation
```
pip install mwplotlib
```

# Usage
Here is a simple example of how to use mwplotlib:
```python
from mwplotlib import MilkyWay
import matplotlib.pyplot as plt

# Plot the Milky Way in polar coordinates (region-style)
plt.figure(figsize=(9, 9))
plt.MilkyWay.shape(plot_type="polar", style="region")

# Plot the Milky Way in polar coordinates (line-style)
plt.figure(figsize=(9, 9))
plt.MilkyWay.shape(plot_type="polar", style="line")

# Plot the Milky Way in Cartesian coordinates (region-style)
plt.figure(figsize=(9, 9))
plt.MilkyWay.shape(plot_type="cartesian", style="region")

# Plot the Milky Way in Cartesian coordinates (line-style)
plt.figure(figsize=(9, 9))
plt.MilkyWay.shape(plot_type="cartesian", style="line")
```

For more examples of usage, please refer to [examples](./example.ipynb) notebook. Those examples are also available on Google Colab:
 - [v1.1.0 (Latest)](https://colab.research.google.com/drive/1Jk6WsD9TVHMwbThDjm192cEQLWn4qpbz?usp=sharing)
 - [v1.0.0](https://colab.research.google.com/drive/1M9IawDSco0dbIZz5crcxTUm4NkWu43fq?usp=sharing)

# Reference
<!-- Citation Y. Xu et al 2023 ApJ 947 54 -->
<!-- https://iopscience.iop.org/article/10.3847/1538-4357/acc45c -->
The galaxy model and data used in this package is based on the following paper:
```Latex
@ARTICLE{2023ApJ...947...54X,
       author = {{Xu}, Y. and {Hao}, C.~J. and {Liu}, D.~J. and {Lin}, Z.~H. and {Bian}, S.~B. and {Hou}, L.~G. and {Li}, J.~J. and {Li}, Y.~J.},
        title = "{What Does the Milky Way Look Like?}",
      journal = {\apj},
     keywords = {Galaxy structure, Milky Way Galaxy, Trigonometric parallax, 622, 1054, 1713},
         year = 2023,
        month = apr,
       volume = {947},
       number = {2},
          eid = {54},
        pages = {54},
          doi = {10.3847/1538-4357/acc45c},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2023ApJ...947...54X},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```
Please BOTH cite the above paper AND acknowledge this package if you are using it in your research.

# License
This package is licensed under the MIT license. See [LICENSE](./LICENSE) for details.

# Acknowledgement
We would like to thank the authors of the above paper for making their data publicly available, which made this package possible. We would also like to credit Prof. Ryan Trainor at Franklin and Marshall College for his guidance and support.
