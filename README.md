# calculate_icv.py
This script is used to calculate the ICV value from `subj-dir`/`mri`/`talairach.xfm` and write the output to a new column in `Cerebel_vols.csv`

## Requirements
* `xfm2det` (put under the same directory as this script)
* Python module [pandas](https://pandas.pydata.org/)
* Python module [Fire](https://github.com/google/python-fire)

## Usage
Default:
`calculate_icv.py` --> will run on current directory, assumes `Cerebel_vols.csv` is in the same directory

