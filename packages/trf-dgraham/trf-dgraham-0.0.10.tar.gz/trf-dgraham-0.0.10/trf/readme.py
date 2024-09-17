# trf/readme.py

readme_template = """\
## trf: tracker - record and forecast

This is a simple application for tracking the sequence of occasions on which a task is completed and predicting when the next completion might be needed.

### Motivation

As an example, consider the task of "filling the bird feeders". Suppose you want to have an idea when you should next fill them. One approach would be to set a reminder to fill them every 14 days starting from the last time you filled them. When the reminder is triggered, you could check the feeders to see if they are empty. If they are, you could fill them and then perhaps adjust the reminder to repeat every 13 days. On the other hand, if they are not yet empty, you might adjust the reminder to repeat every 15 days. Repeating this process, you might eventually set a repetition frequency for the reminder that predicts fairly well the next time you should fill them.

The goal of *track* is to save you trouble of going through this iterative process. Here's how it works:


1. In *track*, press "n" to add a new tracker and name it "fill bird feeders".
2. The first time you fill the feeders, press "c" to add a completion, select the "fill bird feeders" tracker and enter the date and time of the completion. This date and time will be added to the history of completions for the "fill bird feeders" tracker.
3. The next time you need to fill the feeders, repeat the process described in step 2. At this point, you will have two datetimes in the history of the tracker, track will calculate the interval between them and set the "expected next completion" by adding the interval to last completion date and time.
4. The process repeats with each completion. There are only two differences when there are more than 2 completions:

      - The "expected next completion" is calculated by adding the *average* of the intervals to the last completion date and time.

      - If there are more than 12 completions, only the last 12 completions are used to calculate the average interval. The estimated next completion date and time is thus based only on the average of the intervals for the most recent 12 completions.

One slight wrinkle when adding a completion is that you might have filled the bird feeders because it was a convenient time even though you estimate that you could have waited another day. In this case the actual interval should be the difference between the last completion date and the current completion date plus one day. On the other hand, you might have noticed that the feeders were empty on the previous day but weren't able to fill them. In this case the actual interval should be the difference between the last completion date and the current completion date minus one day. To accommodate this, when adding a completion you can optionally specify the interval adjustment. E.g., `4p, +1d` would add a completion for 4pm today with an estimate that the completion could have been postponed by one day. Similarly, `4p, -1d` would add a completion for 4pm today with an estimate that the completion should have been done one day earlier.

The recorded history of completions is thus a list of (datetime, timedelta) pairs with a corresponding list of intervals

        history: [(dt[0], td[0]), (dt[1], td[1]), (dt[2], td[2]), ...]
        intervals: [dt[1] + td[1] - dt[0], dt[2] + td[2] - dt[1], ...]

Here is an illustration of the "inspect" display for the "fill bird feeders" tracker showing a history of three completions together with the corresponding two intervals and other related calculations:

{inspect}

Datetimes are reported using 6 digits for the date and 4 digits for the 24-hour time separated by `T`: `yymmddTHHMM`.  Timedeltas are reported as integer numbers of d (days), h (hours) and m (minutes).

Note that the first interval, `+11d = 11 days`, is the difference between `240823T1400 +1d` and `240813T1400`.  The other intervals are computed in the same way. The `average` interval is just the sum of the two intervals divided by 2. The little downward pointing arrow after the average interval indicates that, since the last interval is less than the average, the average is decreasing.

The `spread` is the average of the absolute values of the differences between the intervals and the average interval. This *MAD* (mean average deviation) is a standard measure of the spread of a series about its average (mean). These calculations are used in two ways:

1. The `forecast` for when the next completion will be due is the sum of the last `completion` datetime and the `average` interval between completions.
2. The confidence we might have in this forecast depends upon the `spread`. If the `spread` is small, we would expect the actual interval between the last completion and the next completion to be close to the average. Chebyshev's Inequality says, in fact, that the proportion of intervals that lie within `η × spread` of the average interval must be at least `1 - 1/η²`. These are the settings for `early` and `late`:

        early = forecast - η × spread
        late = forecast + η × spread

where, by default, `η = 2`. With these settings at least 75% of the intervals would put the actual outcome between `early` and `late`. For the bird feeder example:

        early = 240912T2000 - 2 × 14h = 240911T1600
        late = 240912T2000 + 2 × 14h = 240914T0000

The list view reflects theses calculations:

{list}

In this view, the `forecast` column shows, as discussed above, the sum of `latest` (the last completion) and the average interval between completions. The `η × spread` column shows the product of `η` and the `spread`, e.g., for the bird feeder example, `η = 2` and `spread = 14h` so the column shows `2 × 14h = 28h = 1d4h`.

Since it is currently 10:32am on September 16 or `240916T1032` and this is past `late = 240914T0000` for bird feeders, the display shows the bird feeder tracker in a suspiciously-late color, burnt orange. By comparison, `early` and `late` datetimes for "between late and early" are September 17 plus or minus 6 days and 3 hours.  Since the current time lies within this interval, "between early and late" gets an anytime-now color, gold. Finally, since `early` for "before early" is September 21 minus 3 days and 14 hours which is later than the current time, "before early" gets a not-yet color, blue. There is no forecast for the last two trackers since neither have the two or more completions which are required for an interval on which to base a forecast, so these get trackers get the the no-forecast color, white.

By default, trackers are sorted in reverse order by their "forecast" datetimes, since this is the order in which they will likely need to be completed, and colors them by likely urgency. It is also possible to sort trackers by "latest", "name" or "doc_id" (creation order).

### Options when creating a new tracker

When you press 'n' to create a new tracker, the one requirement is that you specify a name for the new tracker

        > the name of my tracker

You can, optionally, specify a first completion by appending a datetime, e.g.,

        > the name of my tracker, 3p

would record a completion for 3pm today. You can also, optionally, provide an estimate for the next completion by appending a timedelta, e.g.,

        > the name of my tracker, 3p, +12d

would not only record a completion for 3pm today but also provide 12 days as an initial estimate for the interval until the next completion will be needed.

### Usage

#### Data, Backup and Restore

Track stores its data in a ZOBD database.  The data itself is a python dictionary with integer doc_id's as keys and dictionaries as values. These dictionaries contain entries for the tracker name and the history of completions and internals for the intervals and other computed values.  An additional dictionary containing user settings is also stored in the ZOBD datastore.

The ZOBD datastore transparently stores these python objects as 'pickled' versions of the objects themselves, using two files called 'track.fs' and 'track.fs.index'. Track keeps a daily, rotating back up of these two files in a zip format when ever 'track.fs' has been modified since the last backup.  Of these zip files, only 7 are kept  including the 3 most recent 3 files and 4 older files separated by intervals of at least 14 days. Here is an illustrative simulation of the daily backups that would be kept as of November 8, 2024:

        simulating date 241108
            241108.zip
            241107.zip
            241106.zip
            241028.zip
            241013.zip
            240928.zip
            240913.zip

Track also provides a command line option to restore the datastore from from one of these zip files - more on this later.  ZOBD also uses files called 'track.fs.lock' and 'track.fs.tmp' but they are not needed for restoring the datastore and are not backed up.

#### Track Home Directory

Track stores its data in its 'home directory'. When started from the command line there are three optional arguments:

        python3 track.py [log_level] [home_dir] ['restore']

If log_level is given it should be an integer - 10 for debug, 20 for info, 30 for warning or 40 for error, otherwise log_level defaults to 20.

If home_dir is given, it should be the path to the directory for track to use.

If home_dir is not given but there is an environmental variable, TRACKHOME, that specifies a directory, then that directory will be used as the home directory.

Finally, if neither home_dir nor TRACKHOME is given, then track will use the current working directory as its home directory.

If 'restore' is given, then a list of the available backup zip files in the 'backup' sub directory of the home dir will be presented to the user with a prompt to choose the zip file from which to restore the datastore. If the user chooses a zip file, the current 'track.fs' and 'track.fs.index' files will first be saved as 'restore.zip' and then overwritten with the contents of the selected zip file. The next time track is started it will use the restored datastore.

In addition to the 'backup' subdirectory mentioned above, track keeps a daily rotating backup of its log files in a another subdirectory called 'logs'."""


# Define replacements for image links or text alternatives
image_replacements = {
    "inspect": "![inspect view](tracker_inspect.png)",
    "list": "![list view](tracker_list.png)",
}

text_replacements = {
    "inspect": """\
    name:         fill bird feeders
    doc_id:       1
    created:      240915T1232
    modified:     240916T0935
    completions:  (3)
        240813T1400 +0m, 240823T1400 +1d, 240902T1000 +0m
    intervals:    (2)
        +11d, +9d20h
        average:  10d10h↓
        spread:   14h
    forecast:     240912T2000
        early:    240911T1600
        late:     240914T0000
""",
    "list": """\
    tag  forecast  η spread   latest    name
    a    24-09-12  1d4h      24-09-02   fill bird feeders
    b    24-09-17  3d1h30m   24-09-10   between early and late
    c    24-09-21  1d20h     24-09-13   before early
    d       ~         ~      24-09-12   only one completion
    e       ~         ~         ~       no completions yet
"""
}

def generate_readme():
    with open("README.md", "w") as f:
        f.write(readme_template.format(**image_replacements))
    with open("README.txt", "w") as f:
        f.write(readme_template.format(**text_replacements))


if __name__ == "__main__":
    print("generating README.md and README.txt")
    generate_readme()