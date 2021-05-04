# calculate_icv.py
This script is used to calculate the ICV value from `subj-dir`/`mri`/`talairach.xfm` and write the output to a new column in `Cerebel_vols.csv`

## Requirements
* `xfm2det` (put under the same directory as this script)
* Python module [pandas](https://pandas.pydata.org/)
* Python module [Fire](https://github.com/google/python-fire)

## Usage
NAME
    `calculate_icv.py`
    
SYNOPSIS
   `calculate_icv.py <flags>`

DESCRIPTION
    We assume 
   1. Executable xfm2det is under root dir
   2. output file Cerebel_vols.csv is under root dir

FLAGS
```
    --root=ROOT
        Default: current working directory
    --target_name=TARGET_NAME
        Default: 'talairach.xfm'
    --FS_template_volume_constant=FS_TEMPLATE_VOLUME_CONSTANT
        Default: 1948105
    --new_column_name=NEW_COLUMN_NAME
        Default: 'ICV_CALC'
    --output_csv_name=OUTPUT_CSV_NAME
        Default: 'Cerebel_vols.csv'
    --dryrun=DRYRUN
        Default: False
```
