#! /Users/oo/Project/flasking/venv python

import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db 
from app.models import Posts, Items, Collect, Tags, Fav, tag_post, tag_item, Comments,\
                       Users, Star, Flag, Challenge, Follow, Roles, Permission, Authors,\
                       author_item, tag_demand, Demands, Reply, Clan
       

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, Posts=Posts, Items=Items, Collect=Collect, Star=Star, Flag=Flag, 
                Tags=Tags, tag_post=tag_post, tag_item=tag_item, Comments=Comments, Users=Users, 
                Fav=Fav, Follow=Follow, Roles=Roles,Permission=Permission, Challenge=Challenge, 
                tag_demand=tag_demand, Demands=Demands, Clan=Clan, Reply=Reply)

manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade
    from app.models import Roles 
    
    # create db
    db.create_all()

    # migrate database to latest revision
    upgrade()

    # create user roles
    Roles.add_role()


if __name__ == '__main__':
    manager.run()

