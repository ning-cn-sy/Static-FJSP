# FJSP-MR

This repository is the official implementation of the paper 
"[A novel two stage neighborhood search for flexible job shop scheduling problem considering reconfigurablemachine tools]".
Shi, Y., Yu, C. & Ning, S. A novel two stage neighborhood search for flexible job shop scheduling problem considering reconfigurable machine tools. Complex Intell. Syst. 11, 312 (2025). 
https://doi.org/10.1007/s40747-025-01890-0


## Quick Start

### requirements

- python $=$ 3.8.20
- jmetalpy $=$ 1.6.0
- numpy $=$ 1.24.4
- pandas $=$ 2.0.3
- torch $=$ 1.11.0
- torchaudio $=$ 0.11.0
- torchvision $=$ 0.12.0
- tqdm $=$ 4.67.1

### CPLEX-requirements
- python $=$ 3.6.13
- numpy $=$ 1.19.5

### introduction

- `Example` saves the instance files including testing instances .
- `Algrithm` includes the proposed problem model and algorithm structure .
- `Config` contains the definitions of the basic elements required for FJSP-MR.
- `Util` includes data retrieval from standard cases(`Read_By_FJS.py`) .
- `CPLEX.py` is the solver code used to solve MILP, serving as a benchmark for algorithm evaluation.
- `Main.py` is used for solve.
```

### solve

```python
python Main.py
