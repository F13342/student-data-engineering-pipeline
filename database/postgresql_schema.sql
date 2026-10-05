CREATE TABLE IF NOT EXISTS courses (
    course_code VARCHAR(20) PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    credit_hours INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS enrollments (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL,
    course_code VARCHAR(20) NOT NULL REFERENCES courses(course_code),
    semester VARCHAR(20) NOT NULL
);

INSERT INTO courses (course_code, course_name, credit_hours)
VALUES
('CS101', 'Programming', 3),
('CS102', 'Data Engineering', 3),
('IS101', 'Information Systems', 3)
ON CONFLICT (course_code) DO NOTHING;

INSERT INTO enrollments (student_id, course_code, semester)
VALUES
('S001', 'CS101', '2026-1'),
('S002', 'CS101', '2026-1'),
('S003', 'IS101', '2026-1'),
('S004', 'CS102', '2026-1'),
('S005', 'CS101', '2026-1');

