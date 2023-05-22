**Run MongoDB in Docker Container:**

```sh
docker run -d --name test-mongo -p 27017:27017 mongo
```

**Run RabbitMQ in Docker Container**
```sh
docker run -d -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password rabbitmq:3.11-management
```
