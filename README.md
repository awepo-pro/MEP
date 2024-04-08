# MEP

This is CISC3025 NLP project 3, which about implementing name entity using maximum entropy model.

# web (PHP)
```shell
php index.php
php -S localhost:8000
```
open `http://localhost:8000` in browser

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

This is new command which is eqivalent to `python3 run.py -D`. It shows the samples that with wrong judgement and count the number of such samples