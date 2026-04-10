-- ============================================================
--  CPE Repository Management System — Database Setup
--  Run this file once in MariaDB to set everything up
-- ============================================================

CREATE DATABASE IF NOT EXISTS repository;
USE repository;

-- 1. STUDENT
CREATE TABLE IF NOT EXISTS students (
    student_id   INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    email        VARCHAR(100) UNIQUE,
    course       VARCHAR(50)  DEFAULT 'CPE',
    year_level   VARCHAR(20)
);

-- 2. TEAM
CREATE TABLE IF NOT EXISTS team (
    team_id   INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL
);

-- 3. TEAM_MEMBER (links students to teams)
CREATE TABLE IF NOT EXISTS team_member (
    teammember_id INT AUTO_INCREMENT PRIMARY KEY,
    team_id       INT NOT NULL,
    student_id    INT NOT NULL,
    FOREIGN KEY (team_id)    REFERENCES team(team_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- 4. ADVISER
CREATE TABLE IF NOT EXISTS advisers (
    adviser_id   INT AUTO_INCREMENT PRIMARY KEY,
    adviser_name VARCHAR(100) NOT NULL,
    email        VARCHAR(100) UNIQUE
);

-- 5. PANELIST
CREATE TABLE IF NOT EXISTS panelists (
    panelist_id   INT AUTO_INCREMENT PRIMARY KEY,
    panelist_name VARCHAR(100) NOT NULL,
    email         VARCHAR(100) UNIQUE
);

-- 6. PROJECT
CREATE TABLE IF NOT EXISTS projects (
    project_id   INT AUTO_INCREMENT PRIMARY KEY,
    title        VARCHAR(255) NOT NULL,
    description  TEXT,
    year_completed INT,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    status       VARCHAR(50)  DEFAULT 'Active',
    team_id      INT,
    FOREIGN KEY (team_id) REFERENCES team(team_id)
);

-- 7. PROJECT_ADVISER (links adviser to project)
CREATE TABLE IF NOT EXISTS project_adviser (
    adviserproject_id INT AUTO_INCREMENT PRIMARY KEY,
    adviser_id        INT,
    project_id        INT,
    FOREIGN KEY (adviser_id) REFERENCES advisers(adviser_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- 8. PROJECT_PANELIST (links panelists to project)
CREATE TABLE IF NOT EXISTS project_panelist (
    projectpanelist_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id         INT,
    panelist_id        INT,
    FOREIGN KEY (project_id)  REFERENCES projects(project_id),
    FOREIGN KEY (panelist_id) REFERENCES panelists(panelist_id)
);

-- 9. PROJECT_FILES
CREATE TABLE IF NOT EXISTS project_files (
    file_id    INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    file_name  VARCHAR(255),
    file_path  VARCHAR(255),
    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- ============================================================
--  SAMPLE DATA — delete this section if you want a clean DB
-- ============================================================

INSERT IGNORE INTO students (student_name, email, course, year_level) VALUES
('Juan dela Cruz',   'juan.delacruz@tip.edu.ph',   'CPE', '4'),
('Maria Santos',     'maria.santos@tip.edu.ph',     'CPE', '3'),
('Carlo Reyes',      'carlo.reyes@tip.edu.ph',      'CPE', '4'),
('Ana Gonzales',     'ana.gonzales@tip.edu.ph',     'CPE', '2');

INSERT IGNORE INTO advisers (adviser_name, email) VALUES
('Prof. Roberto Cruz',    'roberto.cruz@tip.edu.ph'),
('Prof. Linda Flores',    'linda.flores@tip.edu.ph');

INSERT IGNORE INTO panelists (panelist_name, email) VALUES
('Prof. Eduardo Lim',   'eduardo.lim@tip.edu.ph'),
('Prof. Susan Tan',     'susan.tan@tip.edu.ph');

INSERT IGNORE INTO team (team_name) VALUES
('Team Alpha'),
('Team Beta');

INSERT IGNORE INTO projects (title, description, year_completed, status, team_id) VALUES
('Smart Attendance System',   'An IoT-based attendance tracking system using RFID.',         2024, 'Completed', 1),
('CPE Repository System',     'A centralized system to manage and store CPE projects.',       2024, 'Active',    2),
('Home Automation using ESP', 'Controls home appliances remotely via mobile application.',   2023, 'Completed', 1);

INSERT IGNORE INTO team_member (team_id, student_id) VALUES
(1, 1), (1, 2),
(2, 3), (2, 4);

INSERT IGNORE INTO project_adviser (adviser_id, project_id) VALUES
(1, 1), (2, 2), (1, 3);

INSERT IGNORE INTO project_panelist (project_id, panelist_id) VALUES
(1, 1), (1, 2),
(2, 1),
(3, 2);
