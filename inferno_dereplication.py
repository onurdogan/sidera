import marimo

__generated_with = "0.17.6"

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from pathlib import Path
    import subprocess

    return Path, mo, subprocess


@app.cell
def _(mo):
    mo.md(
        """
        # 🔥 Inferno

        ## Canto VI: Dereplication

        Dereplication of quality-filtered single-end sequences using VSEARCH.
        """
    )
    return


@app.cell
def _(Path, mo):
    projects_root = Path.cwd()

    available_projects = sorted(
        [
            p.name
            for p in projects_root.iterdir()
            if p.is_dir()
            and (p / "00_selva_oscura").exists()
        ]
    )

    project_selector = mo.ui.dropdown(
        options=available_projects,
        label="Select Sidera project:",
    )

    project_selector

    return project_selector


@app.cell
def _(Path, project_selector, mo):
    if project_selector.value:
        PROJECT_DIR = Path.cwd() / project_selector.value

        QUALITY_FILTER_INPUT_DIR = (
            PROJECT_DIR
            / "01_inferno"
            / "canto_05_quality_filtering"
        )

        if QUALITY_FILTER_INPUT_DIR.exists():
            fastq_files = sorted(
                QUALITY_FILTER_INPUT_DIR.glob("*.fastq.gz")
            )
        else:
            fastq_files = []

        mo.md(
            f"""
            **Project:** `{project_selector.value}`

            **Canto V input directory:**  
            `{QUALITY_FILTER_INPUT_DIR}`

            **FASTQ files found:** {len(fastq_files)}
            """
        )

    else:
        PROJECT_DIR = None
        QUALITY_FILTER_INPUT_DIR = None
        fastq_files = []

        mo.md(
            "⚠️ Please select a Sidera project."
        )

    return PROJECT_DIR, QUALITY_FILTER_INPUT_DIR, fastq_files


@app.cell
def _(fastq_files, mo):
    fastq_options = [file.name for file in fastq_files]

    fastq_selector = mo.ui.multiselect(
        options=fastq_options,
        label="Select FASTQ files for dereplication:",
    )

    fastq_selector

    return fastq_selector


@app.cell
def _(QUALITY_FILTER_INPUT_DIR, mo):
    if QUALITY_FILTER_INPUT_DIR is not None:
        INFERNO_DIR = QUALITY_FILTER_INPUT_DIR.parent

        DEREPLICATION_DIR = (
            INFERNO_DIR / "canto_06_dereplication"
        )

        mo.md(
            f"""
            ### Output directory

            `{DEREPLICATION_DIR}`
            """
        )

    else:
        INFERNO_DIR = None
        DEREPLICATION_DIR = None

        mo.md(
            "⚠️ Please select a Sidera project first."
        )

    return DEREPLICATION_DIR, INFERNO_DIR


@app.cell
def _(
    DEREPLICATION_DIR,
    fastq_selector,
    mo,
):
    if DEREPLICATION_DIR is not None and fastq_selector.value:
        _existing_outputs = []

        for _filename in fastq_selector.value:
            _sample_name = _filename.replace(
                "_quality_filtered.fastq.gz",
                "",
            )

            _output_fasta_gz = (
                DEREPLICATION_DIR
                / f"{_sample_name}_dereplicated.fasta.gz"
            )

            if _output_fasta_gz.exists():
                _existing_outputs.append(
                    _output_fasta_gz.name
                )

        if _existing_outputs:
            mo.md(
                "### ⚠️ Existing output files detected\n\n"
                + "\n".join(
                    f"- `{_filename}`"
                    for _filename in _existing_outputs
                )
                + "\n\n"
                "**Do you want to overwrite these files?**"
            )

            overwrite_selector = mo.ui.radio(
                options=["No", "Yes"],
                value="No",
                label="Overwrite existing files:",
            )

            overwrite_selector

        else:
            overwrite_selector = mo.ui.radio(
                options=["No"],
                value="No",
                label="No existing output files.",
            )

            overwrite_selector

    else:
        overwrite_selector = mo.ui.radio(
            options=["No"],
            value="No",
            label="Select FASTQ files first.",
        )

        overwrite_selector

    return overwrite_selector


@app.cell
def _(mo):
    run_dereplication = mo.ui.run_button(
        label="🔥 Run Dereplication"
    )

    run_dereplication

    return run_dereplication


@app.cell
def _(
    DEREPLICATION_DIR,
    QUALITY_FILTER_INPUT_DIR,
    fastq_selector,
    mo,
    overwrite_selector,
    run_dereplication,
    subprocess,
):
    if run_dereplication.value:
        selected_files = fastq_selector.value

        if not selected_files:
            output = mo.md(
                "⚠️ Please select at least one FASTQ file."
            )

        else:
            results = []

            for filename in selected_files:
                input_fastq = (
                    QUALITY_FILTER_INPUT_DIR / filename
                )

                sample_name = filename.replace(
                    "_quality_filtered.fastq.gz",
                    "",
                )

                temporary_fasta = (
                    DEREPLICATION_DIR
                    / f"{sample_name}_dereplicated.fasta"
                )

                output_fasta_gz = (
                    DEREPLICATION_DIR
                    / f"{sample_name}_dereplicated.fasta.gz"
                )

                if (
                    output_fasta_gz.exists()
                    and overwrite_selector.value != "Yes"
                ):
                    results.append(
                        {
                            "sample": filename,
                            "output": output_fasta_gz.name,
                            "status": "⚠️ Already exists — skipped",
                        }
                    )

                    continue

                result = subprocess.run(
                    [
                        "vsearch",
                        "--fastx_uniques",
                        str(input_fastq),
                        "--fastaout",
                        str(temporary_fasta),
                        "--sizeout",
                        "--relabel",
                        f"{sample_name}_",
                        "--threads",
                        "0",
                    ],
                    capture_output=True,
                    text=True,
                )

                if result.returncode == 0:
                    gzip_result = subprocess.run(
                        [
                            "gzip",
                            "-f",
                            str(temporary_fasta),
                        ],
                        capture_output=True,
                        text=True,
                    )

                    if gzip_result.returncode == 0:
                        results.append(
                            {
                                "sample": filename,
                                "output": output_fasta_gz.name,
                                "status": "✅ Completed",
                            }
                        )
                    else:
                        results.append(
                            {
                                "sample": filename,
                                "output": output_fasta_gz.name,
                                "status": "❌ Gzip failed",
                            }
                        )

                else:
                    results.append(
                        {
                            "sample": filename,
                            "output": output_fasta_gz.name,
                            "status": "❌ VSEARCH failed",
                        }
                    )

            output = mo.md(
                "### Dereplication results\n\n"
                + "\n".join(
                    (
                        f"- **{r['sample']}** → "
                        f"`{r['output']}` — "
                        f"{r['status']}"
                    )
                    for r in results
                )
            )

    else:
        output = mo.md(
            "Ready to run dereplication."
        )

    output

    return


if __name__ == "__main__":
    app.run()