## Delete Z(oom) from K(altura)

This is a script that deletes videos tagged with the
zoom tag from SUU's instance of Kaltura. This is done in
an effort to maintain compliance with certain legislation.

### Installation:

```
pip install -r requirements.txt
```

### Run:

```
$ python -m src -s START -e END -p PATH --delete
```
> Date format: MM-DD-YYYY
> 
> -p PATH not required for Version 2, since we are not downloading.

WARNING: the --delete flag will enable deleting media.
