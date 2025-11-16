"""
Manual implementation of dictionary sorting function
"""

def sort_dicts_manual(dict_list, key):
    """
    Sort a list of dictionaries by a specific key manually
    
    Args:
        dict_list (list): List of dictionaries to sort
        key (str): Key to sort by
    
    Returns:
        list: Sorted list of dictionaries
    """
    # Using sorted() with lambda function
    return sorted(dict_list, key=lambda x: x[key])


def test_manual_implementation():
    """Test function for manual implementation"""
    # Test data
    data = [
        {'name': 'John', 'age': 25, 'salary': 50000},
        {'name': 'Alice', 'age': 30, 'salary': 60000},
        {'name': 'Bob', 'age': 20, 'salary': 45000},
        {'name': 'Carol', 'age': 35, 'salary': 70000}
    ]
    
    print("Original data:")
    for item in data:
        print(item)
    
    # Test sorting by age
    sorted_by_age = sort_dicts_manual(data, 'age')
    print("\nSorted by age:")
    for item in sorted_by_age:
        print(item)
    
    # Test sorting by salary
    sorted_by_salary = sort_dicts_manual(data, 'salary')
    print("\nSorted by salary:")
    for item in sorted_by_salary:
        print(item)


if __name__ == "__main__":
    test_manual_implementation()