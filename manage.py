# -*- coding: utf-8 -*-

import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db 
from app.models import Posts, Items, Collect, Tags, Fav, \
                       tag_post, tag_item, tag_demand,\
                       Comments, Reviews, Clips, Demands,\
                       Star, Flag, Challenge, Contribute, Follow,\
                       Users, Roles, Permission, Authors, author_item,\
                       Reply, Clan, Messages, Dialog, Events
       

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, Posts=Posts, Items=Items, 
                Collect=Collect, Star=Star, Flag=Flag, 
                Tags=Tags, tag_post=tag_post, tag_item=tag_item, 
                Comments=Comments, Users=Users, Contribute=Contribute,
                Fav=Fav, Follow=Follow, Roles=Roles,
                Permission=Permission, Challenge=Challenge, 
                tag_demand=tag_demand, Demands=Demands,
                Authors=Authors, author_item=author_item, 
                Clan=Clan, Reply=Reply, Reviews=Reviews,
                Clips=Clips, Messages=Messages, 
                Dialog=Dialog, Events=Events)

manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


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

