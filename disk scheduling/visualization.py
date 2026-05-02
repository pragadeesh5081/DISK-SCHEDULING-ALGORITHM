"""
Visualization functions for disk scheduling algorithms
Uses matplotlib for plotting head movement graphs
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
import matplotlib.patches as mpatches


def plot_head_movement(sequence, initial_head, algorithm_name, disk_size=200):
    """
    Plot head movement for a single algorithm
    """
    if not sequence:
        return None
    
    # Create the full path including initial head
    full_path = [initial_head] + sequence
    positions = list(range(len(full_path)))
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot the head movement
    ax.plot(positions, full_path, 'b-o', linewidth=2, markersize=8, markerfacecolor='red', markeredgecolor='darkred')
    
    # Add labels and title
    ax.set_xlabel('Request Order', fontsize=12)
    ax.set_ylabel('Track Number', fontsize=12)
    ax.set_title(f'{algorithm_name} Algorithm - Head Movement Pattern', fontsize=14, fontweight='bold')
    
    # Set y-axis limits
    ax.set_ylim(-10, disk_size + 10)
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    # Add annotations for each point
    for i, (pos, track) in enumerate(zip(positions, full_path)):
        if i == 0:
            ax.annotate(f'Start: {track}', (pos, track), xytext=(0, 10), 
                       textcoords='offset points', ha='center', fontweight='bold', color='red')
        else:
            ax.annotate(f'{track}', (pos, track), xytext=(0, -15), 
                       textcoords='offset points', ha='center', fontsize=9)
    
    # Add disk boundaries
    ax.axhline(y=0, color='green', linestyle='--', alpha=0.5, label='Disk Start')
    ax.axhline(y=disk_size-1, color='red', linestyle='--', alpha=0.5, label='Disk End')
    
    # Highlight initial head position
    ax.scatter([0], [initial_head], color='red', s=200, zorder=5, edgecolor='darkred', linewidth=2)
    
    # Add legend
    ax.legend(loc='upper right')
    
    # Adjust layout
    plt.tight_layout()
    
    return fig


def plot_comparison_graph(results, disk_size=200):
    """
    Plot comparison of all algorithms
    """
    if not results:
        return None
    
    algorithms = list(results.keys())
    seek_times = [results[alg]['seek_time'] for alg in algorithms]
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Bar chart comparison
    colors = ['skyblue', 'lightgreen', 'lightcoral', 'lightsalmon']
    bars = ax1.bar(algorithms, seek_times, color=colors, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for bar, value in zip(bars, seek_times):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + max(seek_times)*0.01,
                f'{value}', ha='center', va='bottom', fontweight='bold')
    
    ax1.set_xlabel('Algorithm', fontsize=12)
    ax1.set_ylabel('Total Seek Time', fontsize=12)
    ax1.set_title('Algorithm Performance Comparison', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Line chart for sequence comparison
    ax2.set_xlabel('Request Order', fontsize=12)
    ax2.set_ylabel('Track Number', fontsize=12)
    ax2.set_title('Head Movement Patterns Comparison', fontsize=14, fontweight='bold')
    ax2.set_ylim(-10, disk_size + 10)
    ax2.grid(True, alpha=0.3)
    
    # Plot each algorithm's sequence
    for i, (algorithm, data) in enumerate(results.items()):
        sequence = data['sequence']
        if sequence:
            # Get the initial head (assuming it's the same for all algorithms)
            # This would need to be passed or determined from context
            positions = list(range(1, len(sequence) + 1))
            ax2.plot(positions, sequence, 'o-', linewidth=2, markersize=6, 
                    label=algorithm, color=colors[i % len(colors)])
    
    ax2.legend(loc='upper right')
    
    plt.tight_layout()
    return fig


def plot_streaming_performance(results):
    """
    Plot streaming performance visualization
    """
    if not results:
        return None
    
    algorithms = list(results.keys())
    seek_times = [results[alg]['seek_time'] for alg in algorithms]
    
    # Determine performance levels
    performance_levels = []
    colors = []
    
    for seek_time in seek_times:
        if seek_time < 200:
            performance_levels.append('Smooth')
            colors.append('green')
        elif seek_time < 400:
            performance_levels.append('Moderate')
            colors.append('orange')
        else:
            performance_levels.append('Buffering')
            colors.append('red')
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create horizontal bar chart
    y_pos = np.arange(len(algorithms))
    bars = ax.barh(y_pos, seek_times, color=colors, edgecolor='black', linewidth=1.5)
    
    # Add performance zones
    ax.axvline(x=200, color='green', linestyle='--', alpha=0.5, label='Smooth Threshold')
    ax.axvline(x=400, color='orange', linestyle='--', alpha=0.5, label='Moderate Threshold')
    
    # Add labels
    ax.set_yticks(y_pos)
    ax.set_yticklabels(algorithms)
    ax.set_xlabel('Total Seek Time', fontsize=12)
    ax.set_title('Video Streaming Performance by Algorithm', fontsize=14, fontweight='bold')
    
    # Add performance labels on bars
    for i, (bar, perf_level) in enumerate(zip(bars, performance_levels)):
        width = bar.get_width()
        ax.text(width + max(seek_times)*0.02, bar.get_y() + bar.get_height()/2,
                perf_level, ha='left', va='center', fontweight='bold')
    
    # Add legend
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    return fig


def create_animated_visualization(sequence, initial_head, algorithm_name, disk_size=200):
    """
    Create an animated visualization of head movement (bonus feature)
    """
    # This is a placeholder for animation functionality
    # Would require matplotlib animation or similar
    return plot_head_movement(sequence, initial_head, algorithm_name, disk_size)


def plot_seek_time_distribution(results):
    """
    Plot distribution of seek times (bonus feature)
    """
    if not results:
        return None
    
    algorithms = list(results.keys())
    seek_times = [results[alg]['seek_time'] for alg in algorithms]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create histogram-like visualization
    ax.bar(algorithms, seek_times, color='steelblue', edgecolor='black', linewidth=1.5)
    
    # Add mean line
    mean_seek = np.mean(seek_times)
    ax.axhline(y=mean_seek, color='red', linestyle='--', linewidth=2, 
              label=f'Mean: {mean_seek:.1f}')
    
    # Add labels
    ax.set_xlabel('Algorithm', fontsize=12)
    ax.set_ylabel('Total Seek Time', fontsize=12)
    ax.set_title('Seek Time Distribution Across Algorithms', fontsize=14, fontweight='bold')
    
    # Add value labels
    for i, (alg, time) in enumerate(zip(algorithms, seek_times)):
        ax.text(i, time + max(seek_times)*0.01, f'{time}', 
               ha='center', va='bottom', fontweight='bold')
    
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    return fig


def save_plot(fig, filename):
    """
    Save plot to file (bonus feature)
    """
    try:
        fig.savefig(filename, dpi=300, bbox_inches='tight')
        return True
    except Exception as e:
        print(f"Error saving plot: {e}")
        return False


def get_plot_colors():
    """
    Return consistent color scheme for plots
    """
    return {
        'FCFS': 'skyblue',
        'SSTF': 'lightgreen',
        'SCAN': 'lightcoral',
        'C-SCAN': 'lightsalmon',
        'LOOK': 'plum',
        'C-LOOK': 'wheat',
        'background': 'white',
        'grid': 'lightgray',
        'text': 'black'
    }
