## neuroxlink

An experimental [mdast](https://github.com/syntax-tree/mdast) parser to have fun with MyST articles.


```python
nlink = NeuroLink('10.55458/neurolibre.00021')
their_fig_4 = nlink.create_plotly_figure('fig4')
their_fig_4.show()
```
