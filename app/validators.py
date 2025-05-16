def validate_employee(data):
    required_fields = ['first_name', 'last_name', 'department_id', 'hire_date', 'job_title']
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
        if isinstance(data[field], str) and not data[field].strip():
            return False, f"The field '{field}' cannot be empty"
    
    # Validate that department_id is a positive integer
    try:
        if int(data['department_id']) <= 0:
            return False, "The field 'department_id' must be a positive integer"
    except ValueError:
        return False, "The field 'department_id' must be an integer"

    # Validate hire_date (basic format YYYY-MM-DD)
    import re
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    if not date_pattern.match(data['hire_date']):
        return False, "The field 'hire_date' must be in format YYYY-MM-DD"

    return True, "Valid data"