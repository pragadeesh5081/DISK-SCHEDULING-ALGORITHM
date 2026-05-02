"""
Disk Scheduling Algorithm Visualizer
Streamlit UI for video streaming buffer management simulation
"""

import streamlit as st
import matplotlib.pyplot as plt
from algorithms import run_all_algorithms, fcfs, sstf, scan, c_scan, look, c_look, find_best_algorithm
from utils import (
    validate_request_queue, validate_initial_head, validate_disk_size,
    format_sequence, calculate_average_seek_time, format_results_summary,
    validate_algorithm_selection, export_results_to_csv
)
from visualization import (
    plot_head_movement, plot_comparison_graph, plot_streaming_performance,
    plot_seek_time_distribution
)
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Disk Scheduling Visualizer",
    page_icon="disk",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Main title
    st.markdown('<h1 class="main-header">Disk Scheduling Visualizer</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #666;">Video Streaming Buffer Management Simulation</h3>', unsafe_allow_html=True)
    
    # Sidebar for inputs
    st.sidebar.header("Configuration")
    
    # Input fields
    request_queue_str = st.sidebar.text_input(
        "Request Queue",
        value="98,183,37,122,14,124,65,67",
        help="Enter comma-separated track numbers"
    )
    
    initial_head_str = st.sidebar.text_input(
        "Initial Head Position",
        value="53",
        help="Starting position of disk head"
    )
    
    disk_size_str = st.sidebar.text_input(
        "Disk Size",
        value="200",
        help="Total number of tracks (default: 200)"
    )
    
    # Algorithm selection
    algorithm = st.sidebar.selectbox(
        "Select Algorithm",
        ["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK", "ALL"],
        index=6,
        help="Choose which algorithm to run"
    )
    
    # Direction for SCAN, C-SCAN, LOOK, and C-LOOK
    direction = st.sidebar.radio(
        "Direction (for SCAN, C-SCAN, LOOK, C-LOOK)",
        ["right", "left"],
        index=0,
        help="Head movement direction"
    )
    
    # Run simulation button
    run_button = st.sidebar.button(
        "Run Simulation",
        type="primary",
        use_container_width=True
    )
    
    # Reset button
    if st.sidebar.button("Reset", use_container_width=True):
        st.rerun()
    
    # Main content area
    if run_button:
        # Validate inputs
        requests, queue_error = validate_request_queue(request_queue_str)
        initial_head, head_error = validate_initial_head(initial_head_str)
        disk_size, size_error = validate_disk_size(disk_size_str)
        
        # Check for validation errors
        error_messages = []
        if queue_error:
            error_messages.append(f"Request Queue: {queue_error}")
        if head_error:
            error_messages.append(f"Initial Head: {head_error}")
        if size_error:
            error_messages.append(f"Disk Size: {size_error}")
        
        if error_messages:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.error("Please fix the following errors:")
            for error in error_messages:
                st.write(f"- {error}")
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        # Validate algorithm selection
        valid, error = validate_algorithm_selection(algorithm, requests)
        if not valid:
            st.error(error)
            return
        
        # Display configuration summary
        st.markdown("## Configuration Summary")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Requests", len(requests))
        with col2:
            st.metric("Initial Head", initial_head)
        with col3:
            st.metric("Disk Size", disk_size)
        with col4:
            st.metric("Direction", direction.capitalize())
        
        # Display request queue
        st.markdown("### Request Queue")
        st.write(f"**{', '.join(map(str, requests))}**")
        
        # Run algorithms
        if algorithm == "ALL":
            results = run_all_algorithms(requests, initial_head, disk_size, direction)
            display_all_results(results, initial_head, disk_size, direction)
        else:
            # Run single algorithm
            if algorithm == "FCFS":
                sequence, seek_time = fcfs(requests, initial_head)
            elif algorithm == "SSTF":
                sequence, seek_time = sstf(requests, initial_head)
            elif algorithm == "SCAN":
                sequence, seek_time = scan(requests, initial_head, disk_size, direction)
            elif algorithm == "C-SCAN":
                sequence, seek_time = c_scan(requests, initial_head, disk_size, direction)
            elif algorithm == "LOOK":
                sequence, seek_time = look(requests, initial_head, disk_size, direction)
            elif algorithm == "C-LOOK":
                sequence, seek_time = c_look(requests, initial_head, disk_size, direction)
            
            display_single_result(algorithm, sequence, seek_time, initial_head, disk_size)
    
    # Instructions at the bottom
    st.markdown("---")
    st.markdown("## How to Use")
    st.markdown("""
    1. **Enter Request Queue**: Provide comma-separated track numbers (e.g., 98,183,37,122,14,124,65,67)
    2. **Set Initial Head**: Specify the starting position of the disk head
    3. **Choose Disk Size**: Set the total number of tracks (default: 200)
    4. **Select Algorithm**: Choose FCFS, SSTF, SCAN, C-SCAN, or run ALL algorithms
    5. **Set Direction**: For SCAN and C-SCAN algorithms, choose head movement direction
    6. **Run Simulation**: Click the button to see results and visualizations
    """)

def display_single_result(algorithm, sequence, seek_time, initial_head, disk_size):
    """Display results for a single algorithm"""
    from algorithms import get_streaming_status
    
    st.markdown(f"## {algorithm} Algorithm Results")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Seek Time", seek_time)
    with col2:
        avg_seek = calculate_average_seek_time(seek_time, len(sequence))
        st.metric("Average Seek Time", avg_seek)
    with col3:
        status, color = get_streaming_status(seek_time)
        st.metric("Streaming Status", status)
    
    # Sequence display
    st.markdown("### Head Movement Sequence")
    st.write(format_sequence(sequence, initial_head))
    
    # Visualization
    st.markdown("### Head Movement Visualization")
    fig = plot_head_movement(sequence, initial_head, algorithm, disk_size)
    if fig:
        st.pyplot(fig)
        plt.close(fig)
    
    # Performance indicator
    status, color = get_streaming_status(seek_time)
    if color == "green":
        st.markdown(f'<div class="success-box">:heavy_check_mark: {status} - Excellent performance!</div>', unsafe_allow_html=True)
    elif color == "orange":
        st.markdown(f'<div class="warning-box">:warning: {status} - Acceptable performance.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="error-box">:x: {status} - Poor performance, consider optimization.</div>', unsafe_allow_html=True)

def display_all_results(results, initial_head, disk_size, direction):
    """Display results for all algorithms"""
    # Find best algorithm
    best_algorithm, min_seek_time = find_best_algorithm(results)
    
    st.markdown("## Algorithm Comparison Results")
    
    # Performance summary
    summary = format_results_summary(results, best_algorithm, min_seek_time)
    st.markdown(summary)
    
    # Detailed results tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Individual Results", "Comparison Graph", "Streaming Performance", "Data Export"])
    
    with tab1:
        # Individual algorithm results
        for algorithm, data in results.items():
            with st.expander(f"{algorithm} - Seek Time: {data['seek_time']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Sequence:** {format_sequence(data['sequence'], initial_head)}")
                    st.write(f"**Total Seek Time:** {data['seek_time']}")
                    st.write(f"**Average Seek Time:** {calculate_average_seek_time(data['seek_time'], len(data['sequence']))}")
                
                with col2:
                    status, color = data['status']
                    if color == "green":
                        st.success(f"Status: {status}")
                    elif color == "orange":
                        st.warning(f"Status: {status}")
                    else:
                        st.error(f"Status: {status}")
                
                # Individual visualization
                fig = plot_head_movement(data['sequence'], initial_head, algorithm, disk_size)
                if fig:
                    st.pyplot(fig)
                    plt.close(fig)
    
    with tab2:
        # Comparison graph
        st.markdown("### Algorithm Performance Comparison")
        fig = plot_comparison_graph(results, disk_size)
        if fig:
            st.pyplot(fig)
            plt.close(fig)
        
        # Seek time distribution
        st.markdown("### Seek Time Distribution")
        fig2 = plot_seek_time_distribution(results)
        if fig2:
            st.pyplot(fig2)
            plt.close(fig2)
    
    with tab3:
        # Streaming performance
        st.markdown("### Video Streaming Performance Analysis")
        fig = plot_streaming_performance(results)
        if fig:
            st.pyplot(fig)
            plt.close(fig)
        
        # Performance insights
        st.markdown("#### Performance Insights")
        for algorithm, data in results.items():
            status, color = data['status']
            if algorithm == best_algorithm:
                st.markdown(f"**{algorithm}**: {status} :trophy: (Best Performance)")
            else:
                st.markdown(f"**{algorithm}**: {status}")
    
    with tab4:
        # Data export
        st.markdown("### Export Results")
        
        # CSV export
        csv_data = export_results_to_csv(results, initial_head, disk_size, direction)
        st.download_button(
            label="Download Results as CSV",
            data=csv_data,
            file_name="disk_scheduling_results.csv",
            mime="text/csv"
        )
        
        # Display as table
        st.markdown("#### Results Table")
        df_data = []
        for algorithm, data in results.items():
            df_data.append({
                'Algorithm': algorithm,
                'Total Seek Time': data['seek_time'],
                'Average Seek Time': calculate_average_seek_time(data['seek_time'], len(data['sequence'])),
                'Number of Requests': len(data['sequence']),
                'Streaming Status': data['status'][0]
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
    
    # Highlight best algorithm
    st.markdown("---")
    st.markdown(f"## :trophy: Best Algorithm: {best_algorithm}")
    st.markdown(f"The **{best_algorithm}** algorithm achieved the lowest seek time of **{min_seek_time}**, resulting in the best streaming performance.")
    
    # Performance recommendation
    if min_seek_time < 200:
        st.markdown('<div class="success-box">:heavy_check_mark: Excellent! The selected configuration provides smooth video streaming with minimal buffering.</div>', unsafe_allow_html=True)
    elif min_seek_time < 400:
        st.markdown('<div class="warning-box">:warning: Good performance with moderate streaming quality. Consider optimizing request patterns for better results.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="error-box">:x: Poor performance detected. High seek times may cause buffering issues. Consider using SSTF or SCAN algorithms for better results.</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
