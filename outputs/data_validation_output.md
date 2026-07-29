```json
{
  "validation_results": [
    {
      "employee_id": "EMP001",
      "status": "valid",
      "errors": []
    },
    {
      "employee_id": "EMP002",
      "status": "invalid",
      "errors": [
        "Name is required and cannot be empty",
        "Email address is invalid: 'sarah.johnson@example' does not follow valid email format",
        "Phone number is invalid: '555-ABC-1234' contains invalid characters (letters)",
        "Age is invalid: 17 is below the minimum required age of 18",
        "Salary is invalid: -5000 must be greater than 0",
        "Department is invalid: 'IT' is not in the allowed list (Engineering, Human Resources, Finance, Marketing, Sales, Operations)",
        "Joining date is invalid: '15/08/2024' does not follow the required format YYYY-MM-DD"
      ]
    },
    {
      "employee_id": "EMP003",
      "status": "valid",
      "errors": []
    }
  ],
  "summary": {
    "total_records": 3,
    "valid_records": 2,
    "invalid_records": 1
  }
}
```