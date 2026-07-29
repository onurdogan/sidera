import marimo

__generated_with = "0.17.6"
app = marimo.App(width="medium")


@app.cell
def _(Path):
    # --------------------------------------------------------
    # Define project directory
    # --------------------------------------------------------

    project_dir = Path(__file__).resolve().parent.parent

    return (project_dir,)

@app.cell
def _(project_dir):
    # --------------------------------------------------------
    # Prepare Krona output directory
    # --------------------------------------------------------

    krona_dir = project_dir / "Krona_Charts"

    krona_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    krona_dir
    return (krona_dir,)


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    from pathlib import Path
    from io import BytesIO

    import subprocess
    import shutil
    import webbrowser

    return (
        BytesIO,
        Path,
        mo,
        pd,
        shutil,
        subprocess,
        webbrowser,
    )

@app.cell
def _(mo):
    # --------------------------------------------------------
    # Select Taxon Table file
    # --------------------------------------------------------

    taxon_file = mo.ui.file(
        filetypes=[".xlsx"],
        multiple=False,
        label="Select Taxon Table Excel file"
    )

    taxon_file
    return (taxon_file,)


@app.cell
def _(taxon_file):
    # --------------------------------------------------------
    # Check uploaded file
    # --------------------------------------------------------

    taxon_file.value
    return


@app.cell
def _(BytesIO, pd, taxon_file):
    # --------------------------------------------------------
    # Load Taxon Table
    # --------------------------------------------------------

    taxon_table = pd.read_excel(
        BytesIO(
            taxon_file.value[0].contents
        ),
        sheet_name="Taxon Table"
    )

    taxon_table
    return (taxon_table,)


@app.cell
def _():
    # --------------------------------------------------------
    # Define taxonomy columns
    # --------------------------------------------------------

    taxonomy_columns = [
        "Kingdom",
        "Phylum",
        "Class",
        "Order",
        "Family",
        "Genus",
        "Species"
    ]

    taxonomy_columns
    return (taxonomy_columns,)


@app.cell
def _(taxon_table, taxonomy_columns):
    # --------------------------------------------------------
    # Detect sample columns
    # --------------------------------------------------------

    # Identify abundance columns.
    # Taxonomy and sequence-related columns are excluded
    # only for sample selection purposes.

    excluded_columns = (
        taxonomy_columns +
        [
            "Hash",
            "Similarity",
            "N_hashes",
            "Seq",
            "Taxon"
        ]
    )


    sample_columns = [
        col for col in taxon_table.columns
        if col not in excluded_columns
    ]


    sample_columns
    return (sample_columns,)


@app.cell
def _(mo, sample_columns):
    # --------------------------------------------------------
    # Select sample
    # --------------------------------------------------------

    sample_selector = mo.ui.dropdown(
        options=sample_columns,
        value=sample_columns[0],
        label="Select sample"
    )

    sample_selector
    return (sample_selector,)


@app.cell
def _(sample_selector, taxon_table):
    # --------------------------------------------------------
    # Prepare Krona input table
    # --------------------------------------------------------

    sample = sample_selector.value

    krona_df = (
        taxon_table[
            [
                "Hash",
                "N_hashes",
                "Kingdom",
                "Phylum",
                "Class",
                "Order",
                "Family",
                "Genus",
                "Species",
                sample
            ]
        ]
        .rename(
            columns={
                sample: "Count"
            }
        )
    )

    krona_df.head()
    return krona_df, sample


@app.cell
def _(krona_df):
    # --------------------------------------------------------
    # Create N_hashes label
    # --------------------------------------------------------

    krona_df["N_hashes_label"] = (
        "N_hashes="
        + krona_df["N_hashes"].astype(str)
    )

    krona_df.head()
    return


@app.cell
def _(mo):
    # --------------------------------------------------------
    # Krona controls
    # --------------------------------------------------------

    krona_resolution = mo.ui.dropdown(
        options=[
            "Species",
            "Species + N_hashes",
            "Hash + N_hashes"
        ],
        value="Species"
    )


    krona_status = mo.ui.dropdown(
        options=[
            "Disabled",
            "Enabled"
        ],
        value="Enabled"
    )


    mo.vstack([
        krona_resolution,
        krona_status
    ])
    return krona_resolution, krona_status


@app.cell
def _(krona_status, mo):
    # --------------------------------------------------------
    # Krona generation debug
    # --------------------------------------------------------

    mo.md(
        f"""
    ## Krona generation status

    **Selection:**

    {krona_status.value}
    """
    )
    return


@app.cell
def _(krona_df, krona_resolution, taxonomy_columns):
    # --------------------------------------------------------
    # Prepare Krona columns based on resolution
    # --------------------------------------------------------

    if krona_resolution.value == "Species":

        selected_krona_columns = (
            ["Count"]
            + taxonomy_columns
        )


    elif krona_resolution.value == "Species + N_hashes":

        selected_krona_columns = (
            ["Count"]
            + taxonomy_columns
            + ["N_hashes_label"]
        )


    elif krona_resolution.value == "Hash + N_hashes":

        selected_krona_columns = (
            ["Count"]
            + taxonomy_columns
            + ["Hash_label"]
        )


    krona_input = krona_df[
        selected_krona_columns
    ].copy()


    krona_input.head()
    return (krona_input,)


@app.cell
def _(krona_df):
    print(krona_df.head())
    print(krona_df.columns.tolist())
    return


@app.cell
def _(krona_df):
    # --------------------------------------------------------
    # Create Krona labels
    # --------------------------------------------------------

    krona_df["N_hashes_label"] = (
        "N_hashes="
        + krona_df["N_hashes"].astype(str)
    )


    krona_df["Hash_label"] = (
        krona_df["Hash"].astype(str)
        + " (N_hashes="
        + krona_df["N_hashes"].astype(str)
        + ")"
    )


    krona_df.head()
    return


@app.cell
def _(krona_df, krona_input, mo):
    # --------------------------------------------------------
    # Check Krona filtering result
    # --------------------------------------------------------

    mo.md(
        f"""
    ## Krona filtering check

    Before filtering: {len(krona_df)}

    Krona input entries: {len(krona_input)}
    """
    )
    return


@app.cell
def _(krona_input, krona_resolution, mo, sample):
    # --------------------------------------------------------
    # Krona input summary
    # --------------------------------------------------------

    mo.md(
        f"""
    ## Krona input summary

    **Sample:** {sample}

    **Resolution:** {krona_resolution.value}

    **Total reads:** {krona_input["Count"].sum():,}

    **Entries:** {len(krona_input)}
    """
    )
    return


@app.cell
def _(krona_dir, krona_input, mo, sample):
    # --------------------------------------------------------
    # Export Krona input file
    # --------------------------------------------------------

    krona_input_file = (
        krona_dir /
        f"{sample}_krona_input.txt"
    )


    krona_input.to_csv(
        krona_input_file,
        sep="\t",
        header=False,
        index=False
    )


    mo.md(
        f"""
    ## Krona input exported

    **File:** `{krona_input_file.name}`

    **Rows written:** {len(krona_input)}

    **Total reads:** {krona_input["Count"].sum():,}
    """
    )
    return (krona_input_file,)


@app.cell
def _(krona_input_file, merged_krona_input):
    # --------------------------------------------------------
    # Preview Krona text input
    # --------------------------------------------------------

    preview_file = (
        merged_krona_input
        if merged_krona_input is not None
        else krona_input_file
    )

    with open(preview_file, "r") as preview_handle:

        for line_number in range(5):

            print(
                preview_handle.readline().strip()
            )
    return


@app.cell
def _(krona_input):
    krona_input.head()
    return


@app.cell
def _(
    krona_dir,
    krona_input,
    krona_input_file,
    krona_resolution,
    krona_status,
    mo,
    sample,
    subprocess,
):
    # --------------------------------------------------------
    # Generate Krona HTML chart
    # --------------------------------------------------------

    krona_html_file = (
        krona_dir /
        f"{sample}_krona.html"
    )


    if krona_status.value == "Enabled":

        result = subprocess.run(
            [
                "ktImportText",
                str(krona_input_file),
                "-o",
                str(krona_html_file)
            ],
            capture_output=True,
            text=True
        )


        if result.returncode == 0:
            status = "✅ Krona chart created successfully"
        else:
            status = "❌ Krona generation failed"


        message = mo.md(
            f"""
    ## {status}

    **Sample:** {sample}

    **Resolution:** {krona_resolution.value}

    **Total reads:** {krona_input["Count"].sum():,}

    **Entries:** {len(krona_input)}

    **Output exists:** {krona_html_file.exists()}

    **Output file:**

    `{krona_html_file}`


    **Return code:** {result.returncode}
    """
        )

    else:

        message = mo.md(
            """
    ⏸️ Krona generation disabled.
    """
        )

    # --------------------------------------------------------
    # Krona command debug
    # --------------------------------------------------------

    mo.md(
        f"""
    ## 🔍 Krona command debug

    This section reports the result of the `ktImportText` command.

    **Return code:** {result.returncode}

    Interpretation:
    - `0` → Krona HTML file was created successfully.
    - Any other value → Krona generation failed; check STDERR for the error reason.


    ### STDOUT
    Contains normal messages returned by Krona.
    Usually includes the generated output file path.

    {result.stdout}


    ### STDERR
    Contains warnings or error messages.
    If Krona fails, the reason is usually reported here.

    {result.stderr}


    ### Output file check

    Exists:
    {krona_html_file.exists()}

    File:
    `{krona_html_file}`
    """
    )

    message
    return (krona_html_file,)


@app.cell
def _(krona_html_file):
    krona_html_file.exists()
    return


@app.cell
def _(krona_html_file, mo):
    # --------------------------------------------------------
    # Check Krona HTML path
    # --------------------------------------------------------

    mo.md(
        f"""
    ## Krona file check

    Path:

    `{krona_html_file}`

    Exists:

    { krona_html_file.exists() }
    """
    )
    return


@app.cell
def _(krona_dir, krona_html_file):
    # --------------------------------------------------------
    # Serve Krona chart through local HTTP server
    # --------------------------------------------------------

    import http.server
    import socketserver
    import threading
    import socket
    import os


    def find_free_port(start_port=8505):
        """
        Find an available port starting from start_port.
        """

        port = start_port

        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

                if sock.connect_ex(("localhost", port)) != 0:
                    return port

                port += 1


    krona_port = find_free_port(8505)


    krona_folder = str(krona_dir)

    handler = http.server.SimpleHTTPRequestHandler


    os.chdir(krona_folder)


    httpd = socketserver.TCPServer(
        ("localhost", krona_port),
        handler
    )


    threading.Thread(
        target=httpd.serve_forever,
        daemon=True
    ).start()


    krona_url = (
        f"http://localhost:{krona_port}/{krona_html_file.name}"
    )


    krona_url
    return (krona_url,)


@app.cell
def _(krona_html_file, krona_url, mo):
    mo.md(f"""
    🔗 **Open Krona chart**

    [{krona_html_file.name}]({krona_url})
    """)
    return


@app.cell
def _(krona_dir):
    # --------------------------------------------------------
    # Check Krona HTML files
    # --------------------------------------------------------

    for html_file in krona_dir.glob("*.html"):
        print(html_file)
    return


@app.cell
def _():
    # --------------------------------------------------------
    # Merge Krona input files
    # --------------------------------------------------------

    from collections import defaultdict


    def merge_krona_inputs(
        input_files,
        output_file
    ):

        merged = defaultdict(int)

        for input_path in input_files:

            with open(input_path, "r") as input_handle:

                for line in input_handle:

                    parts = line.rstrip("\n").split("\t")

                    if len(parts) < 2:
                        continue

                    count = int(parts[0])

                    taxonomy = tuple(parts[1:])

                    merged[taxonomy] += count


        with open(output_file, "w") as output_handle:

            for taxonomy, count in merged.items():

                if count == 0:
                    continue

                output_handle.write(
                    str(count)
                    + "\t"
                    + "\t".join(taxonomy)
                    + "\n"
                )

        return output_file
    return (merge_krona_inputs,)


@app.cell
def _():
    # --------------------------------------------------------
    # Define sample list for Krona merge
    # --------------------------------------------------------

    sample_list = [
        "D1",
        "D2",
        "D3",
        "G1",
        "G2",
        "G3",
        "L1",
        "L2",
        "L3"
    ]

    sample_list
    return (sample_list,)


@app.cell
def _(sample_list):
    # Debug sample list

    print(sample_list)
    return


@app.cell
def _(mo, sample_list):
    sample_merge_selector = mo.ui.multiselect(
        options=sample_list,
        label="Select samples to merge"
    )

    sample_merge_selector
    return (sample_merge_selector,)


@app.cell
def _(krona_dir, merge_krona_inputs, sample_merge_selector):
    # --------------------------------------------------------
    # Create merged Krona input from selected samples
    # --------------------------------------------------------

    merged_krona_input = None

    selected_samples = sample_merge_selector.value

    if selected_samples:

        input_files = [
            krona_dir / f"{s}_krona_input.txt"
            for s in selected_samples
        ]

        merged_krona_input = (
            krona_dir /
            "merged_krona_input.txt"
        )

        merge_krona_inputs(
            input_files,
            merged_krona_input
        )

    merged_krona_input
    return (merged_krona_input,)


@app.cell
def _(merged_krona_input):
    # --------------------------------------------------------
    # Check merged Krona input
    # --------------------------------------------------------

    if merged_krona_input is not None:

        print("Merged file:")
        print(merged_krona_input)

        print("\nExists:")
        print(merged_krona_input.exists())

        with open(merged_krona_input, "r") as krona_handle:

            for i in range(5):
                print(krona_handle.readline().strip())

    else:

        print("No merged Krona input")
    return


@app.cell
def _(subprocess):
    # --------------------------------------------------------
    # Krona HTML generator function
    # --------------------------------------------------------

    def generate_krona_html(
        input_file,
        output_file
    ):

        krona_command = [
            "ktImportText",
            str(input_file),
            "-o",
            str(output_file)
        ]

        krona_process = subprocess.run(
            krona_command,
            capture_output=True,
            text=True
        )

        return krona_process
    return (generate_krona_html,)


@app.cell
def _(generate_krona_html, merged_krona_input, merged_krona_output):
    # --------------------------------------------------------
    # Generate merged Krona HTML
    # --------------------------------------------------------

    if merged_krona_input is not None and merged_krona_output is not None:

        merged_krona_process = generate_krona_html(
            merged_krona_input,
            merged_krona_output
        )

        print("Return code:")
        print(merged_krona_process.returncode)

        print("\nOutput exists:")
        print(merged_krona_output.exists())

    else:

        print("Missing merged input or output")
    return


@app.cell
def _(merged_krona_output):
    print(merged_krona_output)
    return


@app.cell
def _(krona_dir):
    # --------------------------------------------------------
    # Define merged Krona output path
    # --------------------------------------------------------

    merged_krona_output = (
        krona_dir /
        "merged_krona.html"
    )

    merged_krona_output
    return (merged_krona_output,)


@app.cell
def _(merged_krona_output):
    # --------------------------------------------------------
    # Open Krona chart
    # --------------------------------------------------------

    def open_krona(file):

        import webbrowser

        webbrowser.open(
            file.as_uri()
        )


    open_krona(merged_krona_output)
    return


@app.cell
def _(merged_krona_input, merged_krona_output):
    # --------------------------------------------------------
    # Debug merged Krona generation
    # --------------------------------------------------------

    print("Input:")
    print(merged_krona_input)

    print("\nOutput:")
    print(merged_krona_output)

    print("\nInput exists:")
    print(merged_krona_input.exists())

    print("\nOutput exists before:")
    print(merged_krona_output.exists())
    return


@app.cell
def _(merged_krona_output):
    # --------------------------------------------------------
    # Check merged Krona HTML
    # --------------------------------------------------------

    merged_krona_output.exists()
    return


@app.cell
def _(krona_input):
    # --------------------------------------------------------
    # Calculate taxon abundance percentages
    # --------------------------------------------------------

    krona_analysis = krona_input.copy()

    sample_total_reads = krona_analysis["Count"].sum()

    krona_analysis["Total_%"] = (
        krona_analysis["Count"] / sample_total_reads * 100
    )

    krona_analysis.head()
    return krona_analysis, sample_total_reads


@app.cell
def _(krona_analysis, mo):
    # --------------------------------------------------------
    # Species selector
    # --------------------------------------------------------

    species_list = (
        krona_analysis["Species"]
        .dropna()
        .unique()
        .tolist()
    )

    species_selector = mo.ui.dropdown(
        options=species_list,
        label="Select species"
    )

    species_selector
    return (species_selector,)


@app.cell
def _(krona_analysis, pd, sample_total_reads, species_selector):
    # --------------------------------------------------------
    # Selected species contribution
    # --------------------------------------------------------

    selected_species = species_selector.value

    species_data = krona_analysis[
        krona_analysis["Species"] == selected_species
    ]

    species_reads = species_data["Count"].sum()

    species_percentage = (
        species_reads / sample_total_reads * 100
    )

    summary = pd.DataFrame(
        {
            "Metric": [
                "Species",
                "Reads",
                "% of total sample"
            ],
            "Value": [
                selected_species,
                species_reads,
                f"{species_percentage:.2f}%"
            ]
        }
    )

    summary
    return


if __name__ == "__main__":
    app.run()
