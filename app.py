#coding:utf8
from flask import Flask, g, abort, session, redirect, url_for, \
     request, render_template, _app_ctx_stack, jsonify
from flaskext import *
import json


app = Flask(__name__)
app.config.from_object("config")

#获得普通的英雄数据
@app.route('/getAllHeroData', methods=['POST'])
def getAllHeroData():
    res = queryAll('select * from HeroData')
    return jsonify(dict(heroData=res))
@app.route('/getUserData', methods=['POST'])
def getUserData():
    uid = request.form.get('uid', None, type=int)
    res = queryOne('select * from Users where uid = %s', (uid))
    return jsonify(dict(user=res))
@app.route('/getAllHero', methods=['POST'])
def getAllHero():
    uid = request.form.get("uid", None, type=int)
    res = queryAll('select hid, kind, level, job from Heroes where uid = %s', (uid))
    formation = queryOne('select formation from Users where uid = %s', (uid))
    return jsonify(dict(heroes=res, formation=json.loads(formation['formation'])))
@app.route('/sellHero', methods=['POST'])
def sellHero():
    uid = request.form.get('uid', None, type=int)
    heroes = request.form.get('heroes', None, type=str)
    heroes = json.loads(heroes)
    res = '(%s)'%','.join(['%s']*len(heroes))
    sql = 'delete from Heroes where uid = %s and hid in '+ res
    heroes.insert(0, uid)
    update(sql, heroes)
    return jsonify(dict(code=1))
         


@app.route('/getAllLevel', methods=['POST'])
def getAllLevel():
    res = queryAll('select * from Level')
    for r in res:
        r['formation'] = json.loads(r['formation'])
    return jsonify(dict(level=res))

@app.route('/getAllChallenge', methods=['POST'])
def getAllChallenge():
    res = queryAll('select * from Users')
    for r in res:
        r['formation'] = json.loads(r['formation'])
    return jsonify(dict(user=res))

@app.route('/getAllFriend', methods=['POST'])
def getAllFriend():
    res = queryAll('select * from Users')
    for r in res:
        heroData = queryAll('select hid, kind, level, job from Heroes where uid = %s', (r['uid']))
        r['formation'] = json.loads(r['formation'])
        r['heroData'] = heroData
    return jsonify(dict(friend=res))
@app.route('/getFormation', methods=['POST'])
def getFormation():
    uid = request.form.get('uid', None, type=int)
    res = queryOne('select formation from Users where uid = %s', (uid))
    heroes = queryAll('select hid, kind, level, job from Heroes where uid = %s', (uid))
    return jsonify(dict(formation=json.loads(res['formation']), heroes=heroes))

@app.route('/setFormation', methods=['POST'])
def setFormation():
    uid = request.form.get('uid', None, type=int)
    formation = request.form.get('formation', None, type=str)
    update('update Users set formation = %s where uid = %s', (formation, uid))
    return jsonify(dict(code=1))

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
