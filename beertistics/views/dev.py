import flask
import json 
import os, os.path
from beertistics import app, auth, untappd

@app.route('/dev/stub/<string:user>')
@auth.requires_auth
def dev_stub(user):

    if app.config["UNTAPPD_STUB"]:
        return "Untapped is in stubbed mode. Not possible to update data!"


    checkins = untappd.get_checkins(user)
    friends = untappd.get_user_friends(user)
    user_info = untappd.get_user_info(user)

    user_dir = os.path.join('stub',user)

    if not os.path.exists(user_dir):
        os.mkdir(user_dir)

    with open(os.path.join(user_dir, 'checkins.json'), 'w') as f:
        json.dump(checkins, f, indent = True)

    with open(os.path.join(user_dir, 'user_friends.json'), 'w') as f:
        json.dump(friends, f, indent = True)

    with open(os.path.join(user_dir, 'user_info.json'), 'w') as f:
        json.dump(user_info, f, indent = True)
        
    return 'Your data for %s is complete' % user 