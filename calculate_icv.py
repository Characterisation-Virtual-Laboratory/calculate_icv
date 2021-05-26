#!/usr/bin/env python3
from pathlib import Path
from fire import Fire
import subprocess
import pandas as pd
import os
import logging
import re
from tabulate import tabulate
from colorama import Fore, init
#logging.basicConfig(level=logging.INFO)
init(autoreset=True)



def main(
    freesurfer_dir=Path() / "freesurfer",
    # output_csv=Path() / "acapulco_aachen" / "Cerebel_vols.csv",
    acapulco_dir=Path() / "acapulco_aachen",
    output_csv_name="Cerebel_vols.csv",
    target_name="talairach.xfm",
    FS_template_volume_constant=1948105,
    new_column_name="ICV_CALC",
    dryrun=False
):
    """
    Run <freesurfer_dir>/xfm2det against all files named <target_name>,
    then store the output value times <FS_template_volume_constant> into <output_csv> with column name <new_column_name>

    Assumptions:
    1. Executable xfm2det is under freesurfer_dir (default: $PWD/freesurfer)
    2. output file (default: Cerebel_vols.csv) is under acapulco_dir (default: $PWD/acapulco_aachen)
    p.s. $PWD represent current working directory
    """
    output_csv = Path(acapulco_dir) / output_csv_name

    freesurfer_dir = Path(freesurfer_dir)
    output_csv = Path(output_csv)
    exec = freesurfer_dir / "xfm2det"

    if not (exec.is_file() and os.access(exec, os.EX_OK)):
        raise Exception(f"{exec} is not executable, we assume xfm2det is under root directory {root}")
    if not (output_csv.is_file()):
        raise Exception(f"Output csv {output_csv} does not exist")
    input_files = [p for p in freesurfer_dir.glob("**/*.*") if p.name == target_name]

    outputs = {}

    for i in input_files:
        if i.parent.name != "transforms" or i.parent.parent.name != "mri":
            logging.warning(f"Some directory structure does not compliant with the assumption of the directory structure, => {i}")
        subject_id = i.parent.parent.parent.name
        command = f"{exec} {i}"
        proc = subprocess.run(command, shell=True, capture_output=True)
        value = float(proc.stdout.decode().split('\t')[-1].rstrip("\n"))
        outputs[subject_id] = value * FS_template_volume_constant

    df_orig = pd.read_csv(output_csv, index_col="ID")
    valid_ids = df_orig.index.intersection(outputs.keys())

    if (len(valid_ids) != len(list(outputs.keys()))):
        print(Fore.RED + f"IDs from {output_csv} do not match subject ids found in directories")
        print(tabulate({f"{output_csv}": sorted(list(df_orig.index)), "subjects ids": sorted([f'{v}' for v in outputs.keys()]), "valid_ids": sorted(valid_ids)}, tablefmt="github", headers='keys'))
        print(Fore.RED + f"stopping the script, {output_csv} remains unmodified")
        return



    df_values = pd.Series({k: v for k, v in outputs.items() if k in valid_ids}, name=new_column_name, dtype=object)
    if new_column_name in df_orig.columns:
        print(Fore.RED + f"{new_column_name} exists as an column in {output_csv}, remove it first before running this script")


    df_new = pd.concat([df_orig, df_values], axis=1)
    df_new.index.name = "ID"
    df_new = df_new.reset_index()
    df_new = df_new.rename(columns={"Unnamed: 0": ""})
    if not dryrun:
        df_new.to_csv(output_csv, index=False, columns=["", "ID", *df_new.columns[2:]])
    else:
        print(f"output csv: \n{df_new}")


if __name__ == "__main__":
    Fire(main)
