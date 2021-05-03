#!/usr/bin/env python3
from pathlib import Path
from fire import Fire
import subprocess
import pandas as pd
import os
import logging
import re
#logging.basicConfig(level=logging.INFO)


def standardise_subject_id(subject_id):
    """
    1. strip trailing _temp
    2. Convert con00x => Cont_0x
    """

    subject_id = subject_id.strip("_temp")
    pat = re.compile("[con]{3}(\d{3})")
    if pat.match(subject_id):
        subject_id = f"Cont_{pat.search(subject_id).group(1)[-2:]}"
    return subject_id

def main(
    root=os.getcwd(),
    target_name="talairach.xfm",
    FS_template_volume_constant=1948105,
    new_column_name="ICV_CALC",
    output_csv_name = "Cerebel_vols.csv",
    dryrun=False
):
    """
    We assume
    1. Executable xfm2det is under root dir
    2. output file Cerebel_vols.csv is under root dir
    """
    root = Path(root)
    exec = root / "xfm2det"
    output_csv = root / output_csv_name
    if not (exec.is_file() and os.access(exec, os.EX_OK)):
        raise Exception(f"{exec} is not executable, we assume xfm2det is under root directory {root}")
    if not (output_csv.is_file()):
        raise Exception(f"Output csv {output_csv} does not exist")
    input_files = [p for p in root.glob("**/*.*") if p.name == target_name]

    outputs = {}

    for i in input_files:
        if i.parent.name != "transforms" or i.parent.parent.name != "mri":
            logging.warning(f"Some directory structure does not compliant with the assumption of the directory structure, => {i}")
        subject_id = i.parent.parent.parent.name
        command = f"{exec} {i}"
        proc = subprocess.run(command, shell=True, capture_output=True)
        value = float(proc.stdout.decode().split('\t')[-1].rstrip("\n"))
        outputs[standardise_subject_id(subject_id)] = value * FS_template_volume_constant

    df_orig = pd.read_csv(output_csv, index_col="ID")
    valid_ids = df_orig.index.intersection(outputs.keys())
    logging.info(f"Values for subject {list(valid_ids)} will be filled in")
    df_values = pd.Series({k: v for k, v in outputs.items() if k in valid_ids}, name=new_column_name)

    #df_orig.columns = ['' if i == 'Unnamed: 0' else i for i in df_orig.columns ]
    df_new = pd.concat([df_orig, df_values], axis=1)
    df_new.index.name = "ID"
    df_new = df_new.reset_index()
    # print(df_new.columns[[0,1]])

    # df_new = df_new[df_new.columns[[1,0]]]
    df_new = df_new.rename(columns={"Unnamed: 0": ""})
    if not dryrun:
        df_new.to_csv('output.csv', index=False, columns=["", "ID", *df_new.columns[2:]])

    else:
        print(f"output csv: \n{df_new}")





if __name__ == "__main__":
    Fire(main)
