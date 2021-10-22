## Delete Z(oom) from K(altura)

This script was written for an organization that used 
[Kaltura](https://developer.kaltura.com/api-docs/Overview) 
to store a variety of recordings.
To maintain compliance with certain legislation, all recordings
that were migrated into Kaltura from 
[Zoom](https://marketplace.zoom.us/docs/api-reference/zoom-api)
were required to be deleted after the quarter. 


>This script uses [Poetry](https://python-poetry.org/) for 
virtual environment and dependency management.

### Installation:

```
poetry install
```

### Run:

```
$ poetry run python src/main.py -s START -e END -p PATH --delete
```
> Date format: MM-DD-YYYY

*Note: -p PATH not required for Version 2, since we are not downloading.*

**WARNING:** the --delete flag will enable deleting media.
