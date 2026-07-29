# Krona Dashboard

Interactive Krona visualisation for DNA metabarcoding biodiversity data.

> "Nel mezzo del cammin di nostra vita  
> mi ritrovai per una selva oscura..."
>
> — Dante Alighieri, *Divina Commedia*
>
> "In the middle of the journey our life **I** [came to]  
> myself in a dark wood [where] the straight way was lost..."
> 
> — The Inferno of Dante Alighieri

Krona Dashboard transforms taxon tables into interactive Krona charts.

---

## Overview

DNA metabarcoding analyses generate complex taxonomic tables that can be difficult to interpret visually. Krona Dashboard provides a lightweight workflow to transform **[TaxonTableTools2](https://github.com/TillMacher/TaxonTableTools2))** taxon tables into interactive **[Krona](https://github.com/marbl/Krona)** charts.

Current workflow:
# krona-dashboard
Interactive Krona visualisation for [TaxonTableTools2](https://github.com/TillMacher/TaxonTableTools2) outputs.

Current workflow: 

TaxonTableTools2 taxon table -> Krona Dashboard -> Interactive Krona chart

---

## Features

- Load TaxonTableTools2 taxon tables.
- Explore hierarchical taxonomic composition.
- Generate interactive Krona HTML visualisations.
- Support biodiversity and DNA metabarcoding studies.

---

## Usage
## macOS Installation

## Option 1:

### Download [zip](https://github.com/onurdogan/krona-dashboard/archive/refs/heads/main.zip) 

Download the repository as a **[zip](https://github.com/onurdogan/krona-dashboard/archive/refs/heads/main.zip)** file from GitHub and extract it.

Open your terminal in the `krona-dashboard` folder

**or** 

```
cd krona-dashboard
```

**or**

On macOS, you can open Terminal directly in the project folder:

1. Open the `krona-dashboard` folder in Finder.
2. Right-click the folder.
3. Select **New Terminal at Folder**.
4. Run:

Install the required Python dependencies from [requirements.txt](https://github.com/onurdogan/krona-dashboard/blob/main/requirements.txt):

**then**

[Marimo](https://github.com/marimo-team/marimo) dashboard

Open your terminal in the `krona-dashboard` folder

```
 marimo run marimo/krona_dashboard.py
```

The dashboard will open in your browser.

## Option 2: Conda

### Requirements

## Requirements

- ### Option 1: Conda

- With this option, **Krona Dashboard** and all required dependencies are installed using **Conda**.
- If you do not have Conda installed, install **Miniconda** or Anaconda first.
- After installation, initialize Conda for your shell if needed:

```
conda init zsh
```

- Restart your terminal before continuing.

```
cd path/to/krona-dashboard-main/krona-dashboard
```

Create the environment: 

```
conda env create -f environment.yml

```

Activate: 

```
conda activate krona-dashboard
```
### Krona requirement
#### Krona Tools

Krona Dashboard uses Krona Tools (`ktImportText`) to generate interactive Krona visualisations.

Krona is installed automatically when using the provided Conda environment.

### Workflow:
- Select a TaxonTableTools2 taxon table
- Select a sample
- Generate Krona output
- Open the interactive HTML chart


## Requirements
### Software
- Python ≥ 3.11
- Marimo
- Pandas
- Krona Tools

## Installation
Install Python dependencies:

```
pip install -r requirements.txt
```

## Scientific background 
### TaxonTableTools2
Krona Dashboard uses taxonomic tables generated from [TaxonTableTools2](https://github.com/TillMacher/TaxonTableTools2).
#### Citation:
Macher, T. H., Beermann, A. J., & Leese, F. (2021).
TaxonTableTools—A comprehensive, platform-independent graphical user interface software to explore and visualise DNA metabarcoding data.
Molecular Ecology Resources.
https://doi.org/10.1111/1755-0998.13358  

### Krona 
Interactive visualisation is provided using Krona.
#### Citation:
Ondov, B. D., Bergman, N. H., & Phillippy, A. M. (2011).
Interactive metagenomic visualization in a Web browser.
BMC Bioinformatics, 12, 385.
https://doi.org/10.1186/1471-2105-12-385  

## Development status
Krona Dashboard is actively under development.
Future directions:
Streamlit user interface

## License
MIT License.
