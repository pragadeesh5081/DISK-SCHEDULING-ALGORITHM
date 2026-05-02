"""
Utility functions for input validation and helper operations
"""

def validate_request_queue(queue_str):
    """
    Validate and parse the request queue string
    """
    if not queue_str or queue_str.strip() == "":
        return None, "Request queue cannot be empty"
    
    try:
        # Split by comma and convert to integers
        requests = [int(x.strip()) for x in queue_str.split(',')]
        
        # Validate range (0-999 for reasonable disk size)
        for req in requests:
            if req < 0 or req > 999:
                return None, f"Request {req} is out of valid range (0-999)"
        
        # Return requests in original order for FCFS
        # Other algorithms will sort as needed
        return requests, None
    
    except ValueError:
        return None, "Invalid format. Please use comma-separated integers (e.g., 98,183,37,122)"


def validate_initial_head(head_str):
    """
    Validate and parse the initial head position
    """
    if not head_str or head_str.strip() == "":
        return None, "Initial head position cannot be empty"
    
    try:
        head = int(head_str.strip())
        
        if head < 0 or head > 999:
            return None, "Head position must be between 0 and 999"
        
        return head, None
    
    except ValueError:
        return None, "Invalid head position. Please enter an integer"


def validate_disk_size(size_str):
    """
    Validate and parse the disk size
    """
    if not size_str or size_str.strip() == "":
        return 200, None  # Default value
    
    try:
        size = int(size_str.strip())
        
        if size < 10 or size > 1000:
            return None, "Disk size must be between 10 and 1000"
        
        return size, None
    
    except ValueError:
        return None, "Invalid disk size. Please enter an integer"


def format_sequence(sequence, initial_head):
    """
    Format the sequence for display
    """
    if not sequence:
        return "No requests to process"
    
    formatted = f"Head starts at {initial_head} -> "
    formatted += " -> ".join(map(str, sequence))
    return formatted


def calculate_average_seek_time(total_seek_time, num_requests):
    """
    Calculate average seek time
    """
    if num_requests == 0:
        return 0
    return round(total_seek_time / num_requests, 2)


def export_results_to_csv(results, initial_head, disk_size, direction):
    """
    Export results to CSV format (for bonus feature)
    """
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Algorithm', 'Sequence', 'Total Seek Time', 'Average Seek Time', 'Streaming Status'])
    
    # Data rows
    for algorithm, data in results.items():
        sequence_str = " -> ".join(map(str, data['sequence']))
        avg_seek = calculate_average_seek_time(data['seek_time'], len(data['sequence']))
        status, _ = data['status']
        
        writer.writerow([
            algorithm,
            sequence_str,
            data['seek_time'],
            avg_seek,
            status
        ])
    
    # Configuration info
    writer.writerow([])
    writer.writerow(['Configuration', 'Value'])
    writer.writerow(['Initial Head', initial_head])
    writer.writerow(['Disk Size', disk_size])
    writer.writerow(['Direction', direction])
    
    return output.getvalue()


def get_performance_rating(seek_time):
    """
    Get performance rating based on seek time
    """
    if seek_time < 100:
        return "Excellent", "Excellent performance with minimal seek time"
    elif seek_time < 200:
        return "Good", "Good performance with low seek time"
    elif seek_time < 400:
        return "Fair", "Fair performance with moderate seek time"
    else:
        return "Poor", "Poor performance with high seek time"


def format_results_summary(results, best_algorithm, min_seek_time):
    """
    Format results summary for display
    """
    summary = f"## Performance Summary\n\n"
    summary += f"**Best Algorithm:** {best_algorithm} (Seek Time: {min_seek_time})\n\n"
    
    # Create comparison table
    summary += "| Algorithm | Seek Time | Performance | Streaming Status |\n"
    summary += "|-----------|-----------|-------------|------------------|\n"
    
    for algorithm, data in results.items():
        seek_time = data['seek_time']
        rating, description = get_performance_rating(seek_time)
        status, color = data['status']
        
        # Add emoji for best algorithm
        algo_name = f"**{algorithm}**" if algorithm == best_algorithm else algorithm
        summary += f"| {algo_name} | {seek_time} | {rating} | {status} |\n"
    
    return summary


def validate_algorithm_selection(algorithm, requests):
    """
    Validate algorithm selection against requests
    """
    if not requests:
        return False, "No requests to process"
    
    valid_algorithms = ["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK", "ALL"]
    
    if algorithm not in valid_algorithms:
        return False, f"Invalid algorithm. Choose from: {', '.join(valid_algorithms)}"
    
    return True, None
