# pymdown-fancylists
Python Markdown Extension that allows more types of lists.

Inspired by [Pandoc fancy_lists extension](https://pandoc.org/MANUAL.html#extension-fancy_lists)

- Default (numbers).

- Upper case letters (type="A")

    ```
    A. List item
    B. List item
    C. List item
    ```

- Lower case letters (type="a")

    ```
    a. List item
    b. List item
    c. List item
    ```

- Upper case roman numbers (type="I")

    ```
    I. List item
    II. List item
    III. List item
    ```

- Lower case roman numbers (type="i")

    ```
    i. List item
    ii. List item
    iii. List item
    ```

It also supports setting the starting value of the list.

```
f. List item
g. List item
```


## Installation
```bash
pip install pymdown-fancylists
```

## Usage
```python
md = markdown.Markdown(extensions=['pymdown_fancylists'])
```

