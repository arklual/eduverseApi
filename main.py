from flask import Flask, jsonify, request
from backend.databases import database
from backend import marks_api
from backend.homework_api import get_homework
import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

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

@app.route('/api/homework/')
async def homework():
    date = request.args.get('date', type = str)
    if date:
        if date == 'tommorow': date = datetime.date.today().isoformat()
        hw = await get_homework(datetime.date.fromisoformat(date))
        return jsonify(hw), 200, {'Content-Type': 'text/css; charset=utf-8'}
    else: return '404'
    
@app.route('/api/update/')
async def update_marks():
    await marks_api.update_marks()
