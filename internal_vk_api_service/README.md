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
uvicorn app:app --reload --port 5051
```