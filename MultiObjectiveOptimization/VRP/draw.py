import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def draw(data=[], data_collection=[]):
    fig, ax = plt.subplots()
    x_list = [sublist[0] for sublist in data]
    y_list = [sublist[1] for sublist in data]
    max_x = max(x_list)
    max_y = max(y_list)
    min_x = min(x_list)
    min_y = min(y_list)
    scale_factor = 0.05
    ax.set_xlim(min_x * (1 - scale_factor), max_x * (1 + scale_factor))
    ax.set_ylim(min_y * (1 - scale_factor), max_y * (1 + scale_factor))
    # ax.set_xlim(0, 10)
    # ax.set_ylim(0, 10)

    points, = ax.plot([], [], 'bo')
    lines = []  # To store the Line2D objects

    # # Sample data collection
    # data_collection = [
    #     (np.array([[2, 3], [2, 6], [8, 9]]), np.array([[[3, 7], [2, 6]], [[4, 8], [6, 7]], [[1, 3], [2, 4]]])),
    #     (np.array([[2, 3], [5, 6], [8, 9]]), np.array([[[3, 7], [2, 6]], [[4, 8], [6, 7]]])),
    #     (np.array([[2, 3], [5, 6], [8, 9]]), np.array([[[3, 7], [2, 6]], [[4, 8], [6, 7]]]))
    # ]

    data_collection = data_collection

    def update(frame):
        point_data, line_data = data_collection[frame % len(data_collection)]  # Get current frame's point and line data
        points.set_data(point_data[:, 0], point_data[:, 1])  # Update point positions

        # Clear the lines from the previous frame
        for line in lines:
            line.remove()
        lines.clear()

        # Plot each line segment in red color
        for line_segment in line_data:
            line, = ax.plot(line_segment[:, 0], line_segment[:, 1], color='r')
            lines.append(line)

        # Return a sequence of Artist objects (points and lines) for this frame
        return [points] + lines

    ani = animation.FuncAnimation(fig, update, frames=range(len(data_collection)), blit=True, interval=200)
    plt.show()

# draw(data=[[0, 0], [0, 0]])
