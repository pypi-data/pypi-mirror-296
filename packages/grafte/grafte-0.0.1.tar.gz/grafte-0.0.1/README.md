# My own easy charting library wrapping around matplotlib


"I want to create a grouped bar chart, using `region` as the series, `animal` as the x val, `amount` as the y val"


```py
Bar(data=(df, x='animal', y='amount', c='region')
    canvas={'width': 600, 'height': 300})
```

```sh
$ tought bar ./tests/fixtures/ezbar.csv -o /tmp/mychart.png
```

## TODOS

### 2024-09-12
- write tests for CLI
- handle multi-series charts
    - grouped bar chart

- create default stylesheets

