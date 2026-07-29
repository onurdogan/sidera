# Sidera

**Sidera** is a modular framework for DNA metabarcoding and environmental DNA (eDNA) analysis that combines reproducible bioinformatics workflows, structured data management, and interactive biodiversity visualization.

The project is inspired by Dante Alighieri's *Divine Comedy*, where each stage of the analytical workflow represents a journey from raw sequencing data to biological interpretation.

---

## Project Architecture

```
Sidera
│
├── 00_selva_oscura
│   ├── settings
│   ├── raw_data
│   └── metadata
│
├── 01_inferno
│   ├── Canto I
│   ├── Canto II
│   └── ...
│
├── 02_purgatory
│   ├── ecological analyses
│   ├── quality control
│   └── biodiversity metrics
│
├── 03_paradiso
│   ├── visualization
│   ├── reporting
│   └── knowledge generation
│
├── krona_dashboard
├── core
├── database
└── data
```

---

## Workflow Philosophy

### 00 · Selva Oscura

The "dark forest" where every project begins.

This stage contains:

- project settings
- metadata
- sequencing files
- reference databases
- workflow configuration

Everything downstream is driven from this central entry point.

---

### 01 · Inferno

Raw sequencing data are transformed into structured biological information.

Planned modules include:

- Demultiplexing
- Single-end processing
- Paired-end merging
- Primer trimming
- Quality filtering
- Dereplication
- Denoising
- OTU/ASV clustering
- Taxonomic assignment

Each processing step is implemented as an independent **Canto**.

---

### 02 · Purgatory

Data refinement and ecological interpretation.

Examples:

- contamination removal
- filtering
- diversity analyses
- statistical workflows
- ecological metrics

---

### 03 · Paradiso

The final interpretation layer.

Outputs include:

- biodiversity reports
- interactive visualizations
- Krona dashboards
- publication-ready figures
- integrated ecological knowledge

---

## Components

### Krona Dashboard

Interactive visualization module for exploring taxonomic composition generated from metabarcoding workflows.

---

## Current Status

Sidera is currently under active development.

The long-term goal is to provide a complete, modular, reproducible, and user-friendly platform for DNA metabarcoding research.

---

## License

MIT License.
