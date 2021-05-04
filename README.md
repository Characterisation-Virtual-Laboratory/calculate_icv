# calculate_icv.py
This script is used to calculate the ICV value from `subj-dir`/`mri`/`talairach.xfm` and write the output to a new column in `Cerebel_vols.csv`

## Requirements
* `xfm2det` (put under the same directory as this script)
* Python module [pandas](https://pandas.pydata.org/)
* Python module [Fire](https://github.com/google/python-fire)

NOTE: It is recommended to use Python>=3.5, otherwise you will also need to install [pathlib](https://docs.python.org/3/library/pathlib.html)



## Usage

```
FLAGS
    --freesurfer_dir=FREESURFER_DIR
        Default: './freesurfer'
    --acapulco_dir=ACAPULCO_DIR
        Default: './acapulco_aachan'
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

## Notes

Assumptions
1. Executable xfm2det is under freesurfer_dir (default: $PWD/freesurfer)
2. output file (default: Cerebel_vols.csv) is under acapulco_dir (default: $PWD/acapulco_aachen)
p.s. $PWD represent current working directory

Note that
* In case that the subject id, which is parsed from the directory structure of target_name, is different from ID column of output csv
    * If ID is not found within the set of subject id ===> the corresponding rows will remain empty
    * If subject id is not found within the set of ID ===> the output value of xfm2det is ignored