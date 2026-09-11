# Sidera

**Sidera** is a modular framework for environmental DNA (eDNA) metabarcoding and biodiversity data analysis.

The project is designed to organize bioinformatics workflows into reproducible, independent processing steps, while connecting sequence processing with downstream biodiversity analysis, visualization, and ecological interpretation.

Inspired by Dante Alighieri's *Divine Comedy*, Sidera organizes the analytical journey into four stages:

* 🌲 **00 · Selva Oscura** — project initialization and data organization
* 🔥 **01 · Inferno** — sequence processing and quality control
* ⛰️ **02 · Purgatory** — data refinement and ecological analysis
* ⭐ **03 · Paradiso** — visualization, reporting, and biological interpretation

> **Sidera is under active development.** The current repository focuses primarily on the **Inferno** sequence-processing workflow.

---

## Workflow

### 00 · Selva Oscura

The starting point of an analysis.

This stage is intended to organize:

* project settings
* sample metadata
* raw sequencing data
* reference resources
* workflow configuration

The aim is to establish a consistent project structure before sequence processing begins.

### 01 · Inferno

The sequence-processing stage of Sidera.

Each processing step is organized as an independent **Canto**, allowing workflows to be developed, tested, and executed as modular components.

The current Inferno workflow includes:

1. **Canto I — Demultiplexing**
2. **Canto II — Single-end processing**
3. **Canto III — Paired-end merging**
4. **Canto IV — Primer trimming**
5. **Canto V — Quality filtering**
6. **Canto VI — Dereplication**

The broader Inferno workflow is being developed to include additional steps such as:

* clustering
* denoising
* chimera removal
* taxonomic assignment

### 02 · Purgatory

The data-refinement and ecological-analysis stage.

Planned functionality includes:

* data quality refinement
* contamination filtering
* biodiversity metrics
* community analysis
* multivariate statistics
* ecological interpretation

### 03 · Paradiso

The interpretation and communication stage.

The long-term vision includes:

* biodiversity visualization
* interactive dashboards
* automated reporting
* publication-ready figures
* integrated biological and ecological interpretation

---

## Current Components

### Inferno — Primer Trimming

`inferno_primer_trimming.py`

A marimo-based workflow for primer trimming of metabarcoding sequencing data.

### Inferno — Quality Filtering

`inferno_quality_filtering.py`

A marimo-based workflow for quality filtering of sequencing reads using VSEARCH.

### Inferno — Dereplication

`inferno_dereplication.py`

A marimo-based workflow for dereplication of quality-filtered sequences using VSEARCH.

Dereplicated sequences are generated as compressed FASTA files with abundance information retained in sequence headers.

### Krona Dashboard

`sidera/krona_dashboard/`

An interactive visualization component for exploring taxonomic composition from metabarcoding results.

---

## Technology Stack

Sidera currently uses the following Python ecosystem:

* **Python 3.12**
* **marimo** — reactive notebooks and applications
* **pandas** — tabular data processing
* **Polars** — high-performance DataFrame operations
* **NumPy** — numerical computing
* **PyArrow** — columnar data and Parquet support
* **DuckDB** — analytical database operations
* **SciPy** — scientific computing
* **scikit-learn** — statistical and multivariate analysis
* **scikit-bio** — biological and ecological analysis
* **Matplotlib** — scientific visualization
* **Plotly** — interactive visualization
* **Kaleido** — static export of Plotly figures
* **OpenPyXL** — Excel file support

---

## Installation

Clone the repository:

```bash
git clone https://github.com/onurdogan/sidera.git
cd sidera
```

Create the Conda environment:

```bash
conda env create -f environment.yml
```

Activate the environment:

```bash
conda activate sidera
```

Alternatively, Python dependencies can be installed with:

```bash
pip install -r requirements.txt
```

---

## Usage

The current Inferno workflows are implemented as **marimo applications**.

### Canto IV — Primer Trimming

```bash
marimo run inferno_primer_trimming.py
```

### Canto V — Quality Filtering

```bash
marimo run inferno_quality_filtering.py
```

### Canto VI — Dereplication

```bash
marimo run inferno_dereplication.py
```

For interactive editing:

```bash
marimo edit inferno_primer_trimming.py
```

```bash
marimo edit inferno_quality_filtering.py
```

```bash
marimo edit inferno_dereplication.py
```

The exact input files, parameters, and workflow configuration are defined within each Canto.

---

## Project Structure

A Sidera project is organized into four analytical stages:

```text
project/
├── 00_selva_oscura/          # Project initialization and data organization
│
├── 01_inferno/               # Sequence-processing workflows
│   ├── canto_01_demultiplexing/
│   ├── canto_02_single_end/
│   ├── canto_03_paired_end_merging/
│   ├── canto_04_primer_trimming/
│   ├── canto_05_quality_filtering/
│   ├── canto_06_dereplication/
│   ├── canto_07_clustering/
│   ├── canto_08_denoising/
│   ├── canto_09_chimera_removal/
│   └── canto_10_taxonomic_assignment/
│
├── 02_purgatory/             # Ecological and biodiversity analysis
└── 03_paradiso/              # Visualization and interpretation
```

The repository itself contains the workflow applications and supporting components:

```text
sidera/
├── inferno_primer_trimming.py
├── inferno_quality_filtering.py
├── inferno_dereplication.py
│
├── sidera/
│   └── krona_dashboard/
│
├── core/
├── database/
├── data/
│
├── environment.yml
├── requirements.txt
├── pyproject.toml
├── LICENSE
└── README.md
```

> The directory structure represents the evolving architecture of Sidera. Some components are currently under development.

---

## Design Philosophy

Sidera is built around three principles:

### Modular

Each analytical step can be developed and evaluated independently as a **Canto**.

### Reproducible

Workflow configuration, processing steps, and analytical outputs are intended to be traceable and reproducible across projects.

### Biological-first

The computational workflow is designed around biological and ecological questions rather than computation for its own sake.

---

## Development Status

🚧 **Sidera is under active development.**

The current public repository represents an early stage of the framework. The **Inferno** sequence-processing workflow is currently the main area of development, while the **Purgatory** and **Paradiso** stages are being progressively developed.

---

## License

Sidera is released under the **MIT License**.

See [`LICENSE`](LICENSE) for the full license text.

---

## Author

**Onur Doğan**

Researcher working on environmental DNA (eDNA), molecular ecology, and biodiversity assessment across marine and freshwater ecosystems.

---

## Citation

A formal citation for Sidera will be provided as the project develops toward a stable release.
