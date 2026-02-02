-- Enable readable output format
.mode columns
.headers on

-- Instructions for students:
-- 1. Open SQLite in terminal: sqlite3 university.db
-- 2. Load this script: .read example.sql
-- 3. Exit SQLite: .exit


-- write your sql code here

SELECT name AS CourseName,student_id AS Students 
FROM 
Courses LEFT JOIN StudentCourses 
ON Courses.id=StudentCourses.course_id 
ORDER BY CourseName;
