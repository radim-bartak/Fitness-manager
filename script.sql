CREATE TABLE member(
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(50) NOT NULL,
phone VARCHAR(20) NOT NULL,
email VARCHAR(50) NOT NULL UNIQUE,
active_membership BOOLEAN NOT NULL,
registration_date DATE NOT NULL
);

CREATE TABLE membership(
id INT PRIMARY KEY AUTO_INCREMENT,
member_id INT NOT NULL,
type ENUM('Monthly', 'Three-month', 'Yearly') NOT NULL,
price FLOAT NOT NULL,
valid_from DATE NOT NULL,
valid_to DATE NOT NULL,
FOREIGN KEY (member_id) REFERENCES member(id)
);

CREATE TABLE trainer(
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(50) NOT NULL,
specialization VARCHAR(50) NOT NULL,
phone VARCHAR(20),
email VARCHAR(50) UNIQUE
);

CREATE TABLE class(
id INT PRIMARY KEY AUTO_INCREMENT,
trainer_id INT NOT NULL,
name VARCHAR(50) NOT NULL,
capacity INT NOT NULL,
start_time DATETIME NOT NULL,
canceled BOOLEAN NOT NULL DEFAULT FALSE,
FOREIGN KEY (trainer_id) REFERENCES trainer(id)
);

CREATE TABLE reservation(
id INT PRIMARY KEY AUTO_INCREMENT,
member_id INT NOT NULL,
class_id INT NOT NULL,
reservation_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (member_id) REFERENCES member(id),
FOREIGN KEY (class_id) REFERENCES class(id)
);

CREATE TABLE payment(
id INT AUTO_INCREMENT PRIMARY KEY,
member_id INT NOT NULL,
membership_id INT,
total_price FLOAT NOT NULL,
payment_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
payment_method ENUM('Cash', 'Card', 'Online') NOT NULL,
FOREIGN KEY (member_id) REFERENCES member(id),
FOREIGN KEY (membership_id) REFERENCES membership(id)
);

CREATE VIEW active_members AS
SELECT m.id, m.name, m.email, ms.type, ms.valid_to
FROM member m
INNER JOIN membership ms ON m.id = ms.member_id
WHERE ms.valid_to >= CURDATE();

CREATE VIEW class_statistics AS
SELECT c.name, c.capacity, COUNT(r.id) AS reservations_count, t.name AS trainer
FROM class c
LEFT JOIN reservation r ON c.id = r.class_id
INNER JOIN trainer t ON t.id = c.trainer_id
GROUP BY c.id;

