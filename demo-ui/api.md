
### Get all possible tasks for a certain input (e.g., want to work with tabular datasets)


```
curl -X 'POST' \
  'https://talon-curation-api.cluster1.alidalab.it/curation/choice' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "input": "tabular"
}'
```

The user choose interpolation to remove nulls. 

### Get all possible implementation to solve a task 
(imagine it as a list of models)

```
curl -X 'POST' \
  'https://talon-curation-api.cluster1.alidalab.it/curation/choice' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "input": "interpolation"
}'
```

### Get metadata for each possible implementation

curl -X 'POST' \
  'https://talon-curation-api.cluster1.alidalab.it/curation/choice' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "input": "ts_linear_interpolation",
  "columns": [
    "humidity"
  ]
}'