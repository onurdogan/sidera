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

The current repository includes:

* **Primer trimming**
* **Quality filtering**

The broader Inferno workflow is being developed to include additional steps such as:

* demultiplexing
* paired-end processing
* dereplication
* denoising
* ASV/OTU processing
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

A marimo-based workflow for primer-trimming of metabarcoding sequencing data.

### Inferno — Quality Filtering

`inferno_quality_filtering.py`

A marimo-based workflow for quality filtering of processed sequencing reads.

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
conda activate inferno
```

Alternatively, Python dependencies can be installed with:

```bash
pip install -r requirements.txt
```

---

## Usage

The current Inferno workflows are implemented as **marimo applications**.

For example:

```bash
marimo run inferno_primer_trimming.py
```

and:

```bash
marimo run inferno_quality_filtering.py
```

For interactive editing:

```bash
marimo edit inferno_primer_trimming.py
```

or:

```bash
marimo edit inferno_quality_filtering.py
```

The exact input files, parameters, and workflow configuration are defined within each Canto.

---

## Project Structure

```text
sidera/
│
├── 00_selva_oscura/          # Project initialization and data organization
├── 01_inferno/               # Sequence-processing workflows
├── 02_purgatory/             # Ecological and biodiversity analysis
├── 03_paradiso/              # Visualization and interpretation
│
├── krona_dashboard/           # Interactive taxonomic visualization
├── core/                      # Core functionality
├── database/                  # Structured data resources
├── data/                      # Project data
│
├── inferno_primer_trimming.py
├── inferno_quality_filtering.py
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

The current public repository represents an early stage of the framework. The Inferno sequence-processing workflow is currently the main area of development, while the Purgatory and Paradiso stages are being progressively developed.

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
