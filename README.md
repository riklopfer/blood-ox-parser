# blood-ox-parser

Extract blood oxygen and atmospheric pressure measurements (in kPa) from Apple Health XML export and write to CSV. 

```
usage: extract-blood-ox-csv.py [-h] [--export EXPORT] [--output OUTPUT]

optional arguments:
  -h, --help       show this help message and exit
  --export EXPORT  path to health data export
  --output OUTPUT  Write CSV to this file
```

Sample usage

```shell
python3 ./extract-blood-ox-csv.py --export ~/Downloads/apple_health_export/export.xml 
```

Sample output (`./bloodox.csv`)

```csv
Time,BloodOx,AtmPressure
2022-09-23 15:02:02 -0400,0.98,98.6993
2022-09-23 16:36:02 -0400,0.96,98.7532
2022-09-23 19:56:12 -0400,0.96,98.7608

```

Histogram

```shell
python3 ./elevation-histogram.py --bin-width 100
```

```
100.0m :: n=161     μ=0.96224 σ=0.02006 ************ 
200.0m :: n=435     μ=0.96037 σ=0.01993 ********************************* 
300.0m :: n=178     μ=0.96051 σ=0.02299 ************* 
```

