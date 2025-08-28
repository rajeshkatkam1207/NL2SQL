
-- Banking sample schema and sample rows
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT
);

CREATE TABLE IF NOT EXISTS accounts (
    account_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    account_type TEXT,
    balance REAL,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS transactions (
    tx_id INTEGER PRIMARY KEY,
    account_id INTEGER,
    amount REAL,
    tx_date TEXT,
    description TEXT,
    FOREIGN KEY(account_id) REFERENCES accounts(account_id)
);

DELETE FROM transactions;
DELETE FROM accounts;
DELETE FROM customers;

INSERT INTO customers(customer_id, name, city) VALUES
  (1, 'Alice Gupta', 'Hyderabad'),
  (2, 'Ramesh Kumar', 'Mumbai'),
  (3, 'Sunita Rao', 'Chennai');

INSERT INTO accounts(account_id, customer_id, account_type, balance) VALUES
  (101, 1, 'savings', 12000.50),
  (102, 1, 'current', 5000.00),
  (201, 2, 'savings', 25000.00),
  (301, 3, 'savings', 300.75);

INSERT INTO transactions(tx_id, account_id, amount, tx_date, description) VALUES
  (1, 101, -500.00, '2025-07-01', 'ATM withdrawal'),
  (2, 101, 2000.00, '2025-07-03', 'Salary credit'),
  (3, 201, -1500.00, '2025-07-04', 'Online transfer'),
  (4, 301, -50.00, '2025-07-05', 'POS purchase');
