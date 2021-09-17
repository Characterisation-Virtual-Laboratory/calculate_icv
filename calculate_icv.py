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

FS_TEMPLATE_VOLUME_CONSTANT = 1948105

class CalculateICV:
    def __init__(self,
        freesurfer_dir=Path() / "freesurfer",
        acapulco_dir=Path() / "acapulco_aachen",
        output_csv_name="Cerebel_vols.csv",
        target_name="talairach.xfm",
        FS_template_volume_constant=FS_TEMPLATE_VOLUME_CONSTANT,
        new_column_name="ICV_CALC",
        dryrun=False
    ):
        self.freesurfer_dir = Path(freesurfer_dir)
        self.acapulco_dir = Path(acapulco_dir)
        self.output_csv = self.acapulco_dir / output_csv_name
        self.target_name = target_name
        self.FS_template_volume_constant = FS_template_volume_constant
        self.new_column_name = new_column_name
        self.dryrun = dryrun
        self.exec = self.freesurfer_dir / "xfm2det"
    def check_exec(self):
        if not (self.exec.is_file() and os.access(self.exec, os.EX_OK)):
            raise Exception(f"{self.exec} is not executable, we assume xfm2det is under root directory {self.freesurfer_dir}")
        if not (self.output_csv.is_file()):
            raise Exception(f"Output csv {self.output_csv} does not exist")
    @property
    def input_files(self):
        files = [p for p in self.freesurfer_dir.glob("**/*.*") if p.name == self.target_name]
        for i in files:
            if i.parent.name != "transforms" or i.parent.parent.name != "mri":
                logging.warning(f"Some directory structure does not compliant with the assumption of the directory structure, => {i}")
        return files
    def _calculate_icv_batch(self, *input_files):
        outputs = {}
        for i in input_files:
            i = Path(i)
            subject_id = i.parent.parent.parent.name
            outputs[subject_id] = self._calculate_icv(i)
        return outputs

    def _calculate_icv(self, input_file):
        command = f"{self.exec} {input_file}"
        proc = subprocess.run(command, shell=True, capture_output=True)
        value = float(proc.stdout.decode().split('\t')[-1].rstrip("\n"))
        return value * self.FS_template_volume_constant

    def calculate_icv(self):
        outputs = self._calculate_icv_batch(*self.input_files)
        df_orig = pd.read_csv(self.output_csv, index_col="ID")
        valid_ids = df_orig.index.intersection(outputs.keys())

        if (len(valid_ids) != len(list(outputs.keys()))):
            print(Fore.RED + f"IDs from {self.output_csv} do not match subject ids found in directories")
            print(tabulate({f"{self.output_csv}": sorted(list(df_orig.index)), "subjects ids": sorted([f'{v}' for v in outputs.keys()]), "valid_ids": sorted(valid_ids)}, tablefmt="github", headers='keys'))
        df_values = pd.Series({k: v for k, v in outputs.items() if k in valid_ids}, name=self.new_column_name, dtype=object)
        if self.new_column_name in df_orig.columns:
            print(Fore.RED + f"{self.new_column_name} exists as an column in {self.output_csv}, remove it first before running this script")


        df_new = pd.concat([df_orig, df_values], axis=1)
        df_new.index.name = "ID"
        df_new = df_new.reset_index()
        df_new = df_new.rename(columns={"Unnamed: 0": ""})
        if not self.dryrun:
            df_new.to_csv(self.output_csv, index=False, columns=["", "ID", *df_new.columns[2:]])
        else:
            print(f"output csv: \n{df_new}")
    @property
    def volume_files(self):
        subjects = [i for i in self.acapulco_dir.iterdir() if i.is_dir()]
        volume_files = [list(i.glob("*_volumes.csv")) for i in subjects] # make sure there is only on volumn file
        volume_files = [i[0] for i in volume_files if len(i)==1]
        return volume_files
    def icv_correction(self):
        for f in self.volume_files:
            data = pd.read_csv(f)
            subject_id = f.parent.name
            input_file = Path(self.freesurfer_dir / subject_id / 'mri' / 'transforms' / 'talairach.xfm')
            if input_file.exists():
                icv_value = self._calculate_icv(input_file=input_file)
                data['volume'] = data['volume'] / icv_value
                if self.dryrun:
                    print(f"ICV corrected value for {subject_id} will be saved to {f.parent}/{f.stem}_CORR.csv")
                    print(data)
                else:
                    data.to_csv(f.parent / f"{f.stem}_CORR.csv", index=False)
            else:
                print(Fore.RED + f"Cannot find input file {input_file}")
        return



if __name__ == "__main__":
    Fire(CalculateICV)
