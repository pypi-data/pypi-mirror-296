<div align="center">
  <h1>BFPRT </h1>

  <p>
    <strong>Median of Medians Quickselect Algorithm</strong>
  </p>

  <hr />
</div>

## About

This package implements fast median finding with the median of medians selection algorithm, also known as BFPRT (named after the authors of [Blum et al. (1973)](http://people.csail.mit.edu/rivest/pubs/BFPRT73.pdf)). It can be used to find the kth smallest value in a list, also known as the "kth order statistic".

When k is halfway through a list, then quickselect finds the median of the list in O(n) time. While this asymptotically linear algorithm is provably optimal, the constant factor overhead is known to be large, making this approach less useful in practice. In theory, however, the median of medians trick can be a very powerful proof step.

This package is intended primarily as a learning tool rather than a practical implementation. For faster runtime on most reasonably sized problems, prefer standard implementations of the median.

## Installation

```bash
pip install bfprt
```

## Usage

```py
from bfprt import select_fast

# Items can have any type that implements less-than comparison
items = [4, 2, 1, 9, 5, 8]

# We want to get the kth smallest element from the list
k = 3

# This is the index of the kth smallest element
selected_index = select_fast(items, 0, 5, k)

# If k is len(items) // 2, then this is the median
kth_order_statistic = items[selected_index]
```

## Installing from source

Install using [Poetry](https://python-poetry.org/)

```bash
poetry install
```
