# PyProgress

## General Use

A simple interface for terminal based progress updates

Begin by creating an instance with the starting and ending value

```python
import os

files = os.listdir('.')
bar = ProgressBar(0, len(files))
for file in files:
    bar.iterbegin('Processing file: {}'.format(file))
    process(file)
    bar.iterdone()
bar.done()
```

Manually call `ProgressBar.iterbegin([message])` before an iteration starts 
and call `ProgressBar.iterend()` when it completes or `ProgressBar.iterfail()` 
if it fails 

When all items complete use `ProgressBar.done()` to print a summary

## Alternative Use – Context Manager

ProgressBar instances can also be used as context managers

use a with statement on every iteration

```python
import os

files = os.listdir('.')
bar = ProgressBar(0, len(files), supress_exc=True)
for file in files:
    with bar:
        process(file)
bar.done()
```

Using the `supress_exc=True` argument will report statistic for failures
from raised exceptions but not raise the exception itself 

This is not necessary to use bar as a Context Manager but you must use it as a Context Manager to get the exception suppressing behavior
