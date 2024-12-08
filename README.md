# Customized Jbrowse2 on Your Local Computer

## Authors

- **Cagin Tunc**  
  *Role:* Developer and Maintainer  
  *Email:* [cagin_tunc@berkeley.edu](mailto:cagin_tunc@berkeley.edu)  
  *GitHub:* [https://github.com/cagintunc](https://github.com/cagintunc)  

- **Justin Sung**  
  *Role:* Developer and Maintainer  
  *Email:* [john.doe@example.com](mailto:john.doe@example.com)
  *GitHub:* [https://github.com/johndoe](https://github.com/johndoe)  

## Overview

This repository contains two essential Python scripts, `db.py` and `fix_config.py`, designed to automate the setup, customization, and deployment of genome datasets for visualization and analysis using JBrowse 2. The project focuses on integrating genomic data for **SARS (Severe Acute Respiratory Syndrome)** and **MERS (Middle East Respiratory Syndrome)**, making it easier for researchers to explore and analyze these viral genomes.

### Purpose of the Project

JBrowse 2 is a robust genome browser offering interactive visualizations for genomic data. However, setting up custom datasets can be challenging, especially for large and complex viral genomes like SARS and MERS. This project addresses these challenges by automating the process of downloading, processing, and preparing the data for use in JBrowse 2.

By simplifying this workflow, researchers can focus on genomic analysis without the need for extensive technical knowledge.

### Features

- **Automated Genome and Annotation Downloads**: Retrieve genome sequences and annotation files for SARS and MERS from trusted repositories (e.g., NCBI) with ease.
- **Annotation Conversion and Processing**: Convert annotation formats (e.g., CDS to GFF) to meet JBrowse 2 requirements.
- **Compression and Indexing**: Leverage tools like `bgzip`, `tabix`, and `samtools` to prepare datasets for efficient browsing.
- **Dynamic Configuration**: Automatically update the JBrowse `config.json` file with the assemblies and tracks for SARS and MERS genomes.
- **Cross-Platform Support**: Works seamlessly on Linux-based environments, including WSL for Windows.

### Required Tools and Dependencies

To run these scripts, the following tools and Python libraries are required:

#### System Tools
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

#### Python Dependencies
1. **Biopython**: Used for parsing CDS files and converting them to GFF format.
   - Installation: `pip install biopython`
2. **gzip**: For handling gzipped files (bundled with Python's standard library).
3. **shutil**: For managing files and directories (bundled with Python's standard library).
4. **subprocess**: For running system commands (bundled with Python's standard library).

### How It Works

#### `db.py`
The `db.py` script automates the following steps:
1. **Downloading Data**: Fetch genome sequences in FASTA format and annotation files in CDS or GFF format for SARS and MERS.
2. **Annotation Conversion**: Converts CDS files to GFF format if needed.
3. **File Processing**:
   - Sorts, compresses, and indexes annotation files to meet JBrowse 2's requirements.
   - Handles both `.tbi` (Tabix) and `.csi` (Coordinate Sorted Index) indexing.
4. **Configuration Updates**: Updates the JBrowse `config.json` file to include assemblies and annotation tracks for SARS and MERS.
5. **JBrowse Integration**: Adds assemblies and tracks to the JBrowse setup using the CLI.

#### `fix_config.py`
The `fix_config.py` script ensures the paths in the JBrowse configuration file (`config.json`) are relative instead of absolute. This makes the setup portable and easier to share across different systems or deploy to platforms like AWS or GitHub Pages.

### Why Are These Tools Necessary?

1. **`samtools`**: Indexes the genome FASTA files to allow JBrowse to retrieve sequences efficiently.
2. **`bgzip` and `tabix`**: Compress and index annotation files for interactive browsing in JBrowse.
3. **Biopython**: Automates complex tasks like parsing CDS files and converting them to GFF format.
4. **JBrowse CLI**: Adds assemblies and tracks to JBrowse, ensuring they are displayed correctly.

### Use Cases

1. **Viral Genome Analysis**: Researchers can load SARS and MERS datasets into JBrowse and explore them interactively.
2. **Dataset Portability**: Easily share or deploy JBrowse setups with collaborators or on web platforms.
3. **Extensibility**: The scripts can be extended to support other viral datasets by updating the genome and annotation URLs in the code.

### Why Use This Project?

SARS and MERS are significant public health concerns, and their genomic analysis can provide critical insights into viral behavior, mutations, and therapeutic targets. However, preparing these datasets for visualization can be challenging due to their size and complexity. This project automates the entire pipeline, from downloading and processing the data to configuring JBrowse 2, saving time and reducing errors. Researchers and bioinformaticians can now focus on analysis and discovery rather than tedious data preparation tasks.

---

## `db.py`

### Purpose

The `db.py` script automates tasks such as:
- Downloading genome and annotation data.
- Processing and indexing data for JBrowse2.
- Configuring JBrowse2 with assemblies and tracks.

### How to Use
1. Install Dependencies:
   
```bash
pip install biopython sudo apt-get install tabix
```

2. Follow the prompts to clean directories or retain existing configurations.
---

## `fix_config.py`

### Purpose

The `fix_config.py` script adjusts absolute paths in `config.json` to make it portable.

### How to Use
1. Place `fix_config.py` in the same directory as `config.json`.
2. Run:
```bash
python3 fix_config.py
```
---

## Requirements

- Python 3.x
- Biopython
- bgzip and tabix
- JBrowse2

---

## Example Workflow

1. Clone the repository.
2. Run `db.py`:
```bash
python3 db.py
```
4. Adjust paths with `fix_config.py`:
```bash
python3 fix_config.py
```
5. Start a local server:
```bash
python3 -m http.server 8000
```
Open your browser at `http://localhost:8000`.

---

## Troubleshooting

- Ensure all dependencies are installed.
- Check that files are correctly indexed.
- Use CSI indexing for large GFF files when needed.

---

## License

This project is licensed under the MIT License.




