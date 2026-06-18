USE smart_civic;

INSERT INTO complaint_status (name, description) VALUES
('Open', 'Complaint has been filed and is waiting for assignment.'),
('In Progress', 'Complaint has been assigned and work is underway.'),
('Resolved', 'Complaint has been addressed and resolved.');

INSERT INTO categories (name, description) VALUES
('Road damage', 'Broken roads, potholes, and pavement failures.'),
('Garbage issues', 'Trash collection, overflowing bins, and littering.'),
('Street light failure', 'Non-functioning or flickering street lights.'),
('Water leakage', 'Broken pipes, leaks, or flooding issues.'),
('Drainage blockage', 'Clogged drains and stormwater backups.');

INSERT INTO users (name, email, password_hash, role, phone, address)
VALUES
('Admin User', 'admin@smartcivic.local', '$2b$12$QbZ6jJv8dE0AxG7ukc7eRuLx3CB1rjJP7F8R/WcLCpQVd7Hx7xj6W', 'admin', '0000000000', 'City Hall'),
('Jane Citizen', 'jane.user@example.com', '$2b$12$QbZ6jJv8dE0AxG7ukc7eRuLx3CB1rjJP7F8R/WcLCpQVd7Hx7xj6W', 'citizen', '555-0123', '12 Civic Lane'),
('Officer Joe', 'joe.officer@example.com', '$2b$12$QbZ6jJv8dE0AxG7ukc7eRuLx3CB1rjJP7F8R/WcLCpQVd7Hx7xj6W', 'officer', '555-0456', 'Central Station');

INSERT INTO officers (user_id, department, assigned_area) VALUES
((SELECT id FROM users WHERE email = 'joe.officer@example.com'), 'Public Works', 'Downtown');

INSERT INTO complaints (user_id, category_id, status_id, description, latitude, longitude, image_url)
VALUES
((SELECT id FROM users WHERE email = 'jane.user@example.com'), (SELECT id FROM categories WHERE name = 'Road damage'), (SELECT id FROM complaint_status WHERE name = 'Open'), 'Pothole near the main street intersection.', 37.7749, -122.4194, 'https://via.placeholder.com/640x360.png'),
((SELECT id FROM users WHERE email = 'jane.user@example.com'), (SELECT id FROM categories WHERE name = 'Street light failure'), (SELECT id FROM complaint_status WHERE name = 'In Progress'), 'Streetlight remains dark for three nights.', 37.7750, -122.4180, 'https://via.placeholder.com/640x360.png');
