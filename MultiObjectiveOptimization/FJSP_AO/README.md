# FJSP-AO

This repository is the official implementation of the paper “[An MILP model and improved memetic algorithm for flexible job shop scheduling problem with multi-level assembly operations]”.

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
- `Algrithm` includes the proposed problem model and algorithm structure,`DANIEL` includes problem adaptation modifications to the referenced DANIEL algorithm.
- `Config` contains the definitions of the basic elements required for FJSP-AO.
- `Util` includes data retrieval from standard cases(`Read_By_FJS.py`), generation and allocation of assembly operations(`Instance_read_generator.py`), drawing functions(`Plot_util`), disjunction functions(`distinct_graph`), and weight generation functions(`weight.py`),`analyze.py` is used to evaluate the performance differences of algorithms.
- `CPLEX.py` is the solver code used to solve MILP, serving as a benchmark for algorithm evaluation.
- `Main.py` is used for solve.
```

### solve

```python
python Main.py 

# options (Validation instances of corresponding size should be prepared in ./data/data_train_vali/{data_source})
python Main.py 	self.TARGET_FOLDER = "D:\pycharmproject\MultiObjectiveOptimization\FJSP_AO_test\Outcome"
        self.path1 = "D:\pycharmproject\MultiObjectiveOptimization\FJSP_AO_test\Example_CD"
        self.path = "D:\pycharmproject\MultiObjectiveOptimization\FJSP_AO_test\Example_CD"
        self.op_str = [1]
        self.x = [1]
        self.type = ["CD"]
        self.init_flag = [False]
        self.instance = [
            [self.path1 + "\MK01.fjs"
             ],
            [
                self.path + "\MK01.fjs"
            ]
        ]
        self.cross = [0.8]
        self.mutation = [0.2]
        self.iteration = [self.instance, self.op_str, self.cross, self.mutation, self.init_flag, self.x, self.type]

        self.i = 0
        os.makedirs(self.TARGET_FOLDER, exist_ok=True)
```
## Reference

- https://github.com/wrqccc/FJSP-DRL?tab=readme-ov-file

