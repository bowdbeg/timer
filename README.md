# timer
A Python library to measure time

## Installation

You can install the package using pip through repository on GitHub:

```bash
pip install git+https://github.com/bowdbeg/timer.git
```

## Usage

You can easily measure time using the Timer class. Refer to sample_toy.py, sample_ml.py, and the following example:

```python
>>> from timer import Timer
>>> timer = Timer()
2024-10-29 16:02:11,760 - timer.timer - INFO - Timer started
>>> timer.lap()
2024-10-29 16:02:16,150 - timer.timer - INFO - Lap 0: 4.390325307846069
4.390325307846069
>>> timer.lap()
2024-10-29 16:02:27,638 - timer.timer - INFO - Lap 1: 11.487971544265747
11.487971544265747
>>> timer.lap("func1")
2024-10-29 16:03:12,157 - timer.timer - INFO - Lap func1_0: 44.51946711540222
44.51946711540222
>>> timer.lap("func1")
2024-10-29 16:03:15,184 - timer.timer - INFO - Lap func1_1: 3.0271990299224854
3.0271990299224854
>>> timer.split()
2024-10-29 16:03:45,154 - timer.timer - INFO - Split 0: 93.39418435096741
93.39418435096741
>>> timer.split('end')
2024-10-29 16:03:58,905 - timer.timer - INFO - Split end_0: 107.14573907852173
107.14573907852173
>>> print(timer.report())
Timer report
Total time: 115.72586154937744
Laps:
0: 4.390325307846069
1: 11.487971544265747
func1_0: 44.51946711540222
func1_1: 3.0271990299224854
Splits:
0: 93.39418435096741
end_0: 107.14573907852173

>>> timer.start()
2024-10-29 16:05:18,958 - timer.timer - INFO - Timer started
>>> timer.lap()
2024-10-29 16:05:26,485 - timer.timer - INFO - Lap 0: 7.527182579040527
7.527182579040527
>>> print(timer.report())
Timer report
Total time: 12.784441947937012
Laps:
0: 7.527182579040527
Splits:

```