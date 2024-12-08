# Customized Jbrowse2 on Your Local Computer

# Table of contents
1. [Authors](#authors)
2. [Overview](#overview)
    1. [Purpose of the Project](#purpose)
    2. [Features of the Project](#features)
3. [Required Tools and Dependencies](#tools_required)
    1. [System Tools](#system_tools)
    2. [Python Dependencies](#python_dependencies)
4. [Compartments](#compartments)
    1. [Explanation of dependencies.sh](#dependencies_exp)
    2. [Explanation of db.py](#db_exp)
    3. [Explanation of fix_config.py](#fix_config_exp)
6. [Use Cases](#use_cases)
7. [Why Use This Project?](#reason_to_use)
8. [Example Workflow](#workflow)
9. [Troubleshooting](#traubleshooting)
10. [License](#license)

---

## Authors <a name="authors"></a>

- **Cagin Tunc**  
  *Role:* Developer and Maintainer  
  *Email:* [cagin_tunc@berkeley.edu](mailto:cagin_tunc@berkeley.edu)  
  *GitHub:* [https://github.com/cagintunc](https://github.com/cagintunc)  

- **Justin Sung**  
  *Role:* Developer and Maintainer  
  *Email:* [john.doe@example.com](mailto:john.doe@example.com)
  *GitHub:* [https://github.com/johndoe](https://github.com/johndoe)  

## Overview <a name="overview"></a>

This repository contains two essential Python scripts, `db.py` and `fix_config.py` as well as one bash script, `dependencies.sh`, designed to automate the setup, customization, and deployment of genome datasets for visualization and analysis using JBrowse 2. The project focuses on integrating genomic data for **SARS (Severe Acute Respiratory Syndrome)** and **MERS (Middle East Respiratory Syndrome)**, making it easier for researchers to explore and analyze these viral genomes.

### Purpose of the Project <a name="purpose"></a>

JBrowse 2 is a robust genome browser offering interactive visualizations for genomic data. However, setting up custom datasets can be challenging, especially for large and complex viral genomes like SARS and MERS. This project addresses these challenges by automating the process of downloading, processing, and preparing the data for use in JBrowse 2.

By simplifying this workflow, researchers can focus on genomic analysis without the need for extensive technical knowledge.

### Features <a name="features"></a>

- **Automated Genome and Annotation Downloads**: Retrieve genome sequences and annotation files for SARS and MERS from trusted repositories (e.g., NCBI) with ease.
- **Annotation Conversion and Processing**: Convert annotation formats (e.g., CDS to GFF) to meet JBrowse 2 requirements.
- **Compression and Indexing**: Leverage tools like `bgzip`, `tabix`, and `samtools` to prepare datasets for efficient browsing.
- **Customization via Unique Plugins**: Utilize customized plugins to make the process easier for the users.
- **Dynamic Configuration**: Automatically update the JBrowse `config.json` file with the assemblies and tracks for SARS and MERS genomes.
- **Cross-Platform Support**: Works seamlessly on Linux-based environments, including WSL for Windows.

## Required Tools and Dependencies <a name="tools_required"></a>

To run these scripts, the following tools and Python libraries are required:

### System Tools: Note that they are directly installed by running the `dependencies.sh` bash code. There is no need to install them manually. <a name="system_tools"></a>
1. **`samtools`**: For indexing genome files in FASTA format (`.fai`).
   - Installation: `sudo apt-get install samtools`
2. **`bgzip`**: For compressing annotation files in BGZF format.
   - Installation: `sudo apt-get install tabix` (comes bundled with `bgzip`)
3. **`tabix`**: For indexing compressed annotation files in `.tbi` or `.csi` format.
   - Installation: `sudo apt-get install tabix`
4. **`curl`**: For downloading files from URLs.
   - Installation: `sudo apt-get install curl`
5. **`unzip`**: For extracting the JBrowse web application files.
   - Installation: `sudo apt-get install unzip`
6. **`jbrowse`**: The CLI for JBrowse 2 to add assemblies and tracks.
   - Installation: Follow [JBrowse CLI Installation Guide](https://jbrowse.org/cli/).

### Python Dependencies - For further information(versions of the libraries), please look the requirements. <a name="python_dependencies"></a>
1. **Biopython**: Used for parsing CDS files and converting them to GFF format.
   - Installation: `pip install biopython`
2. **gzip**: For handling gzipped files (bundled with Python's standard library).
3. **shutil**: For managing files and directories (bundled with Python's standard library).
4. **subprocess**: For running system commands (bundled with Python's standard library).
5. **json**: For reading and writing JSON data, often used in configuration files and structured data management (bundled with Python's standard library).
6. **os**: Provides functionalities for interacting with the operating system, such as file path manipulations and environment management (bundled with Python's standard library).

## Compartments <a name="compartments"></a>

### Explanation of `dependencies.sh` <a name="dependencies_exp"></a>

The `dependencies.sh` script is designed to automate the installation and configuration of essential bioinformatics tools on an Ubuntu-based system. It simplifies the process of setting up dependencies required for working with JBrowse2, HTSlib, and related utilities.

---

#### **What the Script Does**

1. **Updates the System**  
   The script ensures that the package manager is up-to-date, allowing it to fetch and install the latest versions of required software.

2. **Installs Necessary Development Tools**  
   It installs tools and libraries essential for building software, handling compressed files, and managing secure network connections. These are foundational for bioinformatics workflows.

3. **Installs JBrowse CLI**  
   The script installs the JBrowse Command Line Interface (CLI), a powerful tool for managing JBrowse2 instances, which is widely used for genomic data visualization.

4. **Downloads and Builds HTSlib**  
   HTSlib, a core library for working with high-throughput sequencing data, is downloaded, configured, and compiled. This ensures compatibility with the system and enables operations on genomic data.

5. **Installs Samtools**  
   The script installs Samtools, a critical utility for processing and analyzing sequencing alignment data.

6. **Performs a Final System Update**  
   A final update ensures that all installed software is current and functioning optimally.


#### Why Are These Tools Necessary?

1. **`samtools`**: Indexes the genome FASTA files to allow JBrowse to retrieve sequences efficiently.
2. **`bgzip` and `tabix`**: Compress and index annotation files for interactive browsing in JBrowse.
3. **Biopython**: Automates complex tasks like parsing CDS files and converting them to GFF format.
4. **JBrowse CLI**: Adds assemblies and tracks to JBrowse, ensuring they are displayed correctly.

---
#### **Purpose of the Script**
This script reduces manual effort by automating the setup process, ensuring consistency, and minimizing errors during the installation of bioinformatics tools. It is particularly useful for users who need a streamlined environment for genomic data analysis.


### Explanation of `db.py` <a name="db_exp"></a>
The `db.py` script automates the following steps:
1. **Downloading Data**: Fetch genome sequences in FASTA format and annotation files in CDS or GFF format for SARS and MERS.
2. **Annotation Conversion**: Converts CDS files to GFF format if needed.
3. **File Processing**:
   - Sorts, compresses, and indexes annotation files to meet JBrowse 2's requirements.
   - Handles both `.tbi` (Tabix) and `.csi` (Coordinate Sorted Index) indexing.
4. **Configuration Updates**: Updates the JBrowse `config.json` file to include assemblies and annotation tracks for SARS and MERS.
5. **JBrowse Integration**: Adds assemblies and tracks to the JBrowse setup using the CLI.
6. **Easily Extendable Genome Database with `db.py`**

The `db.py` file is designed to make it incredibly easy to add new genomes to your local database. The only requirement is to add a new key to the `GENOME_LINKS` dictionary. Each key represents a genome name, and the corresponding value is a dictionary containing all the necessary information for that genome.

6.1. **Current `GENOME_LINKS` Structure**

Here’s an example of the `GENOME_LINKS` dictionary in the code:

```python
GENOME_LINKS = {
    "mers": {
        "genome": "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/901/155/GCF_000901155.1_ViralProj183710/GCF_000901155.1_ViralProj183710_genomic.fna.gz",
        "annotations": "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/901/155/GCF_000901155.1_ViralProj183710/GCF_000901155.1_ViralProj183710_genomic.gff.gz",
        "name": ("MERS", "mers"),
        "cds_path": "mers.cds",
        "gff_path": "mers_genes.gff"
    },
    "sars_cov_2": {
        "genome": "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/858/895/GCF_009858895.2_ASM985889v3/GCF_009858895.2_ASM985889v3_genomic.fna.gz",
        "annotations": "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/858/895/GCF_009858895.2_ASM985889v3/GCF_009858895.2_ASM985889v3_genomic.gff.gz",
        "name": ("SARS Covid 2", "sars_cov_2"),
        "cds_path": "sars_cov.cds",
        "gff_path": "sars_genes.gff"
    }
}
```
6.2. **Adding a New Genome**
To add a new genome, simply append a new key-value pair to the GENOME_LINKS dictionary. Here's an example of adding a new genome, ebola:

```python
GENOME_LINKS["ebola"] = {
    "genome": "https://example_path/GCF_ebola_genomic.fna.gz",
    "annotations": "https://example_path/GCF_ebola_genomic.gff.gz",
    "name": ("Ebola", "ebola"),
    "cds_path": "ebola.cds",
    "gff_path": "ebola_genes.gff"
}
```

6.3. **Required Fields for Each Genome**
- **genome**: URL to the genomic .fna.gz file.
- **annotations**: URL to the annotation .gff.gz file.
- **name**: A tuple containing the full genome name and its short identifier.
- **cds_path**: The local path for the coding sequences (CDS) file.
- **gff_path**: The local path for the GFF (gene annotation) file.


### Explanation of `fix_config.py` <a name="fix_config_exp"></a>
The `fix_config.py` script ensures the paths in the JBrowse configuration file (`config.json`) are relative instead of absolute. This makes the setup portable and easier to share across different systems or deploy to platforms like AWS or GitHub Pages.

## Use Cases <a name="use_cases"></a>

1. **Viral Genome Analysis**: Researchers can load SARS and MERS datasets into JBrowse and explore them interactively.
2. **Dataset Portability**: Easily share or deploy JBrowse setups with collaborators or on web platforms.
3. **Extensibility**: The scripts can be extended to support other viral datasets by updating the genome and annotation URLs in the code.

## Why Use This Project? <a name="reason_to_use"></a>

SARS and MERS are significant public health concerns, and their genomic analysis can provide critical insights into viral behavior, mutations, and therapeutic targets. However, preparing these datasets for visualization can be challenging due to their size and complexity. This project automates the entire pipeline, from downloading and processing the data to configuring JBrowse 2, saving time and reducing errors. Researchers and bioinformaticians can now focus on analysis and discovery rather than tedious data preparation tasks.

---

## Example Workflow <a name="workflow"></a>

1. **Clone the repository by running the following command from your terminal**:
```bash
git clone https://github.com/cagintunc/331_final_project.git
```
2. **Run `dependencies.sh` by using the following command**:
```bash
./dependencies.sh
```
3. **Run `db.py`**:
```bash
python3 db.py
```
4. **Adjust paths with `fix_config.py`**:
```bash
python3 fix_config.py
```
5. **Start a local server**:
```bash
python3 -m http.server 8000
```
Open your browser at `http://localhost:8000/jbrowse2`.

---

## Troubleshooting <a name="troubleshooting"></a>

- Ensure all dependencies are installed.
- Check that files are correctly indexed.
- Use CSI indexing for large GFF files when needed.

---

## License <a name="license"></a>

This project is licensed under the MIT License.




