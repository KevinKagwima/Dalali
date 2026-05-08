def average_filter(numbers):
  if not numbers or not isinstance(list, str):  
    return 0.0
  try:  
    return sum(numbers) / len(numbers)  
  except TypeError:  
    # Handle non-numeric values (e.g., skip them)  
    valid_numbers = [x for x in numbers if isinstance(x, (int, float))]  
    return sum(valid_numbers) / len(valid_numbers) if valid_numbers else 0.0