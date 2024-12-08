import os
import subprocess
import shutil
import json
import gzip

CURRENT_DIR = os.path.abspath(os.getcwd())
JBROWSE_DIR = os.path.join(CURRENT_DIR, "jbrowse2")


#Genomes:
GENOME_LINKS = {
    "mers": {
        "genome": "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/901/155/GCF_000901155.1_ViralProj183710/GCF_000901155.1_ViralProj183710_genomic.fna.gz",
        "annotations": "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/901/155/GCF_000901155.1_ViralProj183710/GCF_000901155.1_ViralProj183710_genomic.gff.gz",
        "name":("MERS", "mers"),
        "cds_path": "mers.cds",
        "gff_path": "mers_genes.gff"
    },
    "sars_cov_2": {
        "genome": "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/858/895/GCF_009858895.2_ASM985889v3/GCF_009858895.2_ASM985889v3_genomic.fna.gz",
        "annotations": "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/858/895/GCF_009858895.2_ASM985889v3/GCF_009858895.2_ASM985889v3_genomic.gff.gz",
        "name":("SARS Covid 2", "sars_cov_2"),
        "cds_path": "sars_cov.cds",
        "gff_path": "sars_genes.gff"
    }
}


# Helper Functions
def run_command(command, error_message):
    """Run a shell command and handle errors."""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"{error_message}: {e}")
        exit(1)


def install_dependencies():
    """Ensure all dependencies are installed."""
    dependencies = ["curl", "unzip", "bgzip", "jbrowse"]
    print("Checking dependencies for the installation script...")

    for dep in dependencies:
        if shutil.which(dep):
            print(f"Checking availability of {dep}... OK!")
        else:
            print(f"Dependency {dep} not found. Please install it before proceeding.")
            exit(1)
    print("All dependencies are available!")


def setup_jbrowse():
    """Set up JBrowse in the specified directory."""
    if os.path.exists(JBROWSE_DIR):
        print("JBrowse has already been downloaded!")
        return

    run_command(
        f'jbrowse create "{JBROWSE_DIR}" --force',
        "Error initializing JBrowse",
    )

def create_config_file():
    """Manually create a minimal config.json if not generated."""
    config_path = os.path.join(JBROWSE_DIR, "config.json")
    if not os.path.exists(config_path):
        print("Creating a minimal config.json...")
        config_template = {
            "assemblies": [],
            "tracks": [],
            "configuration": {},
            "connections": [],
            "defaultSession": {"name": "New Session"},
        }
        with open(config_path, "w") as config_file:
            json.dump(config_template, config_file, indent=2)
        print("Minimal config.json created successfully.")

def load_genome_into_jbrowse(virus):
    """Load the genome into JBrowse."""
    genome_path = os.path.join(JBROWSE_DIR, f"{virus['name'][1]}.fa")
    config_path = os.path.join(JBROWSE_DIR, "config.json")

    print(f"Adding assembly for {virus['name'][0]}...")

    if not os.path.exists(genome_path):
        print(f"Error: Genome file {genome_path} does not exist. Cannot add assembly.")
        return

    # Check if assembly is already in config.json
    if os.path.exists(config_path):
        with open(config_path, "r") as file:
            config = json.load(file)

        if any(assembly["name"] == virus["name"][1] for assembly in config.get("assemblies", [])):
            print(f"Assembly for {virus['name'][0]} is already present in config.json.")
            return

    # Add assembly using JBrowse CLI
    run_command(
        f'jbrowse add-assembly "{genome_path}" --out "{JBROWSE_DIR}" --load inPlace --force',
        f"Error adding assembly for {virus['name'][0]}",
    )
    print(f"Assembly for {virus['name'][0]} added successfully.")



def download_process_genome(virus):
    """Download and process the virus genome."""
    genome_path = os.path.join(JBROWSE_DIR, f"{virus["name"][1]}.fa")
    if os.path.exists(genome_path):
        print(f"{virus['name'][0]} has been already download!")
        return
    else:
        print(f"Downloading genome to {genome_path}...")
        run_command(
            f'wget \"{virus["genome"]}\" -O "{genome_path}.gz"',
            "Error downloading genome",
        )
        run_command(f'gunzip -f "{genome_path}.gz"', "Error unzipping genome")
        run_command(f'samtools faidx "{genome_path}"', "Error indexing genome")
        print(f"{virus["name"][0]} genome downloaded and processed successfully.")


def update_config_file(virus):
    """Update the JBrowse config.json file with new genome and annotation track info."""
    config_path = os.path.join(JBROWSE_DIR, "config.json")

    # Load the current config
    if not os.path.exists(config_path):
        print("Error: config.json does not exist. Ensure JBrowse is initialized.")
        return

    with open(config_path, "r") as file:
        config = json.load(file)

    # Add assembly if not already present
    assembly_name = virus["name"][1]
    genome_path = f"{assembly_name}.fa"

    if not any(assembly["name"] == assembly_name for assembly in config.get("assemblies", [])):
        config.setdefault("assemblies", []).append({
            "name": assembly_name,
            "sequence": {
                "type": "ReferenceSequenceTrack",
                "trackId": f"{assembly_name}-ReferenceSequenceTrack",
                "adapter": {
                    "type": "IndexedFastaAdapter",
                    "fastaLocation": {"uri": genome_path, "locationType": "UriLocation"},
                    "faiLocation": {"uri": f"{genome_path}.fai", "locationType": "UriLocation"},
                },
            },
        })

    # Write the updated config back to the file
    with open(config_path, "w") as file:
        json.dump(config, file, indent=2)

    print(f"Updated config.json with {virus['name'][0]} genome and annotation track.")


def convert_fasta_to_gff(fasta_path, gff_path):
    """Convert a FASTA file to a pseudo-GFF file."""
    if os.path.exists(gff_path):
        return
    
    with open(fasta_path, "r") as fasta, open(gff_path, "w") as gff:
        gff.write("##gff-version 3\n")  # Add GFF header
        seq_id = None
        sequence = []

        for line in fasta:
            line = line.strip()
            if line.startswith(">"):  # Header line
                if seq_id:  # Write the previous sequence as GFF
                    gff.write(
                        f"{seq_id}\t.\tgene\t1\t{len(''.join(sequence))}\t.\t+\t.\tID={seq_id}\n"
                    )
                seq_id = line[1:].split("|")[1]  # Extract the ID from the header
                sequence = []
            else:
                sequence.append(line)

        # Write the last sequence
        if seq_id:
            gff.write(
                f"{seq_id}\t.\tgene\t1\t{len(''.join(sequence))}\t.\t+\t.\tID={seq_id}\n"
            )


def download_and_process_annotations(virus):
    """Download, process, and prepare virus annotations."""
    gff_path = os.path.join(JBROWSE_DIR, virus["gff_path"])
    gz_path = f"{gff_path}.gz"

    # Step 1: Download the file
    print("Downloading annotations...")
    run_command(
        f'wget "{virus["annotations"]}" -O "{gz_path}"',
        "Error downloading annotations",
    )

    # Step 2: Check if the file is gzipped
    print("Checking if the downloaded file is gzipped...")
    with gzip.open(gz_path, "rt") as gz_file:
        first_line = gz_file.readline().strip()
        if not first_line.startswith("##gff-version"):
            print("Error: The downloaded file is not in valid GFF format!")
            exit(1)
        else:
            print(f"{gz_path} is a valid gzipped GFF file. Proceeding with decompression.")

    # Step 3: Decompress the GFF file
    print("Decompressing GFF file...")
    run_command(f'gunzip -f "{gz_path}"', "Error decompressing GFF file")

    # Step 4: Sort the GFF file
    print("Sorting the GFF file...")
    sorted_gff_path = f"{gff_path}.sorted"
    try:
        subprocess.run(
            f'sort -k1,1 -k4,4n "{gff_path}" > "{sorted_gff_path}"',
            shell=True,
            check=True
        )
        # Replace the original file with the sorted one
        os.rename(sorted_gff_path, gff_path)
        print("GFF file sorted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error sorting GFF file: {e}")
        exit(1)

    # Step 5: Compress the GFF file using BGZF format
    print("Compressing GFF file with BGZF...")
    run_command(f'bgzip -f "{gff_path}"', "Error compressing GFF file")

    # Step 6: Index the compressed GFF file
    print("Indexing compressed GFF file...")
    run_command(f'tabix -p gff "{gz_path}"', "Error indexing GFF file")

    print(f"{virus['name'][0]} genome annotations downloaded and processed successfully.")



def add_annotation_track(virus):
    """Add the annotation track to JBrowse."""
    gff_path = os.path.join(JBROWSE_DIR, virus["gff_path"])
    gz_path = f"{gff_path}.gz"

    print("Ensuring the .gz file is present before adding the track...")
    if not os.path.exists(gz_path):
        print(f"{gz_path} is missing. Recreating it...")
        if os.path.exists(gff_path):
            run_command(f'bgzip -f "{gff_path}"', "Error compressing GFF to .gz")
            print(f"Recreated {gz_path} successfully.")
        else:
            print(f"Error: {gff_path} does not exist. Cannot create {gz_path}.")
            exit(1)

    # Add the annotation track using --assemblyNames
    print("Adding annotation track using inPlace load method...")
    try:
        run_command(
            f'jbrowse add-track "{gz_path}" --out "{JBROWSE_DIR}" --assemblyNames {virus["name"][1]} --load inPlace --force',
            "Error adding annotation track",
        )
        print(f"Annotation track added successfully for {virus['name'][0]}.")
    except Exception as e:
        print(f"Failed to add annotation track for {virus['name'][0]}: {e}")
        print("Retrying with recreated .gz file...")
        if os.path.exists(gff_path):
            run_command(f'bgzip -f "{gff_path}"', "Error compressing GFF to .gz during retry")
            run_command(
                f'jbrowse add-track "{gz_path}" --out "{JBROWSE_DIR}" --assemblyNames {virus["name"][1]} --load inPlace --force',
                "Error adding annotation track during retry",
            )
            print(f"Annotation track added successfully after retry for {virus['name'][0]}.")
        else:
            print(f"Error: {gff_path} is missing. Retry failed.")
            exit(1)


def convert_fasta_to_gff(cds_path, gff_path):
    """
    Convert a FASTA file containing CDS information to a pseudo-GFF3 format.
    """
    if os.path.exists(gff_path):
        print(f"GFF file {gff_path} already exists. Skipping conversion.")
        return

    print(f"Converting CDS file {cds_path} to GFF3 format...")
    with open(cds_path, "r") as fasta, open(gff_path, "w") as gff:
        gff.write("##gff-version 3\n")  # Add GFF header
        seq_id = None
        sequence = []

        for line in fasta:
            line = line.strip()
            if line.startswith(">"):  # Header line
                if seq_id:  # Write the previous sequence as GFF
                    gff.write(
                        f"{seq_id}\t.\tgene\t1\t{len(''.join(sequence))}\t.\t+\t.\tID={seq_id}\n"
                    )
                seq_id = line[1:].split("|")[0]  # Extract the ID from the header
                sequence = []
            else:
                sequence.append(line)

        # Write the last sequence
        if seq_id:
            gff.write(
                f"{seq_id}\t.\tgene\t1\t{len(''.join(sequence))}\t.\t+\t.\tID={seq_id}\n"
            )

    print(f"CDS file {cds_path} successfully converted to GFF3 format at {gff_path}.")


def index_for_gene_search():
    """Index the genome and annotations for gene search in JBrowse."""
    print("Indexing genome for gene search...")
    run_command(
        f'jbrowse text-index --out "{JBROWSE_DIR}"',
        "Error indexing genome for gene search",
    )
    print("Gene search indexing completed successfully.")


def clean_directories():
    """Delete directories and files created by the script."""
    try:
        if os.path.exists(JBROWSE_DIR):
            print(f"Removing existing directory: {JBROWSE_DIR}")
            shutil.rmtree(JBROWSE_DIR)
        print("Cleanup complete.")
    except PermissionError as e:
        print(f"Permission error: {e}. Try running the script with elevated privileges.")


def maf_to_paf(maf_file, paf_file):
    with open(maf_file, 'r') as maf, open(paf_file, 'w') as paf:
        query_name, query_start, query_end = None, None, None
        target_name, target_start, target_end = None, None, None
        query_len, target_len = None, None
        strand = '+'

        for line in maf:
            if line.startswith('s'):  
                parts = line.split()
                if query_name is None:  
                    query_name = parts[1]
                    query_start = int(parts[2])
                    query_len = int(parts[5])
                    query_end = query_start + int(parts[3])
                else:  
                    target_name = parts[1]
                    target_start = int(parts[2])
                    target_len = int(parts[5])
                    target_end = target_start + int(parts[3])

                    paf.write(f"{query_name}\t{query_len}\t{query_start}\t{query_end}\t{strand}\t"
                              f"{target_name}\t{target_len}\t{target_start}\t{target_end}\t"
                              f"{query_end - query_start}\t{query_end - query_start}\t60\n")

                    query_name, query_start, query_end = None, None, None


def create_paf_file(vir1, vir2, output_maf, db_name="mers_db", threads=4):
    try:
        print("Installing last-align if not present...")
        subprocess.run(["sudo", "apt", "install", "-y", "last-align"], check=True)
        
        print(f"Creating LAST database: {db_name} from {vir1}...")
        subprocess.run(["lastdb", db_name, vir1], check=True)
        
        print(f"Running alignment: {vir1} against {vir2}...")
        with open(output_maf, "w") as maf_file:
            subprocess.run(["lastal", f"-m100", f"-E0.05", f"-P{threads}", db_name, vir2], stdout=maf_file, check=True)
        
        print(f"Alignment complete. Output written to {output_maf}")
        paf_file = "jbrowse2/mers_sars.paf"
        maf_to_paf(output_maf, paf_file)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing the command: {e}")
    except FileNotFoundError as e:
        print(f"Required tool not found. Please ensure 'last-align' is installed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        


if __name__ == "__main__":
    # Ask user if they want to clean directories before proceeding
    clean_choice = input("Do you want to clean existing directories before running? (yes/no): ").strip().lower()
    if clean_choice in ["yes", "y"]:
        clean_directories()
    virs = ["sars_cov_2", "mers"]
    for vir in virs:
        virus = GENOME_LINKS[vir]
        install_dependencies()
        setup_jbrowse()
        create_config_file()
        download_process_genome(virus)
        load_genome_into_jbrowse(virus)
        download_and_process_annotations(virus)
        add_annotation_track(virus)
        update_config_file(virus)

    create_paf_file("jbrowse2/mers.fa", "jbrowse2/sars_cov_2.fa", "jbrowse2/sars_mers.maf", db_name="mers_db")
    print("All tasks completed successfully!")


