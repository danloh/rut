# -*- coding: utf-8 -*-
# circle : challenge circle, a group people who challege a rut together

from flask import request, g, jsonify, abort
from ..models import Circles
from . import db, rest, auth, PER_PAGE


@rest.route('/circles', methods=['GET'])
@auth.login_required
def get_circles():
    # get request params
    area = request.args.get('area', '').strip()
    # query
    query = Circles.query.filter(Circles.disabled == None)
    if area:
        if area == "[]":
            query = query.filter_by(facilitator=g.user)
        else:
            query = query.filter(Circles.address.contains(area))
    # pagination
    page = request.args.get('page', 0, type=int)
    per_page = request.args.get('perPage', PER_PAGE, type=int)
    circles = query.order_by(Circles.timestamp.desc())\
                   .offset(page*per_page).limit(per_page)
    circle_dict = {
        'circles': [c.to_dict() for c in circles],
        'circlecount': query.count()
    }
    return jsonify(circle_dict)


@rest.route('/circles', methods=['POST'])
@auth.login_required
def new_circle():
    name = request.json.get('name', '').strip()
    address = request.json.get('address', '').strip()
    time = request.json.get('time', '').strip()
    if not (name and address and time):
        abort(403)
    note = request.json.get('note', '').strip()
    user = g.user
    circle = Circles(
        name=name,
        address=address,
        time=time,
        note=note,
        facilitator=user
    )
    db.session.add(circle)
    db.session.commit()
    circle_dict = circle.to_dict()
    return jsonify(circle_dict)


@rest.route('/circles/<int:circleid>', methods=['PUT'])
@auth.login_required
def edit_circle(circleid):
    circle = Circles.query.get_or_404(circleid)
    user = g.user
    if circle.facilitator != user and user.role != 'Admin':
        abort(403)
    # get data
    name = request.json.get('name', '').strip()
    address = request.json.get('address', '').strip()
    time = request.json.get('time', '').strip()
    if not (name and address and time):
        abort(403)
    note = request.json.get('note', '').strip()
    circle.name = name
    circle.address = address
    circle.time = time
    circle.note = note
    db.session.add(circle)
    db.session.commit()
    return jsonify(circle.to_dict())


@rest.route('/circles/<int:circleid>', methods=['DELETE'])
@auth.login_required
def del_circle(circleid):
    circle = Circles.query.get_or_404(circleid)
    user = g.user
    if circle.facilitator != user and user.role != 'Admin':
        abort(403)
    db.session.delete(circle)
    db.session.commit()
    return jsonify('Deleted')


@rest.route('/circles/<int:circleid>/disabled', methods=['PATCH'])
@auth.login_required
def disable_circle(circleid):
    circle = Circles.query.get_or_404(circleid)
    user = g.user
    # if circle.facilitator != user and user.role != 'Admin':
    #     abort(403)
    # dis_or_enb = request.json.get('disbaled', True)
    circle.disabled = True  # dis_or_enb
    db.session.add(circle)
    db.session.commit()
    return jsonify(circle.disabled)


@rest.route('/circles/<int:circleid>/part', methods=['GET'])
@auth.login_required
def check_participate(circleid):
    circle = Circles.query.get_or_404(circleid)
    user = g.user
    participating = 'Cancle' if user.parting(circle) else 'Participate'
    return jsonify(participating)


@rest.route('/circles/<int:circleid>/participates', methods=['GET'])
@auth.login_required
def get_who_participate_circle(circleid):
    circle = Circles.query.get_or_404(circleid)
    participators = circle.participators
    part_list = [p.to_simple_dict() for p in participators]
    part_dict = {
        'participators': part_list,
        'count': participators.count()
    }
    return jsonify(part_dict)


@rest.route('/circles/<int:circleid>/participates', methods=['PATCH'])
@auth.login_required
def participate_circle(circleid):
    circle = Circles.query.get_or_404(circleid)
    user = g.user
    user.participate(circle)
    return jsonify('Cancle')


@rest.route('/circles/<int:circleid>/participates', methods=['DELETE'])
@auth.login_required
def unparticipate_circle(circleid):
    circle = Circles.query.get_or_404(circleid)
    user = g.user
    user.unparticipate(circle)
    return jsonify('Paticipate')
