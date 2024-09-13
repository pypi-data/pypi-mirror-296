# Villog is a simple logger for your everyday projects

## Villog

### Usage
**script.py**
```
from villog import Logger

l = Logger()

l.log("test")
```
**log.txt**
```
2024.06.20 14:55:50|test
```

### Logger __init__
- ```file_path```: (str) Path to the, by default it is **./log.txt**
- ```encoding```: (str) Encoding of the file it logs to, by default it is **utf-8-sig**
- ```time_format```: (str) Format of the strftime, by default it is **%Y.%m.%d %H:%M:%S**
- ```separator```: (str) Separator between the time and the content, by default it is **" - "**

### Logger functions
- ```log()```: logs
- ```change_path()```: changes the ```file_path```
- ```change_encoding()```: changes the ```encoding```
- ```change_time_format()```: changes the ```time_format```
- ```change_separator()```: changes the ```separator```
- ```read()```: returns the content of the log file
- ```read_list()```: returns the content of the log file in a list line by line
- ```clear()```: clears the log file

## Writexcel

## Install
Via **pip**, with:
```
pip install villog
```