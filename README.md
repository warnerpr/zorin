How to run:
-----------

setup:

```
make get-sample-data
make prepare-venv
```

test:

```
make test-small
make
```

run it:

```
./venv/bin/python zorin/report.py <PATH_TO_INPUT> > <PATH_TO_OUTPUT>
```

Thought process:
----------------

**Update 1:**

- New keyboard (and weekend) has arrived, so time to tackle https://gist.github.com/jzellner/856fd143323f3cba4773
- Irix joke was funny.  Oh SGI
- New keyboard is much nicer than the one in the ideapad.  It is made for children's hands...
- Problem is to generate metrics from a large set of records stored in a file.  
- A DB does make sense to use as it would allow multiple processes to work on the problem, and allow for recovery on crash, but for first pass I Think I want to simply do it in RAM with one process and see how that goes.  I will put in an abstraction that allows me to add a DB later.

**Update 2:**

 - 3.5 hours in, it works on the big file too after fixing bugs
 - logic for online / offline was totally wrong but small file hid it.  should have written a unit test on that logic
 - takes about 20 - 25 seconds to run on large file
 - 350 MB RAM so probably 10M lines will max out past 2GB, so we can't do this in RAM
 - let's move it to a DB, but time is short to let's just use sqlite
