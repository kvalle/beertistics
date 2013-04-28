## Beertistics

Visualizing your drinking habits, based on your Untappd beer checkins.

Beertistics offers visualization of your untappd checkin data in the form of charts, maps and photos.
You log in using your

### Contribute

If you want to help contribute to beertistics, these are the steps needed to get verything up and running.

1. `$ pip install -r requirements.txt`
1. `$ cp beertistics/config/default.py.sample cp beertistics/config/default.py`

If you'd like to be able to actually authenticate with Untappd while developing (and not just use the stubbed data), make sure you update the `UNTAPPD_CLIENT_ID` and `UNTAPPD_CLIENT_SECRET` fields and set `UNTAPPD_STUB` to `False`.

You start the development server with the provided script.

    $ ./server.py

### Author

Any questions and feedback is welcome at kjetil.valle AT gmail.com.

### Disclaimer

*Although based on data provided by them, Beertistics is in no way affiliated with Untappd.*