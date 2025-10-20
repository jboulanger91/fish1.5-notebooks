# fish1.5-release Notebooks

This repository contains Jupyter notebooks for working with zebrafish EM + functional imaging datasets from the fish1.5 dataset.

---

## Environment Setup

We recommend using Conda (or Mamba for faster installs):

```bash
conda env create -f environment.yml
conda activate fish-env
```

or

```bash
mamba env create -f environment.yml
mamba activate fish-env
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

See `environment.yml` for all required packages.
