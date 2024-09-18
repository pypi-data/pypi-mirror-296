# PyLogs

**NOTE: This library is for internal use of Markematics Digital.**

## Config File

**Example**

```ini
[Database]
host = localhost
port = 5432
user = admin
password = secret
dbName = myDatabase
tableName = myTable
```

- `Database` section must be present
- All properties are must except `tableName`.
- If `tableName` is not given then default will be `pylogs`

`py -m pip install --upgrade build`
`py -m build`
`py -m pip install --upgrade twine`
`py -m twine upload --repository pypi dist/\*`
