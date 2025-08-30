# NL2SQL Test Report

| ID | Query | Generated SQL | Rows Returned | Message | Status |
|----|-------|---------------|---------------|---------|--------|
| 1 | List all branches and their managers' names. Include branches without a manager. | `SELECT b.name AS branch_name, COALESCE(e.name, 'No Manager') AS manager_name FROM branches b LEFT JOIN employees e ON b.manager_id = e.id;` | 50 | OK | PASS |
| 2 | Find the names of customers who have both 'checking' and 'savings' accounts. | `SELECT c.first_name, c.last_name FROM customers c JOIN accounts a ON c.id = a.customer_id WHERE a.type = 'checking' INTERSECT SELECT c.first_name, c.last_name FROM customers c JOIN accounts a ON c.id = a.customer_id WHERE a.type = 'savings';` | 0 | OK | PASS |
| 3 | List all employees who have handled a transaction for a customer born before 1960. | `SELECT DISTINCT e.name FROM employees e JOIN transactions t ON e.id = t.employee_id JOIN accounts a ON t.account_id = a.id JOIN customers c ON a.customer_id = c.id WHERE STRFTIME('%Y', c.date_of_birth) < '1960';` | 0 | OK | PASS |
| 4 | Find the total number of accounts for each customer gender. | `SELECT c.gender, COUNT(a.id) AS total_accounts FROM customers c JOIN accounts a ON c.id = a.customer_id GROUP BY c.gender;` | 0 | OK | PASS |
| 5 | For each employee position, what is the average salary, but only for positions with an average salary above 80000? | `SELECT position, AVG(salary) AS average_salary FROM employees GROUP BY position HAVING AVG(salary) > 80000;` | 12 | OK | PASS |
| 6 | Show the average transaction amount for transactions completed in the first quarter of 2025. | `SELECT AVG(amount) FROM transactions WHERE strftime('%Y-%m', transaction_date) BETWEEN '2025-01' AND '2025-03';` | 1 | OK | PASS |
| 7 | Which employees were hired in the same month as 'Raymond Jefferson'? | `SELECT id FROM employees WHERE strftime('%Y-%m', hire_date) = (SELECT strftime('%Y-%m', hire_date) FROM employees WHERE name = 'Raymond Jefferson');` | 3 | OK | PASS |
| 8 | For each customer, list their total deposit amount and total withdrawal amount. | `SELECT c.first_name, c.last_name, SUM(CASE WHEN t.type = 'deposit' THEN t.amount ELSE 0 END) AS total_deposit, SUM(CASE WHEN t.type = 'withdrawal' THEN t.amount ELSE 0 END) AS total_withdrawal FROM customers c JOIN accounts a ON c.id = a.customer_id JOIN transactions t ON a.id = t.account_id GROUP BY c.first_name, c.last_name;` | 0 | OK | PASS |
| 9 | Identify employees who have handled transactions for customers from a different branch than their own. | `SELECT e.name FROM employees e JOIN transactions t ON e.id = t.employee_id JOIN accounts a ON t.account_id = a.id JOIN customers c ON a.customer_id = c.id WHERE e.branch_id != c.branch_id;` | 0 | OK | PASS |
| 10 | Find the names of branches where the average salary of employees is higher than the overall average employee salary. | `SELECT name FROM branches WHERE id IN (SELECT branch_id FROM employees GROUP BY branch_id HAVING AVG(salary) > (SELECT AVG(salary) FROM employees));` | 24 | OK | PASS |
| 11 | List customers who have a 'credit' account and have made at least one 'fee' transaction. | `SELECT DISTINCT c.first_name, c.last_name FROM customers c JOIN accounts a ON c.id = a.customer_id JOIN transactions t ON a.id = t.account_id WHERE a.type = 'credit' AND t.type = 'fee';` | 0 | OK | PASS |
| 12 | Show customers who have the same first name but different last names. | `SELECT c1.first_name, c1.last_name FROM customers c1 JOIN customers c2 ON c1.first_name = c2.first_name AND c1.last_name != c2.last_name;` | 3006 | OK | PASS |
| 13 | List the branches where the total salary of employees is less than 500000. | `SELECT branch_id FROM employees GROUP BY branch_id HAVING SUM(salary) < 500000;` | 5 | OK | PASS |
| 14 | Show the email and phone number of customers who have a 'loan' account with a balance greater than 20000. | `SELECT c.email, c.phone FROM customers c JOIN accounts a ON c.id = a.customer_id WHERE a.type = 'loan' AND a.balance > 20000;` | 0 | OK | PASS |
| 15 | For each employee position, list the number of employees and their average salary. | `SELECT position, COUNT(*) AS num_employees, AVG(salary) AS avg_salary FROM employees GROUP BY position;` | 12 | OK | PASS |
| 16 | List all transactions that occurred on a weekend (Saturday or Sunday). | `SELECT * FROM transactions WHERE strftime('%w', transaction_date) IN ('0', '6');` | 0 | OK | PASS |
| 17 | Find the customers who have made transactions on consecutive days. | `SELECT c.first_name, c.last_name FROM customers c JOIN accounts a ON c.id = a.customer_id JOIN transactions t ON a.id = t.account_id GROUP BY c.id HAVING COUNT(DISTINCT STRFTIME('%Y-%m-%d', t.transaction_date)) > 1 AND COUNT(DISTINCT STRFTIME('%Y-%m-%d', t.transaction_date)) = SUM(CASE WHEN STRFTIME('%Y-%m-%d', t.transaction_date) = STRFTIME('%Y-%m-%d', JULIANDAY(t.transaction_date) + 1) THEN 1 ELSE 0 END);` | 0 | OK | PASS |
| 18 | List all accounts that have more deposits than withdrawals in terms of count. | `429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 15
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 22
}
]` | 0 | Exception | FAIL |
| 19 | For each customer, list their first name, last name, and the total number of transactions they made in the year 2024. | `429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 15
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 20
}
]` | 0 | Exception | FAIL |
| 20 | Find the average balance of accounts that have had at least one transaction. | `429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 15
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 18
}
]` | 0 | Exception | FAIL |
| 21 | Get the names of customers who have the same last name as their branch manager. | `SELECT c.first_name, c.last_name FROM customers c JOIN branches b ON c.branch_id = b.id JOIN employees e ON b.manager_id = e.id WHERE c.last_name = e.name;` | 0 | OK | PASS |
| 22 | List all accounts that have never had a 'withdrawal' transaction. | `429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 15
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 15
}
]` | 0 | Exception | FAIL |
| 23 | Show the average salary of employees for each branch, only considering employees hired after 2020. | `429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 15
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 14
}
]` | 0 | Exception | FAIL |
| 24 | List customers who have a total transaction amount (sum of all their transactions) greater than 50000. | `429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 15
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 12
}
]` | 0 | Exception | FAIL |
| 25 | Find the branch with the most diverse set of employee positions. | `429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 15
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 10
}
]` | 0 | Exception | FAIL |
| 26 | Find the total number of customers for each gender, excluding 'prefer_not_to_say'. | `429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 15
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 9
}
]` | 0 | Exception | FAIL |
| 27 | List all customers who have exactly two accounts. | `429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 15
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 7
}
]` | 0 | Exception | FAIL |
| 28 | Get the names of branches that have no managers assigned yet. | `429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 15
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 6
}
]` | 0 | Exception | FAIL |
| 29 | Show the names of branches that have an employee named 'Michael'. | `429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 15
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 4
}
]` | 0 | Exception | FAIL |
| 30 | List customers who share the same address with another customer. | `429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 15
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 3
}
]` | 0 | Exception | FAIL |
| 31 | Find the branch that has the highest number of 'completed' transactions. | `429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 15
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 3
}
]` | 0 | Exception | FAIL |
| 32 | Show the names of employees who have never handled a 'failed' transaction. | `429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 15
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 2
}
]` | 0 | Exception | FAIL |
| 33 | List customers who have a credit account and a loan account, and their combined balance for these two types is greater than 30000. | `SELECT c.first_name, c.last_name, SUM(a.balance) AS combined_balance FROM customers c JOIN accounts a ON c.id = a.customer_id WHERE a.type IN ('credit', 'loan') GROUP BY c.id HAVING SUM(a.balance) > 30000;` | 0 | OK | PASS |
| 34 | Find the average balance of accounts for customers whose age is between 30 and 40. | `SELECT AVG(T1.balance) FROM accounts AS T1 INNER JOIN customers AS T2 ON T1.customer_id = T2.id WHERE STRFTIME('%Y', 'now') - STRFTIME('%Y', T2.date_of_birth) BETWEEN 30 AND 40;` | 1 | OK | PASS |
| 35 | Show the names of branches that have at least one employee from every position type present in the 'employees' table. | `SELECT T1.name FROM branches AS T1 JOIN employees AS T2 ON T1.id = T2.branch_id GROUP BY T1.name HAVING count(DISTINCT T2.position) = (SELECT count(DISTINCT position) FROM employees);` | 0 | OK | PASS |
