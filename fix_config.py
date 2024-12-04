import json
import os

def fix_config_paths(config_path, base_dir):
    """Rewrite paths in config.json to ensure correct file extensions and relative paths."""
    if not os.path.exists(config_path):
        print("Error: config.json not found!")
        return

    with open(config_path, "r") as file:
        config = json.load(file)

    # Update assembly paths
    for assembly in config.get("assemblies", []):
        fasta = assembly["sequence"]["adapter"]["fastaLocation"]["uri"]
        fai = assembly["sequence"]["adapter"]["faiLocation"]["uri"]
        assembly["sequence"]["adapter"]["fastaLocation"]["uri"] = os.path.relpath(fasta, base_dir)
        assembly["sequence"]["adapter"]["faiLocation"]["uri"] = os.path.relpath(fai, base_dir)

    # Update track paths
    for track in config.get("tracks", []):
        gff_gz_location = track["adapter"]["gffGzLocation"]["uri"]
        index_location = track["adapter"]["index"]["location"]["uri"]

        # Ensure the .gz extension is present
        if not gff_gz_location.endswith(".gz"):
            track["adapter"]["gffGzLocation"]["uri"] = f"{gff_gz_location}.gz"

        if not index_location.endswith(".gz.tbi"):
            track["adapter"]["index"]["location"]["uri"] = f"{index_location}.gz.tbi"

        # Convert to relative paths
        track["adapter"]["gffGzLocation"]["uri"] = os.path.relpath(track["adapter"]["gffGzLocation"]["uri"], base_dir)
        track["adapter"]["index"]["location"]["uri"] = os.path.relpath(track["adapter"]["index"]["location"]["uri"], base_dir)

    # Save the fixed config file
    with open(config_path, "w") as file:
        json.dump(config, file, indent=2)

    print("Fixed config.json paths and ensured .gz extensions.")


def add_plugins(config_path):
    config = None
    with open(config_path, "r") as file:
        config = json.load(file)
        plugins = [{"name": "Protein3d",
                    "authors": ["Colin Diesh"],
                    "description": "View 3-D protein structures in JBrowse 2",
                    "location": "https://github.com/cmdcolin/jbrowse-plugin-protein3d",
                    "license": "MIT",
                    "url": "https://unpkg.com/jbrowse-plugin-protein3d/dist/jbrowse-plugin-protein3d.umd.production.min.js",
                    "image": "https://raw.githubusercontent.com/GMOD/jbrowse-plugin-list/main/img/protein3d-fs8.png"
        }]
        config["plugins"] = plugins

    if config is not None:
        with open(config_path, "w") as config_file:
            json.dump(config, config_file, indent=2)
        

config_file = "jbrowse2/config.json"
jbrowse_dir = "jbrowse2"

fix_config_paths(config_file, jbrowse_dir)
add_plugins(config_file)