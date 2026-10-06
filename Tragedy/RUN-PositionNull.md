# Running the positional null on the held-out tragedies

**You are the runner: you run one committed program, save its output, and push it; you change no program and judge nothing.**
The program is `Tragedy/heldOutChecks.py position`, which applies the frozen rule of `Blocks/PositionNull.txt` to the plays P05 to P32.
It is a long computation (likely an hour or more) and uses one processor.

## Steps

**0. Work from the latest `master`.**
Bring the working copy up to date with `master` and start your branch from it. Report the commit you started from.

**1. Put the tragedy transcriptions beside this repository.**
The program reads them from a folder named `Tragedy` next to this repository's folder:

```
git clone https://github.com/MooseNotSquirrel/Propp-Tragedy.git ../Tragedy
```

If the clone is refused, stop and report it; do not copy the transcriptions any other way.

**2. Check that Python has numpy.** If `python -c "import numpy"` fails, install it with `pip install numpy`.

**3. Run the program in the background, and wait for it.**

```
PYTHONIOENCODING=utf-8 nohup python Tragedy/heldOutChecks.py position > /tmp/posnull.log 2>&1 &
```

Check every ten minutes or so whether the process is still running (`ps aux | grep heldOutChecks`), without restarting it.
It is finished when the process is gone and `Tragedy/PositionNullHeldOut.txt` exists.
If it stops with an error, save `/tmp/posnull.log` as `Tragedy/PositionNullHeldOut.log`, and report it.

**4. Check the files.** `git status` must show `Tragedy/PositionNullHeldOut.txt` as the only new file, and nothing modified; `Blocks/PositionNullRun.txt` must be unchanged.

**5. Commit and push.** Commit only `Tragedy/PositionNullHeldOut.txt` (or the log, on an error) with the message `Tragedy positional null, held out`, to a new branch; if your environment assigns the branch name, use it.

**6. Reply with a short account:** the commit you started from, the branch, how long the run took, and the file's verdict lines copied word for word.
