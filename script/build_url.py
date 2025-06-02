def uid_to_url(uid):
    """
    Convert a UID to an impresso-project URL.
    
    Args:
        uid (str): UID in format like 'luxwort-1925-02-21-a-i0054'
    
    Returns:
        str: Complete URL for the impresso-project
    
    Example:
        >>> uid_to_url('luxwort-1925-02-21-a-i0054')
        'https://impresso-project.ch/app/issue/luxwort-1925-02-21-a/view?articleId=i0054'
    """
    # Find the last occurrence of '-i' to split issue and article parts
    last_dash_i = uid.rfind('-i')
    
    if last_dash_i == -1:
        raise ValueError(f"Invalid UID format: {uid}. Expected format with '-i' separator.")
    
    # Split into issue_id and article_id
    issue_id = uid[:last_dash_i]
    article_id = uid[last_dash_i + 1:]  # Remove the '-' prefix
    
    # Construct the URL
    url = f"https://impresso-project.ch/app/issue/{issue_id}/view?articleId={article_id}"
    
    return url


# Example usage and test
if __name__ == "__main__":
    # Test with your example
    test_uid = "luxwort-1925-02-21-a-i0054"
    result = uid_to_url(test_uid)
    print(f"Input UID: {test_uid}")
    print(f"Generated URL: {result}")
    
    # Test with other examples
    test_cases = [
        "indeplux-1893-02-07-a-i0019",
        "luxwort-1924-03-01-a-i0045"
    ]
    
    for uid in test_cases:
        print(f"\nUID: {uid}")
        print(f"URL: {uid_to_url(uid)}")