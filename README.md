# fish1.5-release Notebooks

This repository contains Jupyter notebooks for working with zebrafish EM + functional imaging datasets from the fish1.5 dataset.

---

## Environment Setup

We recommend using Conda:

```bash
conda env create -f environment.yml
conda activate fish-env
```

---

## Tutorials

You can follow full walkthroughs and tutorials at:

https://jboulanger91.github.io/fish1.5-release/tutorials/

---

## Notebooks

- `functional_responses.ipynb`: Analyze and visualize calcium imaging responses.
- `download_mesh_and_synapses.ipynb`: Access and download neuron meshes + synaptic info from CAVE.
- `CAVE_setup.ipynb`: Setup notebook for authenticating and configuring CAVE access.

---

## Dependencies

All required packages are listed in `environment.yml`, which defines an environment named `fish-env`.
