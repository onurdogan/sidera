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

    ---

    ## 🔥 Canto 05: Quality Filtering

    Primer-trimmed FASTQ files are quality filtered using VSEARCH.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    Enter desired primer-trimmed FASTQ folder path
    """)
    return


@app.cell
def define_primer_trimming_input(mo):
    # 📂 Quality Filtering Input Folder

    mo.md(
        """
    # 📂 Quality Filtering Input Folder

    ## **Enter desired primer-trimmed FASTQ folder path**

    Provide the directory containing primer-trimmed FASTQ files for quality filtering.
    """
    )

    input_dir = mo.ui.text(
        value="",
        label="Primer-trimmed FASTQ folder"
    )

    input_dir
    return (input_dir,)


@app.cell
def _(input_dir):
    input_dir.value
    return


@app.cell
def _(mo):
    mo.md(r"""
    # 🔍 FASTQ File Selection

    ## **__Select primer-trimmed FASTQ files for quality filtering__**

    Detected FASTQ files from the selected input folder will appear below.

    Choose the reads that will enter the quality filtering stage using VSEARCH.
    """)
    return


@app.cell
def select_trimmed_fastq_files_for_quality_filtering(Path, input_dir, mo):
    # 🔍 Detect FASTQ files in selected input folder

    QUALITY_FILTER_INPUT_DIR = Path(
        input_dir.value
    )


    # Find FASTQ files

    fastq_files = sorted(
        QUALITY_FILTER_INPUT_DIR.glob("*.fastq.gz")
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
        label="Select primer-trimmed FASTQ files for quality filtering"
    )


    mo.vstack(
        [
            select_all_button,
            deselect_all_button,
            fastq_selector
        ]
    )
    return QUALITY_FILTER_INPUT_DIR, fastq_selector


@app.cell
def _(fastq_selector, filtered_paths):
    # ✅ Verify input and output file counts match
    #
    # The number of selected FASTQ files should equal
    # the number of generated quality filtered output files.

    len(fastq_selector.value), len(filtered_paths)
    return


@app.cell
def define_quality_filtering_path(QUALITY_FILTER_INPUT_DIR, mo):
    # Define Inferno and quality filtering output paths

    INFERNO_DIR = (
        QUALITY_FILTER_INPUT_DIR
        .parents[0]
    )


    QUALITY_FILTERING_DIR = (
        INFERNO_DIR
        / "canto_05_quality_filtering"
    )


    QUALITY_FILTERING_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    mo.md(
        f"""
    ## Detected workflow paths

    Input folder:

    `{QUALITY_FILTER_INPUT_DIR}`


    Inferno folder:

    `{INFERNO_DIR}`


    Quality filtering output:

    `{QUALITY_FILTERING_DIR}`
    """
    )
    return (QUALITY_FILTERING_DIR,)


@app.cell
def _(fastq_selector):
    fastq_selector.value
    return


@app.cell
def _(mo):
    # ⚙️ Quality filtering parameters for VSEARCH

    max_ee = mo.ui.number(
        value=1,
        start=0,
        step=1,
        label="Maximum expected errors (maxEE)"
    )


    min_length = mo.ui.number(
        value=110,
        start=0,
        step=1,
        label="Minimum sequence length"
    )


    max_length = mo.ui.number(
        value=160,
        start=0,
        step=1,
        label="Maximum sequence length"
    )


    mo.vstack(
        [
            max_ee,
            min_length,
            max_length
        ]
    )
    return max_ee, max_length, min_length


@app.cell
def _(max_ee, max_length, min_length, mo):
    # Prepare VSEARCH quality filtering parameters

    MAX_EE = max_ee.value
    MIN_LENGTH = min_length.value
    MAX_LENGTH = max_length.value


    mo.md(
        f"""
    ## VSEARCH quality filtering parameters

    Maximum expected errors (maxEE):

    `{MAX_EE}`


    Minimum sequence length:

    `{MIN_LENGTH} bp`


    Maximum sequence length:

    `{MAX_LENGTH} bp`
    """
    )
    return


@app.cell
def _(QUALITY_FILTERING_DIR, fastq_selector, mo):
    # Generate quality filtering output filenames

    filtered_paths = [
        QUALITY_FILTERING_DIR /
        file.replace(
            "_trimmed.fastq.gz",
            "_quality_filtered.fastq.gz"
        )
        for file in fastq_selector.value
    ]


    mo.md(
        f"""
    ## Generated quality filtered files

    {chr(10).join(
        [f"- `{p.name}`" for p in filtered_paths]
    )}
    """
    )
    return (filtered_paths,)


@app.cell
def _(filtered_paths):
    filtered_paths
    return


@app.cell
def _(QUALITY_FILTERING_DIR):
    # 📂 Create log directory for VSEARCH quality filtering reports

    VSEARCH_LOG_DIR = (
        QUALITY_FILTERING_DIR
        / "logs"
    )

    VSEARCH_LOG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    VSEARCH_LOG_DIR
    return (VSEARCH_LOG_DIR,)


@app.cell
def _():
    import shutil

    shutil.which("vsearch")
    return


@app.cell
def _(subprocess):
    test = subprocess.run(
        [
            "vsearch",
            "--version"
        ],
        capture_output=True,
        text=True
    )

    test.stdout, test.stderr
    return


@app.cell
def run_quality_filtering(
    QUALITY_FILTER_INPUT_DIR,
    VSEARCH_LOG_DIR,
    fastq_selector,
    filtered_paths,
    max_ee,
    max_length,
    min_length,
    subprocess,
):
    quality_filter_results = []

    for input_file, output_file in zip(
        fastq_selector.value,
        filtered_paths
    ):

        input_fastq = (
            QUALITY_FILTER_INPUT_DIR / input_file
        )

        log_file = (
            VSEARCH_LOG_DIR
            / f"{input_file.replace('.fastq.gz','')}_quality_filtering.log"
        )

        result = subprocess.run(
            [
                "vsearch",
                "--fastq_filter",
                str(input_fastq),
                "--fastq_maxee",
                str(max_ee.value),
                "--fastq_minlen",
                str(min_length.value),
                "--fastq_maxlen",
                str(max_length.value),
                "--fastqout",
                str(output_file)
            ],
            capture_output=True,
            text=True
        )

        with open(log_file, "w") as f:
            f.write(result.stdout)
            f.write(result.stderr)

        quality_filter_results.append(
            {
                "sample": input_file,
                "output": str(output_file),
                "status": result.returncode,
                "log": str(log_file)
            }
        )

    quality_filter_results
    return quality_filter_results, result


@app.cell
def summarize_vsearch_results(filtered_paths):
    # ✅ Verify quality filtered FASTQ output files

    # Create an empty list that will store output file information
    filtered_check = [

        {
            # Get only the filename from the full path
            "file": p.name,

            # Check whether the quality filtered FASTQ file exists
            "exists": p.exists(),

            # Get file size in bytes, convert to MB, and round to 2 decimals
            "size_MB": round(
                p.stat().st_size / 1024**2,
                2
            )
        }

        # Repeat the dictionary creation for every file in filtered_paths
        for p in filtered_paths
    ]


    # Display the final verification table/list
    filtered_check
    return


@app.cell
def _(Path, quality_filter_results):
    # ============================================================
    # Summarize VSEARCH quality filtering performance
    # ============================================================

    import re
    import pandas as pd


    def summarize_quality_filtering(log_results):

        quality_filter_summary = []

        for filtering_result in log_results:

            current_log_file = Path(
                filtering_result["log"]
            )

            if current_log_file.exists():

                log_text = current_log_file.read_text()

                kept_match = re.search(
                    r"(\d+)\s+sequences kept",
                    log_text
                )

                discarded_match = re.search(
                    r"(\d+)\s+sequences discarded",
                    log_text
                )

                kept_reads = (
                    int(kept_match.group(1))
                    if kept_match
                    else None
                )

                discarded_reads = (
                    int(discarded_match.group(1))
                    if discarded_match
                    else None
                )

                total_reads = (
                    kept_reads + discarded_reads
                    if kept_reads is not None and discarded_reads is not None
                    else None
                )

                quality_filter_summary.append(
                    {
                        "sample": filtering_result["sample"],
                        "total_reads": total_reads,
                        "quality_filtered_reads": kept_reads,
                        "discarded_reads": discarded_reads,
                        "retained_percent": (
                            round(
                                kept_reads / total_reads * 100,
                                2
                            )
                            if total_reads
                            else None
                        )
                    }
                )

        return pd.DataFrame(
            quality_filter_summary
        )


    quality_filter_summary = summarize_quality_filtering(
        quality_filter_results
    )

    quality_filter_summary
    return (pd,)


@app.cell
def _(result):
    # 🔍 Preview VSEARCH quality filtering output
    #
    # VSEARCH writes processing summaries to stderr rather than stdout.
    # This preview displays the first part of the command output,
    # including the number of retained and discarded sequences.
    #
    # Retained reads:
    #   sequences passing maxEE and length filtering
    #
    # Discarded reads:
    #   sequences removed during quality filtering


    result.stdout[:500], result.stderr[:500]
    return


@app.cell
def _(QUALITY_FILTER_INPUT_DIR):
    test_input = (
        QUALITY_FILTER_INPUT_DIR
        / "D1_R1_trimmed.fastq.gz"
    )
    return (test_input,)


@app.cell
def _(subprocess, test_input):
    test_result = subprocess.run(
        [
            "vsearch",
            "--fastq_filter",
            str(test_input),
            "--fastq_maxee",
            "20",
            "--fastqout",
            "D1_test_maxee20.fastq.gz"
        ],
        capture_output=True,
        text=True
    )

    test_result.stderr
    return


@app.cell
def _(test_input):
    # 🔍 Check read length distribution after primer trimming

    import gzip
    from Bio import SeqIO


    lengths = []

    with gzip.open(
        test_input,
        "rt"
    ) as handle:

        for record in SeqIO.parse(
            handle,
            "fastq"
        ):
            lengths.append(len(record.seq))


    min(lengths), max(lengths), len(lengths)
    return SeqIO, gzip, lengths


@app.cell
def _(lengths, pd):
    pd.Series(lengths).describe()
    return


@app.cell
def _(Path):
    PRIMER_LOG_DIR = Path(
        "/Users/onurdogan/sidera-main/KÇ_Winter_2026/01_inferno/canto_04_primer_trimming/logs"
    )

    list(PRIMER_LOG_DIR.glob("*.log"))[:5]
    return (PRIMER_LOG_DIR,)


@app.cell
def _(PRIMER_LOG_DIR):
    # 🔍 Inspect first cutadapt primer trimming log

    first_log = list(
        PRIMER_LOG_DIR.glob("*.log")
    )[0]

    print(first_log.read_text())
    return


@app.cell
def _(Path, SeqIO, gzip):
    # 🔍 Inspect primer trimmed reads
    trimmed_file_check = Path(
        "/Users/onurdogan/sidera-main/KÇ_Winter_2026/01_inferno/canto_04_primer_trimming/D1_R1_trimmed.fastq.gz"
    )

    with gzip.open(trimmed_file_check, "rt") as fq_handle_check:

        for i, seq_record_check in enumerate(
            SeqIO.parse(fq_handle_check, "fastq")
        ):

            print(seq_record_check.id)
            print("Length:", len(seq_record_check.seq))
            print(seq_record_check.seq)
            print()

            if i == 5:
                break
    return


if __name__ == "__main__":
    app.run()
