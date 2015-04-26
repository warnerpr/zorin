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
make test-big
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

**Update 3:**

 - 5 hours in, took a while to get sqlalchemy going, had not used it in many years
 - wow, sqlalchemy + sqlite = insane slow.  20 second execution time is now 6 minutes
 - I don't want to leave it here at all, but I need to put it aside for today possibly.
 - Unsure if I should just get this working the rest of the way with current DB choices or pursue something better?  For sure if this was going into production I would not proceed with current performance, it is too slow.  
 - I wonder if the way I used the DB is just totally wrong or it is just that slow...

**Update 4:**
 
 - spent another hour (6 total) trying ZODB, which is even slower than sqlalchemy, so forget that
 - also tried getting the in memory version down on RAM, but I think 10M entries will still be 2.1 GB, so will fail the criteria.
 - Conclusion from my end is that I need to think a bit more about what DB to use.
