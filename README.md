# MEP

This is CISC3025 NLP project 3, which about implement name entity using maximum entropy model.

# new update 
all results are stored in `record.txt`. There are two parts for each flag `-t`, `-s` and `-D`.
1. config, this records the `beta`, `max-iters` and `model` dump or used
1. the second part records the info. ie: in test, f_score, accuracy etc.
   
NOTE: for each train(), all features name are recorded in `record.txt`

for each `dump_model`, the model is records and stored in file `models` with format `model{current_time}.pkl`
   
# f-score
f_score=        0.9626
accuracy=       0.9880
recall=         0.9173
precision=      0.9757

# Makefile

use `make` to run to program in path: `MEP/CISC3025 project 3/NER`

```shell
make t
```

This is eqivalent to `python3 run.py -t`

```shell
make d
```

```shell
make s
```

```shell
make D
```

This is new command which is eqivalent to `python3 run.py -D`. It shows the samples that with wrong judgement and 
count the number of such samples

# time in training
- 3379.91s