from flask import Flask, jsonify, request
from backend.databases import database
from backend import marks_api
from backend.homework_api import get_homework, update_hash
import datetime
from flask_cors import CORS
from edutypes import *


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

@app.route('/api/students/')
async def get_students():
    db = await database.Database.setup()
    students = await db.get_students()
    return jsonify(students), 200, {'Content-Type': 'text/css; charset=utf-8'}

@app.route('/api/marks/')
async def get_marks():
    id = request.args.get('id', type = str)
    if id:
        db = await database.Database.setup()
        marks = await db.get_students_marks(await db.get_student_by_id(telegram_id=id))
        return jsonify(marks), 200, {'Content-Type': 'text/css; charset=utf-8'}
    else:
        return '404'
'''
async def homework(date, telegram_id):
    hws = []
    data = await homework_api.get_homework(date)
    db = await Database.setup()
    for hw in data:
        if not hw is None:
            hws.append(Homework(subject=hw['subject'], task=hw['task'], files=hw['files'], deadline=date, task_id=hw['id']))
            hw = hws[len(hws)-1]
            student = await db.get_student_by_id(telegram_id)
            if not await db.hw_exists(hw, student):
                await db.add_homework(hw, student)
            else:
                hws[len(hws)-1].is_done = await db.is_homework_done(hw, student)
    await db.close_connection()
    return hws
'''
@app.route('/api/homework/')
async def homework():
    date = request.args.get('date', type = str)
    if date:
        hw = await get_homework(datetime.date.fromisoformat(date))
        return jsonify(hw), 200, {'Content-Type': 'text/css; charset=utf-8'}
    else: return '404'

@app.route('/api/homework-new/')
async def homework_new():
    date = request.args.get('date', type = str)
    date = datetime.date.fromisoformat(date)
    telegram_id = request.args.get('telegramid', type = str)
    if date:
        hws = []
        data = await get_homework(date)
        db = await database.Database.setup()
        for hw in data:
            if not hw is None:
                hws.append(Homework(subject=hw['subject'], task=hw['task'], files=hw['files'], deadline=date, task_id=hw['id']))
                hw = hws[len(hws)-1]
                student = await db.get_student_by_id(telegram_id)
                if not await db.hw_exists(hw, student):
                    await db.add_homework(hw, student)
                else:
                    hws[len(hws)-1].is_done = await db.is_homework_done(hw, student)
        await db.close_connection()
        return jsonify(hws), 200, {'Content-Type': 'text/css; charset=utf-8'}
    else: return '404'
    
@app.route('/api/update-marks/')
async def update_marks():
    await marks_api.update_marks()

@app.route('/api/update-hw-hash/')
async def update_hw_hash():
    await update_hash()

app.run(port=8000)
