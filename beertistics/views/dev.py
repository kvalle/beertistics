import flask
import json
from os import mkdir
from os.path import join, exists
from beertistics import app, auth, untappd


@app.route('/dev/stub/<string:user>')
@auth.requires_auth
def dev_stub(user):
    if app.config["UNTAPPD_STUB"]:
        return "Unable to update stubs because Untapped is in stubbed mode."

    user_dir = join('stub', user)

    if not exists(user_dir):
        mkdir(user_dir)

    with open(join(user_dir, 'checkin.json'), 'w') as f:
        json.dump(untappd.get_checkins(user), f, indent=True)
    with open(join(user_dir, 'friend_list.json'), 'w') as f:
        json.dump(untappd.get_user_friends(user), f, indent=True)
    with open(join(user_dir, 'user_info.json'), 'w') as f:
        json.dump(untappd.get_user_info(user), f, indent=True)

    return 'Updated stub for user "%s".' % user
