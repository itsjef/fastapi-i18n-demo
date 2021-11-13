# Serve the application

```bash
# Install dependencies
$ poetry install
# Start the server
$ poetry run uvicorn main:app
```

# Call the API

```bash
curl -i localhost:8000  # Message in English (default)
curl -i -H 'Accept-Languages: es' localhost:8000 # Message in Spanish
```
