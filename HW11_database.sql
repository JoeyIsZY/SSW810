select CWID, Name from HW11_instructors
where CWID = '98763'

select Dept, count(*) as cnt
from HW11_instructors group by Dept

select Grade, max(cnt)
from (select Grade, count(*) as cnt from "HW11_grades" group by Grade)

select s.Name, s.CWID, s.Major, g.Course, g.Grade
from HW11_students s
    join HW11_grades g on s.CWID=g.Student_CWID

select s.Name, s.CWID, s.Major, g.Course, g.Grade
from HW11_students s
    join HW11_grades g on s.CWID=g.Student_CWID
where g.Course = 'SSW 810'

CREATE TABLE instructors_summary (
    CWID    TEXT  UNSIGNED NOT NULL,
    Name	TEXT    NOT NULL,
    Dept	TEXT    NOT NULL,
    course	TEXT	NOT NULL,
    stuNum	TEXT	NOT NULL
);




