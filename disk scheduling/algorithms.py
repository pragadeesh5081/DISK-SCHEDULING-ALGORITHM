"""
Disk Scheduling Algorithms Implementation
Contains FCFS, SSTF, SCAN, C-SCAN, LOOK, and C-LOOK algorithms
"""

def fcfs(requests, initial_head):
    """
    First Come First Serve Algorithm
    Processes requests in the order they arrive
    """
    if not requests:
        return [], 0
    
    sequence = [initial_head] + requests
    seek_time = 0
    
    for i in range(1, len(sequence)):
        seek_time += abs(sequence[i] - sequence[i-1])
    
    return requests, seek_time


def sstf(requests, initial_head):
    """
    Shortest Seek Time First Algorithm
    Always serves the request closest to current head position
    """
    if not requests:
        return [], 0
    
    requests_copy = requests.copy()
    sequence = []
    current_head = initial_head
    seek_time = 0
    
    while requests_copy:
        # Find the closest request
        closest_index = 0
        closest_distance = abs(requests_copy[0] - current_head)
        
        for i in range(1, len(requests_copy)):
            distance = abs(requests_copy[i] - current_head)
            if distance < closest_distance:
                closest_distance = distance
                closest_index = i
        
        # Serve the closest request
        next_request = requests_copy.pop(closest_index)
        sequence.append(next_request)
        seek_time += closest_distance
        current_head = next_request
    
    return sequence, seek_time


def scan(requests, initial_head, disk_size=200, direction="right"):
    """
    SCAN Algorithm (Elevator Algorithm)
    Moves in one direction, serves all requests, then reverses
    """
    if not requests:
        return [], 0
    
    requests_copy = requests.copy()
    sequence = []
    current_head = initial_head
    seek_time = 0
    
    # Separate requests based on current head position
    left_requests = [r for r in requests_copy if r < current_head]
    right_requests = [r for r in requests_copy if r >= current_head]
    
    # Sort requests in each direction
    left_requests.sort(reverse=True)  # Descending for left movement
    right_requests.sort()             # Ascending for right movement
    
    if direction == "right":
        # Move right first
        sequence.extend(right_requests)
        # Calculate seek time for right movement
        if right_requests:
            seek_time += right_requests[-1] - current_head
            current_head = right_requests[-1]
        
        # Go to the end of disk
        seek_time += (disk_size - 1) - current_head
        current_head = disk_size - 1
        
        # Move left
        sequence.extend(left_requests)
        if left_requests:
            seek_time += current_head - left_requests[-1]
    else:
        # Move left first
        sequence.extend(left_requests)
        # Calculate seek time for left movement
        if left_requests:
            seek_time += current_head - left_requests[-1]
            current_head = left_requests[-1]
        
        # Go to the beginning of disk
        seek_time += current_head - 0
        current_head = 0
        
        # Move right
        sequence.extend(right_requests)
        if right_requests:
            seek_time += right_requests[-1] - current_head
    
    return sequence, seek_time


def c_scan(requests, initial_head, disk_size=200, direction="right"):
    """
    C-SCAN Algorithm (Circular SCAN)
    Moves in one direction, serves all requests, jumps to beginning
    """
    if not requests:
        return [], 0
    
    requests_copy = requests.copy()
    sequence = []
    current_head = initial_head
    seek_time = 0
    
    # Separate requests based on current head position
    left_requests = [r for r in requests_copy if r < current_head]
    right_requests = [r for r in requests_copy if r >= current_head]
    
    # Sort requests
    left_requests.sort()
    right_requests.sort()
    
    if direction == "right":
        # Move right first
        sequence.extend(right_requests)
        if right_requests:
            seek_time += right_requests[-1] - current_head
            current_head = right_requests[-1]
        
        # Jump to beginning (circular movement)
        if left_requests:
            seek_time += (disk_size - 1) - current_head
            seek_time += (disk_size - 1) - 0
            current_head = 0
            
            # Continue right movement
            sequence.extend(left_requests)
            seek_time += left_requests[-1] - current_head
    else:
        # Move left first
        sequence.extend(left_requests)
        if left_requests:
            seek_time += current_head - left_requests[-1]
            current_head = left_requests[-1]
        
        # Jump to end (circular movement)
        if right_requests:
            seek_time += current_head - 0
            seek_time += (disk_size - 1) - 0
            current_head = disk_size - 1
            
            # Continue left movement
            sequence.extend(right_requests)
            seek_time += current_head - right_requests[-1]
    
    return sequence, seek_time


def look(requests, initial_head, disk_size=200, direction="right"):
    """
    LOOK Algorithm (Optimized SCAN)
    Moves only till the last request in that direction, then reverses
    Does NOT go to disk end unnecessarily
    """
    if not requests:
        return [], 0
    
    requests_copy = requests.copy()
    sequence = []
    current_head = initial_head
    seek_time = 0
    
    # Separate requests based on current head position
    left_requests = [r for r in requests_copy if r < current_head]
    right_requests = [r for r in requests_copy if r >= current_head]
    
    # Sort requests in each direction
    left_requests.sort(reverse=True)  # Descending for left movement
    right_requests.sort()             # Ascending for right movement
    
    if direction == "right":
        # Move right first
        sequence.extend(right_requests)
        if right_requests:
            seek_time += right_requests[-1] - current_head
            current_head = right_requests[-1]
        
        # Move left (no need to go to disk end)
        sequence.extend(left_requests)
        if left_requests:
            seek_time += current_head - left_requests[-1]
    else:
        # Move left first
        sequence.extend(left_requests)
        if left_requests:
            seek_time += current_head - left_requests[-1]
            current_head = left_requests[-1]
        
        # Move right (no need to go to disk end)
        sequence.extend(right_requests)
        if right_requests:
            seek_time += right_requests[-1] - current_head
    
    return sequence, seek_time


def c_look(requests, initial_head, disk_size=200, direction="right"):
    """
    C-LOOK Algorithm (Optimized C-SCAN)
    Moves only till last request, jumps directly to first request
    """
    if not requests:
        return [], 0
    
    requests_copy = requests.copy()
    sequence = []
    current_head = initial_head
    seek_time = 0
    
    # Separate requests based on current head position
    left_requests = [r for r in requests_copy if r < current_head]
    right_requests = [r for r in requests_copy if r >= current_head]
    
    # Sort requests
    left_requests.sort()
    right_requests.sort()
    
    if direction == "right":
        # Move right first
        sequence.extend(right_requests)
        if right_requests:
            seek_time += right_requests[-1] - current_head
            current_head = right_requests[-1]
        
        # Jump directly to first request (circular movement)
        if left_requests:
            seek_time += current_head - left_requests[0]
            current_head = left_requests[0]
            
            # Continue right movement
            sequence.extend(left_requests)
            seek_time += left_requests[-1] - current_head
    else:
        # Move left first
        sequence.extend(left_requests)
        if left_requests:
            seek_time += current_head - left_requests[-1]
            current_head = left_requests[-1]
        
        # Jump directly to last request (circular movement)
        if right_requests:
            seek_time += right_requests[-1] - current_head
            current_head = right_requests[-1]
            
            # Continue left movement
            sequence.extend(right_requests)
            seek_time += current_head - right_requests[0]
    
    return sequence, seek_time


def get_streaming_status(seek_time):
    """
    Determine streaming status based on seek time
    """
    if seek_time < 200:
        return "Smooth Playback", "green"
    elif seek_time < 400:
        return "Moderate Streaming", "orange"
    else:
        return "Buffering... Poor Performance", "red"


def run_all_algorithms(requests, initial_head, disk_size=200, direction="right"):
    """
    Run all algorithms and return results
    """
    results = {}
    
    # FCFS
    sequence, seek_time = fcfs(requests, initial_head)
    results["FCFS"] = {
        "sequence": sequence,
        "seek_time": seek_time,
        "status": get_streaming_status(seek_time)
    }
    
    # SSTF
    sequence, seek_time = sstf(requests, initial_head)
    results["SSTF"] = {
        "sequence": sequence,
        "seek_time": seek_time,
        "status": get_streaming_status(seek_time)
    }
    
    # SCAN
    sequence, seek_time = scan(requests, initial_head, disk_size, direction)
    results["SCAN"] = {
        "sequence": sequence,
        "seek_time": seek_time,
        "status": get_streaming_status(seek_time)
    }
    
    # C-SCAN
    sequence, seek_time = c_scan(requests, initial_head, disk_size, direction)
    results["C-SCAN"] = {
        "sequence": sequence,
        "seek_time": seek_time,
        "status": get_streaming_status(seek_time)
    }
    
    # LOOK
    sequence, seek_time = look(requests, initial_head, disk_size, direction)
    results["LOOK"] = {
        "sequence": sequence,
        "seek_time": seek_time,
        "status": get_streaming_status(seek_time)
    }
    
    # C-LOOK
    sequence, seek_time = c_look(requests, initial_head, disk_size, direction)
    results["C-LOOK"] = {
        "sequence": sequence,
        "seek_time": seek_time,
        "status": get_streaming_status(seek_time)
    }
    
    return results


def find_best_algorithm(results):
    """
    Find the algorithm with minimum seek time
    """
    best_algorithm = None
    min_seek_time = float('inf')
    
    for algorithm, data in results.items():
        if data["seek_time"] < min_seek_time:
            min_seek_time = data["seek_time"]
            best_algorithm = algorithm
    
    return best_algorithm, min_seek_time
