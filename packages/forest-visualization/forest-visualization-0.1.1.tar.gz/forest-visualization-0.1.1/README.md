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