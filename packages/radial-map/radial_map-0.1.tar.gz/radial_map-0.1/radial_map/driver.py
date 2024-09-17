import matplotlib.pyplot as plt
import numpy as np

class RadialMap:
    def __init__(self, points = [], variances = [], title = None): 
        if not points: 
            raise ValueError("No points were provided to plot.")
        if points and not variances: 
            self.points = points
        elif (points and variances) and len(points) == len(variances):
            self.points = points
            self.variances = variances
        else: 
            raise ValueError("The length of points and variances arrays must be equal (1-to-1 correspondence).")
        self.title = title

    def plot(self): 
        if not self.points: 
            raise ValueError("No points were provided to plot.")
        elif self.points and not self.variances:     
            # Point-based plot
            angles = []
            radii = []
            for point in self.points:
                x, y = point
                angle = np.arctan2(y, x)  # Calculate the angle in radians
                radius = np.sqrt(x**2 + y**2)  # Calculate the radius (distance from origin)
                angles.append(angle)
                radii.append(radius)
            # Plot the radial map using Matplotlib
            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax.plot(angles, radii, 'o', linewidth=2)  # Just plot points (no line between them)
            # Ensure the graph is a full circle
            ax.set_ylim(0, max(radii))  # Set radial limits from 0 to max radius
            ax.set_xlim(-np.pi, np.pi)  # Set angular limits from -π to π (full circle)
            ax.set_yticklabels([]) 
            ax.set_xticklabels([])
            if self.title: 
                ax.set_title(self.title)

            plt.show()
        elif self.points and self.variances: 
            # Variance-based boxplot
            angles = []
            radii = []
            variances = self.variances
            
            for point in self.points:
                x, y = point
                angle = np.arctan2(y, x)  # Calculate the angle in radians
                radius = np.sqrt(x**2 + y**2)  # Calculate the radius (distance from origin)
                angles.append(angle)
                radii.append(radius)
                

            # Plot the radial map using Matplotlib
            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax.plot(angles, radii, 'o', linewidth=2)  # Just plot points (no line between them)

            # Ensure the graph is a full circle
            ax.set_ylim(0, max(radii))  # Set radial limits from 0 to max radius
            ax.set_xlim(-np.pi, np.pi)  # Set angular limits from -π to π (full circle)
            
            for i, angle in enumerate(angles):
                radius = radii[i]
                variance = 2 * variances[i]
                long_variance = variance + variances[i]
                long_dist = radius + .5 * variance
                short_dist = radius - .5 * variance
                cross_len = .2
                d_prime_long = np.sqrt(long_dist**2 + (cross_len / 2)**2)
                d_prime_short = np.sqrt(short_dist**2 + (cross_len / 2)**2)
                theta_prime_long = np.arctan2(cross_len / 2, long_dist)
                theta_prime_short = np.arctan2(cross_len / 2, short_dist)
                
                
                
                start_radius = radius - variance / 2
                end_radius = radius + variance / 2
                # main radius line
                # ax.plot([angle, angle], [start_radius, end_radius], color='r', linewidth=1)
                # top cross-line
                ax.plot([angle + theta_prime_long, angle - theta_prime_long], [d_prime_long, d_prime_long], color='r', linewidth=1)
                # bottom cross-line
                ax.plot([angle + theta_prime_short, angle - theta_prime_short], [d_prime_short, d_prime_short], color='r', linewidth=1)
                # left-vertical line
                ax.plot([angle + theta_prime_short, angle + theta_prime_long], [d_prime_short, d_prime_long], color='r', linewidth=1)
                # right-vertical line
                ax.plot([angle - theta_prime_short, angle - theta_prime_long], [d_prime_short, d_prime_long], color='r', linewidth=1)
                
                

            ax.set_yticklabels([])  # Hide the radial labels
            ax.set_xticklabels([])

            # ax.set_title("Radial Map of 2D Euclidean Points")
            if self.title: 
                ax.set_title(self.title)

            plt.show()
            

# Example usage
points = [[1, 1], [2, 2], [3, 1], [4, 0], [3, -1], [2, -2], [1, -1]]
variances = [0.5, 0.7, 0.6, 0.4, 0.6, 0.7, 0.5] 
# radial_map = RadialMap(points, [])
radial_map = RadialMap(points, variances)
radial_map.plot()


