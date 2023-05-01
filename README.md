App for image detection using FastAPI

**Run MongoDB in Docker Container:**

```sh
docker run -d --name test-mongo -p 27017:27017 mongo
```

**Run local:**

```sh
python3 -m venv venv
```

```sh
source venv/bin/activate
```

```sh
pip install -r requirements.txt
```

```sh
uvicorn app:app --reload
```
