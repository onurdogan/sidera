import marimo

__generated_with = "0.17.6"
app = marimo.App(width="medium")


@app.cell
def _():
    from pathlib import Path
    import marimo as mo
    import subprocess
    return Path, mo, subprocess


@app.cell
def _(mo):
    mo.md(r"""
    # 🔥 Inferno

    *"Lasciate ogne speranza, voi ch'intrate..."*

    Welcome to the Inferno workflow.

    Here, raw sequencing reads enter the fire of processing and emerge as refined datasets ready for downstream analysis.

    ---

    ## 🔥 Canto II-III-IV: Primer Trimming for Single-End

    Before entering the next stages of the pipeline, FASTQ files are prepared through primer trimming using **cutadapt**.

    ### 🔥 Workflow Path

    canto_II_single_end
            ↓
    canto_IV_primer_trimming
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # 📂 FASTQ Input Folder

    ## **__Enter FASTQ input folder path__**

    Provide the directory containing FASTQ files for primer trimming.
    """)
    return


@app.cell
def define_primer_trimming_input(mo):
    # 📂 Define input folder containing FASTQ files for primer trimming

    input_path = mo.ui.text(
        value="",
        label="Enter FASTQ input folder path"
    )

    input_path
    return (input_path,)


@app.cell
def _(input_path):
    input_path.value
    return


@app.cell
def _(mo):
    mo.md(r"""
    # 🔍 FASTQ File Selection

    ## **__Select FASTQ files for primer trimming__**

    Detected FASTQ files from the selected input folder will appear below.

    Choose the reads that will enter the primer trimming stage.
    """)
    return


@app.cell
def select_fastq_files_for_trimming(Path, input_path, mo):
    # 🔍 Detect FASTQ files in selected input folder

    TRIMMING_INPUT_DIR = Path(
        input_path.value
    )


    # Find FASTQ files

    fastq_files = sorted(
        TRIMMING_INPUT_DIR.glob("*.fastq.gz")
    )


    # File names

    fastq_names = [
        file.name
        for file in fastq_files
    ]


    # Select all / deselect all buttons

    select_all_button = mo.ui.button(
        label="Select all"
    )

    deselect_all_button = mo.ui.button(
        label="Deselect all"
    )


    # Multiselect FASTQ files

    fastq_selector = mo.ui.multiselect(
        options=fastq_names,
        label="Select FASTQ files for primer trimming"
    )


    mo.vstack(
        [
            select_all_button,
            deselect_all_button,
            fastq_selector
        ]
    )
    return TRIMMING_INPUT_DIR, fastq_selector


@app.cell
def define_primer_trimming_paths(TRIMMING_INPUT_DIR, mo):
    # Define Inferno and primer trimming output paths

    INFERNO_DIR = (
        TRIMMING_INPUT_DIR
        .parents[0]
    )


    PRIMER_TRIMMING_DIR = (
        INFERNO_DIR
        / "canto_04_primer_trimming"
    )


    PRIMER_TRIMMING_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    mo.md(
        f"""
    ## Detected workflow paths

    Input folder:

    `{TRIMMING_INPUT_DIR}`


    Inferno folder:

    `{INFERNO_DIR}`


    Primer trimming output:

    `{PRIMER_TRIMMING_DIR}`
    """
    )
    return (PRIMER_TRIMMING_DIR,)


@app.cell
def _(fastq_selector):
    fastq_selector.value
    return


@app.cell
def define_primer_sequences(mo):
    # 🧬 Enter primer sequences for cutadapt

    p5_primer = mo.ui.text(
        value="",
        label="P5 primer (5' → 3')"
    )


    p7_primer = mo.ui.text(
        value="",
        label="P7 primer (5' → 3')"
    )


    anchoring = mo.ui.dropdown(
        options=[
            "TRUE",
            "FALSE"
        ],
        value="FALSE",
        label="Anchoring"
    )


    mo.vstack(
        [
            p5_primer,
            p7_primer,
            anchoring
        ]
    )
    return anchoring, p5_primer, p7_primer


@app.cell
def _(anchoring, mo, p5_primer, p7_primer):
    # Check current widget values

    mo.md(
        f"""
    P5 value:

    `{p5_primer.value}`


    P7 value:

    `{p7_primer.value}`


    Anchoring:

    `{anchoring.value}`
    """
    )
    return


@app.cell
def _(anchoring, mo, p5_primer, p7_primer):
    # Prepare primers for cutadapt

    if anchoring.value == "TRUE":
        forward = "^" + p5_primer.value
        reverse = "^" + p7_primer.value

    else:
        forward = p5_primer.value
        reverse = p7_primer.value


    mo.md(
        f"""
    ## Cutadapt primers

    Forward (-g):

    `{forward}`


    Reverse (-a):

    `{reverse}`
    """
    )
    return


@app.cell
def _(PRIMER_TRIMMING_DIR, fastq_selector, mo):
    # Generate primer trimming output filenames

    trimmed_paths = [
        PRIMER_TRIMMING_DIR /
        file.replace(
            "_SE.fastq.gz",
            "_trimmed.fastq.gz"
        )
        for file in fastq_selector.value
    ]


    mo.md(
        f"""
    ## Generated trimmed files

    {chr(10).join(
        [f"- `{p.name}`" for p in trimmed_paths]
    )}
    """
    )
    return (trimmed_paths,)


@app.cell
def _(trimmed_paths):
    trimmed_paths
    return


@app.cell
def _(PRIMER_TRIMMING_DIR):
    # 📂 Create log directory for cutadapt reports

    CUTADAPT_LOG_DIR = (
        PRIMER_TRIMMING_DIR
        / "logs"
    )

    CUTADAPT_LOG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    CUTADAPT_LOG_DIR
    return (CUTADAPT_LOG_DIR,)


@app.cell
def _():
    import shutil

    shutil.which("cutadapt")
    return


@app.cell
def _(subprocess):
    test = subprocess.run(
        [
            "cutadapt",
            "--version"
        ],
        capture_output=True,
        text=True
    )

    test.stdout, test.stderr
    return


@app.cell
def run_cutadapt_primer_trimming(
    CUTADAPT_LOG_DIR,
    TRIMMING_INPUT_DIR,
    fastq_selector,
    p5_primer,
    p7_primer,
    subprocess,
    trimmed_paths,
):
    cutadapt_results = []

    for input_file, output_file in zip(
        fastq_selector.value,
        trimmed_paths
    ):

        input_fastq = (
            TRIMMING_INPUT_DIR / input_file
        )

        log_file = (
            CUTADAPT_LOG_DIR
            / f"{input_file.replace('.fastq.gz','')}_cutadapt.log"
        )

        result = subprocess.run(
            [
                "cutadapt",
                "-g",
                p5_primer.value,
                "-a",
                p7_primer.value,
                "-o",
                str(output_file),
                str(input_fastq)
            ],
            capture_output=True,
            text=True
        )

        with open(log_file, "w") as f:
            f.write(result.stdout)
            f.write(result.stderr)

        cutadapt_results.append(
            {
                "sample": input_file,
                "output": str(output_file),
                "status": result.returncode,
                "log": str(log_file)
            }
        )

    cutadapt_results
    return cutadapt_results, result


@app.cell
def summarize_cutadapt_results(trimmed_paths):
    # ✅ Verify trimmed FASTQ output files

    # Create an empty list that will store output file information
    trimmed_check = [

        {
            # Get only the filename from the full path
            "file": p.name,

            # Check whether the trimmed FASTQ file exists
            "exists": p.exists(),

            # Get file size in bytes, convert to MB, and round to 2 decimals
            "size_MB": round(
                p.stat().st_size / 1024**2,
                2
            )
        }

        # Repeat the dictionary creation for every file in trimmed_paths
        for p in trimmed_paths
    ]


    # Display the final verification table/list
    trimmed_check
    return


@app.cell
def _(Path, cutadapt_results):
    # ============================================================
    # Summarize cutadapt primer trimming performance
    # ============================================================

    import re
    import pandas as pd


    def summarize_primer_trimming(log_results):

        cutadapt_summary = []

        for trimming_result in log_results:

            current_log_file = Path(trimming_result["log"])

            if current_log_file.exists():

                log_text = current_log_file.read_text()

                total_reads_match = re.search(
                    r"Total reads processed:\s+([\d,]+)",
                    log_text
                )

                trimmed_reads_match = re.search(
                    r"Trimmed:\s+([\d,]+)\s+times",
                    log_text
                )

                cutadapt_summary.append(
                    {
                        "sample": trimming_result["sample"],
                        "total_reads": (
                            int(total_reads_match.group(1).replace(",", ""))
                            if total_reads_match
                            else None
                        ),
                        "primers_trimmed": (
                            int(trimmed_reads_match.group(1).replace(",", ""))
                            if trimmed_reads_match
                            else None
                        )
                    }
                )

        return pd.DataFrame(cutadapt_summary)


    cutadapt_summary = summarize_primer_trimming(cutadapt_results)

    cutadapt_summary
    return (pd,)


@app.cell
def _(result):
    result.stdout[:100]
    return


@app.cell
def _(fastq_selector, trimmed_paths):
    len(fastq_selector.value), len(trimmed_paths)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
