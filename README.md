# LoadTest.py

LoadTest.py is a Python tool for simulating end-user traffic by replaying access logs. Its a first draft. Might have to be tweeked to work for a given usecase

## Installation

Just download and run with Python3

## Usage
Running the tool requires a directory that contaions n logfiles. Each logfile provided will simulate the traffic of one user.
the Directory has to be called `accesslogs` and should be a sibeling of the script


```
├── accesslogs
│   └── access-log-1.log
│   └── access-log-2.log
│   └── access-log-3.log
│   └── ...
└── LoadTest.py
```
