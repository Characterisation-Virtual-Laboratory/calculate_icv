# calculate_icv.py
This script implements two procedures
* calculate_icv: Calculating ICV values from `subject-dir`/`mri`/`talairach.xfm` and write the output to a new column in `Cerebel_vols.csv`.
* icv_correction: For each volume files under acapulco dir, devide colume `volume` by its corresponding ICV value, and write the output to a new volume file suffixed by `CORR.csv` in the same directory.

## Requirements
* `xfm2det` (put under the same directory as this script)
* Python module [pandas](https://pandas.pydata.org/)
* Python module [Fire](https://github.com/google/python-fire)

NOTE: It is recommended to use Python>=3.5, otherwise you will also need to install [pathlib](https://docs.python.org/3/library/pathlib.html)



## Usage


```
./calculate_icv.py --freesurfer_dir=<path to freesurfer directory> --acapulco_dir=<path to acapulco directory> [calculate_icv|icv_correction]
```
### Command line arguments

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

## Debugging

Make sure you always run with `--dryrun=True` before you run the program.


### calculate_icv



You can print out a list of input files ('talairach.xfm') discorvered by the program through `input_files` subcommand
```
./calculate_icv.py input_files
```

If you want check the icv value of single input file you may run

```
./calculate_icv.py _calculate_icv <path to telairach.xfm>
```

Or if you have a set of input files under  directory "root"
```
find <root> -name talairach.xfm | xargs ./calculate_icv.py _calculate_icv_batch
```

### icv_correction

You can print out a list of volume files discorvered by the program through `volume_files` subcommand
```
./calculate_icv.py volume_files
```

## Notes

Assumptions
1. Executable xfm2det is under freesurfer_dir (default: $PWD/freesurfer)
2. output file (default: Cerebel_vols.csv) is under acapulco_dir (default: $PWD/acapulco_aachen) if you are running calculate_icv
p.s. $PWD represent current working directory

