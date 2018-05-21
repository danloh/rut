# -*- coding: utf-8 -*-
# Not for production(except migrate), localtest/debug
import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db, cache
from app.models import Posts, Items, Collect, Star, Flag, Tags, Users,\
                       tag_post, tag_item, Comments, Mvote, Contribute,\
                       Fav, Follow, Roles, Respon, Permission, tag_demand,\
                       Demands, Dvote, Cvote, Rvote, Hvote, Authors, Byline,\
                       Reviews, Articles, Columns, Headlines, Clips, Messages,\
                       Circles, Dialog, Events, Reply, Clan, Gather, Roads, Heat

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, cache=cache, Posts=Posts, Items=Items,
                Collect=Collect, Star=Star, Flag=Flag, Cvote=Cvote,
                Tags=Tags, tag_post=tag_post, tag_item=tag_item,
                Comments=Comments, Users=Users, Contribute=Contribute,
                Fav=Fav, Follow=Follow, Roles=Roles, Respon=Respon,
                Permission=Permission, Gather=Gather, Roads=Roads,
                tag_demand=tag_demand, Demands=Demands, Dvote=Dvote,
                Authors=Authors, Byline=Byline, Hvote=Hvote, Mvote=Mvote,
                Clan=Clan, Reply=Reply, Reviews=Reviews, Rvote=Rvote,
                Articles=Articles, Columns=Columns, Headlines=Headlines,
                Clips=Clips, Messages=Messages, Circles=Circles,
                Dialog=Dialog, Events=Events, Heat=Heat)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


# # for code profiling
@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler
    : run python manage.py profile
    """
    p_dir = profile_dir or os.path.join(os.getcwd(), 'backend/log/prof/')
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=p_dir)
    app.run()


@manager.command
def createdb():
    # create db
    db.create_all()
    # create user roles
    Roles.add_role()


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade
    from app.models import Roles
    # migrate database to latest revision
    upgrade()
    # create user roles
    Roles.add_role()


if __name__ == '__main__':
    manager.run()
