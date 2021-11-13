# Serve the application

```bash
# Install dependencies
$ poetry install
# Compile translations
$ poetry run pybabel compile -d translations
# Start the server
$ poetry run uvicorn main:app
```

# Call the API

```bash
# (default) Message is English
$ curl -i localhost:8000
# Message is Spanish
$ curl -i -H 'Accept-Languages: es' localhost:8000
# Message is Japanese
$ curl -i -H 'Accept-Languages: ja' localhost:8000
```
