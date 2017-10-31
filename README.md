# Punktuator service image

1. Build the docker image:

    ```
    docker build -t taln/krispunk -f Dockerfile .
    ```

2. Launch the container, bound to ``localhost:8989``:

    ```
    docker run -p 8989:80 -t taln/krispunk
    ```

After that, you'll be able to connect to ``http://localhost:8989/punkt`` and see the input form.
