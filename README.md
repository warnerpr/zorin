# zorin

New keyboard (and weekend) has arrived, so time to tackle https://gist.github.com/jzellner/856fd143323f3cba4773

Thought process:
----------------

**Update 1:**

- Irix joke was funny.  Oh SGI
- New keyboard is much nicer than the one in the ideapad.  It is made for children's hands...
- Problem is to generate metrics from a large set of records stored in a file.  
- A DB does make sense to use as it would allow multiple processes to work on the problem, and allow for recovery on crash, but for first pass I Think I want to simply do it in RAM with one process and see how that goes.  I will put in an abstraction that allows me to add a DB later.
