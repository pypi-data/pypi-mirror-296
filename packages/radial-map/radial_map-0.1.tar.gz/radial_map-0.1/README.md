# RadialMap Python Library

This library defines the RadialMap class for polar plotting in Python, allowing for distance and variance-based charts to be plotted quickly and concisely. The starting point of this code was cs271 and then I built more and published it.

## Class Arguments: 
`points`: Euclidian points to be plotted (List[List[int]])

    * Ex: [(1, 1), (-1, 1), (1, 3), (3, -1)]

`variances`: Confidence intervals for each point: variances[i] being the confidence for the distance of points[i] (List[int])

    * Ex: [1, 2, 3, 4]

`title`: Title of plot to be displayed (str)

    * Ex: "Basic Polar Boxplot"

**Once the class has been instantiated, models can be rendered through the plot() function**

## Example Usage:
**Base Polar Plot:**
```python
from radial_map import RadialMap
points = [(1, 1), (-1, 1), (1, 3), (3, -1)]
base_map = RadialMap(points=points, title="Base Polar Map")
base_map.plot()
```
**Base Polar Boxplot:**
```python
from radial_map import RadialMap
points = [(1, 1), (-1, 1), (1, 3), (3, -1)]
variances = [1, 2, 3, 4]
base_boxplot = RadialMap(points=points, variances=variances, title="Base Polar Boxplot")
base_boxplot.plot() 
```




