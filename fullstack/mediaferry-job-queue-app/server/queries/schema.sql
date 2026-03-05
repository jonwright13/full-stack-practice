-- schema.sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TYPE job_status AS ENUM('pending', 'completed', 'failed', 'processing');
CREATE TYPE job_type AS ENUM('image_process', 'csv_transform');

CREATE TABLE jobs (
  id SERIAL PRIMARY KEY,
  file_name VARCHAR(100) NOT NULL,
  job_type job_type NOT NULL,
  status job_status DEFAULT 'pending',
  submitted_by VARCHAR(100) NOT NULL,
  user_id INTEGER REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- seed some users
INSERT INTO users (name, email)
VALUES ('bob', 'bob@bob.com'), ('jon', 'jon@wright.com'), ('mary', 'mary@gmail.com'), ('rick', 'rick@bobby.com');

-- seed some jobs
INSERT INTO jobs (file_name, job_type, status, submitted_by, user_id)
VALUES 
('file1.csv', 'csv_transform', 'pending', 'jon@wright.com', (SELECT id FROM users WHERE email = 'jon@wright.com')), 
('file2.png', 'image_process', 'completed', 'mary@gmail.com', (SELECT id FROM users WHERE email = 'mary@gmail.com')),
('file3.jpg', 'image_process', 'failed', 'rick@bobby.com', (SELECT id FROM users WHERE email = 'rick@bobby.com')),
('file4.csv', 'csv_transform', 'completed', 'bob@bob.com', (SELECT id FROM users WHERE email = 'bob@bob.com'));


-- Updated at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER jobs_updated_at
BEFORE UPDATE ON jobs
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();