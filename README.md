## Beertistics

Visualizing your drinking habits, based on your Untappd beer checkins.

Beertistics offers visualization of your untappd checkin data in the form of charts, maps and photos.
You log in using your

### Getting started

If you want to help contribute to beertistics, follow these steps.

#### Install

1. Install dependencies:

        $ pip install -r requirements.txt

1. Create config-file:

        $ cp beertistics/config/default.py.sample cp beertistics/config/default.py

    If you'd like to be able to actually authenticate with Untappd while developing (and not just use the stubbed data), make sure you update the `UNTAPPD_CLIENT_ID` and `UNTAPPD_CLIENT_SECRET` fields and set `UNTAPPD_STUB` to `False`.

1. Set up pre-commit hook:

        $ ln -s ../../scripts/pre-commit.sh .git/hooks/pre-commit

#### Startup

You start the development server with the provided script.

    $ ./scripts/server.py

You'll also need an Elastic Search instance running. Start one with this script (from another terminal/tab):

    $ ./scripts/es.sh

### Code style

The project uses [Flake8](https://flake8.readthedocs.org/en/2.0/) to check for good style and detect code smells.

You might stumble upon comments containing the word `noqa` scattered around some places in the project.
This is where something is intentionally done despite Flake8 considering it bad.

- any line ending with `# noqa` is ignored
- any file with the line `# flake8: noqa` is ignored

Use these when needed, but sparingly.

### Disclaimer

*Although based on data provided by them, Beertistics is in no way affiliated with Untappd.*