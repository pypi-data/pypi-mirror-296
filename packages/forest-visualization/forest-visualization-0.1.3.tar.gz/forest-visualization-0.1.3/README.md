# Forest Visualizer

`forest-visualizer` is a Python package that provides tools for building and visualizing forest data structures using Turtle Graphics. This package allows users to perform operations like inserting nodes, tree traversal (pre-order, post-order, and level-order), deleting nodes, and drawing the forest structure visually.

## Background
This package implements a forest visualization algorithm based on the paper [Novel Static Multi-Layer Forest Approach and Its Applications](https://www.mdpi.com/2227-7390/9/21/2650)   published in MDPI. The paper provides detailed insights into the theoretical foundations of the algorithm.

## Features

- **Tree Insertion:** Insert parent-child relationships to build a forest structure.
- **Tree Traversal:** Perform pre-order, post-order, and level-order traversals of the forest.
- **Node Deletion:** Remove nodes and automatically adjust the tree structure.
- **Visual Representation:** Use Turtle Graphics to draw the forest with customizable node sizes and gaps.
- **Path Finding:** Find the path from any node to the root.

## Installation

You can install the `forest-visualizer` package directly from PyPI:

```bash
pip install forest-visualizer
```
## Example  Python Code

```python
from forest_visualizer import Forest
# Example usage
forest = Forest()

# Inserting nodes
forest.insert('40', 'N/A')
forest.insert('50', '40')
forest.insert('30', '40')
forest.insert('35', '30')
forest.insert('25', '30')
forest.insert('28', '25')
forest.insert('15', '25')
forest.insert('60', '50')
forest.insert('45', '50')
forest.insert('70', '60')
forest.insert('55', '60')


forest.level_traversal()
forest.display()
print(forest.find_parent('25'))
print(forest.find_path_to_root('15'))
#Perform pre-order traversal and print the result
pre_order_result = forest.pre_order_traversal('40')
print("Pre-order traversal result:", pre_order_result)

#Perform pre-order traversal and print the result
post_order_result = forest.post_order_traversal('40')
print("Post-order traversal result:", post_order_result)
forest.draw_tree()
forest.delete_node('25')
forest.draw_tree()
forest.insert('90', '35')
forest.draw_tree()
```
## Output File![enter image description here](https://github.com/ganeshb15/forest-visualization/blob/main/two_circles.png?raw=true)
