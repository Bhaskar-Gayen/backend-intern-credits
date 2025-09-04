CREATE SCHEMA IF NOT EXISTS credit_db;

-- Switch to schema
SET search_path TO credit_db;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE credits (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    credits INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX idx_credits_user_id ON credits(user_id);
CREATE INDEX idx_users_email ON users(email);

-- Insert some sample data
INSERT INTO users (email, name) VALUES
('john@example.com', 'John Doe'),
('jane@example.com', 'Jane Smith'),
('bob@example.com', 'Bob Johnson');

INSERT INTO credits (user_id, credits) VALUES
(1, 100),
(2, 50),
(3, 75);