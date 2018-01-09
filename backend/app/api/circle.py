# -*- coding: utf-8 -*-
# circle : challenge circle, a group people who challege a rut together

from flask import request, g, jsonify, abort
from ..models import *
from . import db, rest, auth, PER_PAGE

@rest.route('/<int:rutid>/circles')
def get_circles(rutid):
    # get request params
    area = request.args.get('area')
    # query
    query = Circles.query.filter_by(post_id=rutid)
    if area:
        query = query.filter_by(area=area)
    # pagination
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    circles = query.offset(page*per_page).limit(per_page)
    cirlce_dict = {
        'circles': [c.to_dict() for c in circles],
        'circlecount': query.count()
    }
    return jsonify(circle_dict)

@rest.route('/newcircle', methods=['POST'])
@auth.login_required
def new_circle():
    user = g.user
    name = request.json.get('name','').strip()
    address = request.json.get('address','').strip()
    area = request.json.get('area','').strip()
    time = request.json.get('time','').strip()
    if not (name and address and area and time):
        abort(403)
    note = request.json.get('note','').strip()
    circle = Circles(
        name = name
        address = address
        area = area
        time = time
        note = note
        facilitator = user
    )
    db.session.add(circle)
    db.session.commit()
    circle_dict = circle.to_dict
    return jsonify(circle_dict)

@rest.route('/editcircle/<int:circleid>', methods=['POST'])
@auth.login_required
def edit_circle(circleid):
    user = g.user
    circle = Circles.query.get_or_404(circleid)
    if circle.facilitator != user and user.role != 'Admin':
        abort(403)
    # get data
    name = request.json.get('name','').strip()
    address = request.json.get('address','').strip()
    area = request.json.get('area','').strip()
    time = request.json.get('time','').strip()
    if not (name and address and area and time):
        abort(403)
    note = request.json.get('note','').strip()
    circle.name = name
    circle.address = address
    circle.area = area
    circle.time = time
    circle.note = note
    db.session.add(circle)
    db.session.commit()
    return jsonify('Updated')

@rest.route('/delete/circle/<int:circleid>')
@auth.login_required
def del_circle(circleid):
    user = g.user
    circle = Circles.query.get_or_404(circleid)
    if circle.facilitator != user and user.role != 'Admin':
        abort(403)
    db.session.delete(circle)
    db.session.commit()
    return jsonify('Deleted')

@rest.route('/disable/circle/<int:circleid>')
@auth.login_required
def disable_circle(circleid):
    user = g.user
    circle = Circles.query.get_or_404(circleid)
    if circle.facilitator != user and user.role != 'Admin':
        abort(403)
    circle.disabled = True
    db.session.add(circle)
    db.session.commit()
    return jsonify('Disabled')

@rest.route('/recover/circle/<int:circleid>')
@auth.login_required
def recover_circle(circleid):
    user = g.user
    circle = Circles.query.get_or_404(circleid)
    if circle.facilitator != user and user.role != 'Admin':
        abort(403)
    circle.disabled = False #enable
    db.session.add(circle)
    db.session.commit()
    return jsonify('Enabled')

@rest.route('/checkparticipate/<int:circleid>')
@auth.login_required
def check_participate(circleid):
    user = g.user
    circle = Circles.query.get_or_404(circleid)
    participating = 'Cancle' if user.parting(circle) else 'Participate'
    return jsonify(participating)

@rest.route('/participate/<int:circleid>')
@auth.login_required
def participate_circle(circleid):
    user = g.user
    circle = Circles.query.get_or_404(circleid)
    user.participate(circle)
    return jsonify('Cancle')

@rest.route('/unparticipate/<int:circleid>')
@auth.login_required
def unparticipate_circle(circleid):
    user = g.user
    circle = Circles.query.get_or_404(circleid)
    user.unparticipate(circle)
    return jsonify('Paticipate')