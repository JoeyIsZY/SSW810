"""@Author: JoeyIsZY
"""
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def homepage():
    return "HW12_yu_zhou \n" + "Please enter */instructor_summary_table to access the table page."


@app.route('/instructor_summary_table')
def table_page():
    dbpath = '/Applications/DataGrip.app/Contents/bin/810_starup.db'

    try:
        db = sqlite3.connect(dbpath)
    except sqlite3.OperationalError:
        return f'Error: Unable to open database at {dbpath}'
    else:
        query = """select t.CWID, t.Name, t.Dept, g.Course, count(*) as Students from grades g 
                    join instructors t on g.InstructorCWID=t.CWID group by t.CWID,t.Name,t.Dept,g.Course"""

        data = [{'cwid': cwid, 'name': name, 'dept': dept, 'courses': courses, 'students': students}
                for cwid, name, dept, courses, students in db.execute(query)]

        db.close()

        return render_template(
            'instructor_summary_table.html',
            title='Stevens Repository',
            table_title='The number of student by course and teacher',
            students=data)


if __name__ == "__main__":
    app.run(debug=True)