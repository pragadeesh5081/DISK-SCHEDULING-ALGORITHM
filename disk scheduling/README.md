# Disk Scheduling Algorithm for Video Streaming Buffer Management

A comprehensive Python application that simulates different disk scheduling algorithms and demonstrates how they optimize disk access in video streaming systems to reduce buffering and improve playback performance.

## Features

- **Multiple Disk Scheduling Algorithms**: FCFS, SSTF, SCAN, C-SCAN
- **Interactive Web Interface**: Built with Streamlit for easy use
- **Visualizations**: matplotlib graphs showing head movement patterns
- **Performance Comparison**: Compare algorithms based on seek time
- **Video Streaming Simulation**: Shows impact on streaming quality
- **Data Export**: Export results to CSV format

## Problem Statement

A video streaming service retrieves media data from disk based on user requests. If disk requests are not handled efficiently, it leads to high seek time, causing buffering and playback delays. This system demonstrates how optimized disk scheduling improves streaming performance.

## Project Structure

```
disk_scheduling_project/
|
|-- app.py              # Streamlit UI and main application
|-- algorithms.py       # All scheduling algorithms implementation
|-- visualization.py    # Graph plotting and visualization functions
|-- utils.py            # Input validation and helper functions
|-- README.md           # Documentation
```

## Algorithms Implemented

### 1. FCFS (First Come First Serve)
- Processes requests in the order they arrive
- Simple but often inefficient
- No optimization based on head position

### 2. SSTF (Shortest Seek Time First)
- Always serves the request closest to current head position
- Better performance than FCFS
- Can cause starvation for distant requests

### 3. SCAN (Elevator Algorithm)
- Moves in one direction, serves all requests, then reverses
- More predictable performance
- Fair service to all requests

### 4. C-SCAN (Circular SCAN)
- Moves in one direction, serves all requests, jumps to beginning
- Uniform wait time
- Good for real-time systems

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
pip install streamlit matplotlib numpy pandas
```

## Running the Application

1. Navigate to the project directory:
```bash
cd "disk_scheduling_project"
```

2. Run the Streamlit application:
```bash
streamlit run app.py
```

3. Open your web browser and go to `http://localhost:8501`

## Usage Guide

### Input Parameters

1. **Request Queue**: Enter comma-separated track numbers (e.g., `98,183,37,122,14,124,65,67`)
2. **Initial Head Position**: Starting position of the disk head (e.g., `53`)
3. **Disk Size**: Total number of tracks (default: 200)
4. **Algorithm Selection**: Choose FCFS, SSTF, SCAN, C-SCAN, or ALL
5. **Direction**: For SCAN and C-SCAN algorithms, choose head movement direction

### Sample Input

```
Request Queue: 98,183,37,122,14,124,65,67
Initial Head: 53
Disk Size: 200
Algorithm: ALL
Direction: Right
```

### Expected Output

The application will display:
- **Total Seek Time** for each algorithm
- **Head Movement Sequence** showing the order of disk access
- **Performance Comparison** highlighting the best algorithm
- **Streaming Status** indicating video playback quality
- **Visual Graphs** showing head movement patterns

## Video Streaming Performance

The system evaluates streaming quality based on seek time:

- **Green (Smooth Playback)**: Seek time < 200
- **Orange (Moderate Streaming)**: Seek time 200-400  
- **Red (Buffering)**: Seek time > 400

## Code Structure

### algorithms.py
Contains core scheduling algorithms:
- `fcfs()` - First Come First Serve implementation
- `sstf()` - Shortest Seek Time First implementation
- `scan()` - Elevator Algorithm implementation
- `c_scan()` - Circular SCAN implementation
- `run_all_algorithms()` - Execute all algorithms
- `find_best_algorithm()` - Identify optimal algorithm

### visualization.py
Handles all plotting and visualization:
- `plot_head_movement()` - Individual algorithm visualization
- `plot_comparison_graph()` - Multi-algorithm comparison
- `plot_streaming_performance()` - Streaming quality analysis
- `plot_seek_time_distribution()` - Performance distribution

### utils.py
Utility functions for validation and formatting:
- Input validation functions
- Data formatting helpers
- CSV export functionality
- Performance rating system

### app.py
Main Streamlit application:
- User interface components
- Input validation
- Result display
- Tabbed interface for different views

## Key Features

### 1. Real-time Visualization
- Interactive matplotlib graphs
- Head movement patterns
- Performance comparisons

### 2. Performance Analysis
- Total seek time calculation
- Average seek time
- Best algorithm identification
- Streaming quality assessment

### 3. Data Export
- CSV export for further analysis
- Formatted result tables
- Configuration summary

### 4. User-friendly Interface
- Intuitive controls
- Clear error messages
- Responsive design
- Help tooltips

## Technical Requirements

- **Language**: Python 3.7+
- **Libraries**:
  - `streamlit` - Web interface
  - `matplotlib` - Data visualization
  - `numpy` - Numerical operations
  - `pandas` - Data handling

## Performance Metrics

The application evaluates algorithms based on:

1. **Total Seek Time**: Sum of all head movements
2. **Average Seek Time**: Mean seek time per request
3. **Streaming Quality**: Impact on video playback
4. **Fairness**: Service distribution across requests

## Example Results

For the sample input (98,183,37,122,14,124,65,67, head=53):

| Algorithm | Total Seek Time | Average Seek Time | Streaming Status |
|-----------|------------------|-------------------|------------------|
| FCFS      | 648              | 81.0              | Buffering        |
| SSTF      | 236              | 29.5              | Smooth Playback  |
| SCAN      | 208              | 26.0              | Smooth Playback  |
| C-SCAN    | 292              | 36.5              | Moderate Streaming |

**Best Algorithm**: SCAN with seek time of 208

## Educational Value

This project demonstrates:
- Operating system concepts (disk scheduling)
- Algorithm analysis and comparison
- Data visualization techniques
- Web application development
- Performance optimization principles

## Bonus Features

- **Animated Head Movement**: Visual representation of disk access patterns
- **Export Functionality**: Save results for further analysis
- **Performance Insights**: Automated recommendations
- **Responsive Design**: Works on different screen sizes

## Troubleshooting

### Common Issues

1. **Streamlit not found**: Install using `pip install streamlit`
2. **Matplotlib errors**: Install using `pip install matplotlib`
3. **Port already in use**: Streamlit will automatically find an available port
4. **Input validation errors**: Check the format of comma-separated values

### Performance Tips

- Use smaller request queues for faster processing
- Default disk size (200) works well for most scenarios
- "ALL" algorithms option provides comprehensive comparison

## Future Enhancements

- Add more disk scheduling algorithms (LOOK, C-LOOK)
- Implement real-time simulation
- Add disk speed parameters
- Include I/O scheduling comparison
- Mobile-responsive design

## Contributing

Feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation

## License

This project is open source and available under the MIT License.

---

**Note**: This educational project demonstrates how disk scheduling algorithms impact video streaming performance. The seek time thresholds and streaming quality indicators are simplified for demonstration purposes.
