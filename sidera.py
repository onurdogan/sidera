import marimo

__generated_with = "0.17.6"
app = marimo.App(width="medium")


@app.cell
def imports():
    # Imports

    import marimo as mo
    from pathlib import Path
    import shutil
    return Path, mo


@app.cell
def welcome(mo):
    mo.md("""
    # 🌿 Sidera

    *"Nel mezzo del cammin di nostra vita..."*

    Welcome, traveler.

    Before entering the 🔥 Inferno 🔥, you must choose the path where your project will be born.

    Create a new Sidera project or open an existing one.
    """)
    return


@app.cell
def text_project_name(mo):
    # Enter your project name below
    project_name = mo.ui.text(
        label="Project name",
        placeholder="e.g. Sampling_location_Session/Month_Year"
    )

    project_name
    return (project_name,)


@app.cell
def _(project_name):
    project_name.value
    return


@app.cell
def new_project_path(Path, project_name):
    # 📁 Define new project path

    if project_name.value:

        new_project_path = (
            Path.cwd() /
            project_name.value
        )

    else:

        new_project_path = None


    new_project_path
    return (new_project_path,)


@app.cell
def select_project_path(Path, mo):
    # Select project path from available Sidera projects

    # Select existing Sidera project path

    path_root = Path.cwd()

    available_paths = [
        str(p) # Convert the Path object into a string path
        for p in path_root.iterdir() # Loop through every item inside the root directory
        if p.is_dir() # Keep only directories (ignore files)
        and (p / "00_selva_oscura").exists()
    ]

    path_selector = mo.ui.dropdown(
        options=available_paths,
        label="Select Sidera project path"
    )

    path_selector
    return (path_selector,)


@app.cell
def _(path_selector):
    # 🔎 Check selected project path

    path_selector.value
    return


@app.cell
def project_selector(Path, mo):
    # 📂 Define the root directory where Sidera projects are stored

    #create avariable called projects_root that will store the location where we search for Sidera projects
    projects_root = Path.cwd()   # Get the current working directory (cwd) as the project root location

    # 🌿 Search existing Sidera projects in the current directory

    available_projects = [
        p.name                                      # Store only the project folder name (not the full path)
        for p in projects_root.iterdir()            # Loop through every item inside the projects root directory
        if p.is_dir()                                # Keep only directories, ignore files
        and (p / "00_selva_oscura").exists()         # Identify valid Sidera projects by checking the Selva Oscura folder
    ]

    project_selector = mo.ui.dropdown(
        options=available_projects,
        label="Select Sidera project"
    )

    project_selector
    return (project_selector,)


@app.cell
def _(project_selector):
    project_selector.value
    return


@app.cell
def project_creator(mo, new_project_path, project_name):
    # 🌱 Create Sidera project architecture

    if project_name.value:

        folders = [

            # 🌲 Selva Oscura
            "00_selva_oscura/settings",
            "00_selva_oscura/raw_data",
            "00_selva_oscura/metadata",


            # 🔥 Inferno

            "01_inferno/canto_01_demultiplexing",
        
            "01_inferno/canto_02_single_end",
      
            "01_inferno/canto_03_paired_end_merging",
      
            "01_inferno/canto_04_primer_trimming",
      
            "01_inferno/canto_05_quality_filtering",
      
            "01_inferno/canto_06_dereplication",
      
            "01_inferno/canto_07_clustering",
      
            "01_inferno/canto_08_denoising",
      
            "01_inferno/canto_09_chimera_removal",
      
            "01_inferno/canto_10_taxonomic_assignment",


            # ⚗️ Purgatory
            "02_purgatory",


            # 🌈 Paradiso
            "03_paradiso",


            # 🏗 Core
            "core",
            "database",
            "data",
            "logs",
            "reports",
            "krona_dashboard",

        ]


        # Create all folders

        for folder in folders:

            (new_project_path / folder).mkdir(
                parents=True,
                exist_ok=True
            )


        # Create standard project files

        for file in [
            "README.md",
            "LICENSE",
            "requirements.txt",
            "environment.yml",
        ]:

            (new_project_path / file).touch(
                exist_ok=True
            )


        mo.md(
        f"""
        # 🌱 Sidera project created

        Project:

        `{new_project_path}`


        Structure created:

        ✓ Selva Oscura  
        ✓ Inferno (Canto 01 → 10)  
        ✓ Purgatory  
        ✓ Paradiso  
        ✓ Core infrastructure  
        """
        )


    else:

        mo.md(
        """
        ⚠️ Enter a project name first.
        """
        )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
