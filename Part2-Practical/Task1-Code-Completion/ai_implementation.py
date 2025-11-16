"""
AI-suggested implementation using GitHub Copilot patterns
"""

def sort_dicts_ai(dict_list, key, default_value=0):
    """
    Sort a list of dictionaries by a specific key with AI enhancements
    
    Args:
        dict_list (list): List of dictionaries to sort
        key (str): Key to sort by
        default_value: Default value if key is missing
    
    Returns:
        list: Sorted list of dictionaries
    """
    # AI-suggested: Using get() method with default value for missing keys
    return sorted(dict_list, key=lambda x: x.get(key, default_value))


def sort_dicts_safe(dict_list, key):
    """
    AI-suggested safe sorting with comprehensive error handling
    """
    try:
        # Filter out dictionaries missing the key
        valid_dicts = [d for d in dict_list if key in d]
        invalid_dicts = [d for d in dict_list if key not in d]
        
        if invalid_dicts:
            print(f"Warning: {len(invalid_dicts)} dictionaries missing key '{key}'")
        
        # Sort valid dictionaries
        sorted_list = sorted(valid_dicts, key=lambda x: x[key])
        
        # Append invalid dictionaries at the end
        return sorted_list + invalid_dicts
        
    except Exception as e:
        print(f"Error during sorting: {e}")
        return dict_list


def test_ai_implementations():
    """Test function for AI implementations"""
    # Test data with potential missing keys
    data = [
        {'name': 'John', 'age': 25, 'salary': 50000},
        {'name': 'Alice', 'age': 30},  # Missing salary
        {'name': 'Bob', 'salary': 45000},  # Missing age
        {'name': 'Carol', 'age': 35, 'salary': 70000}
    ]
    
    print("Original data:")
    for item in data:
        print(item)
    
    # Test basic AI implementation
    print("\nBasic AI implementation (sort by age):")
    sorted_basic = sort_dicts_ai(data, 'age')
    for item in sorted_basic:
        print(item)
    
    # Test safe implementation
    print("\nSafe AI implementation (sort by age):")
    sorted_safe = sort_dicts_safe(data, 'age')
    for item in sorted_safe:
        print(item)
    
    # Test with missing key
    print("\nSafe AI implementation (sort by salary):")
    sorted_salary = sort_dicts_safe(data, 'salary')
    for item in sorted_salary:
        print(item)


if __name__ == "__main__":
    test_ai_implementations()