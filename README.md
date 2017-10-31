# Punktuator service image

This repository describes the elements needed to install and run the automatic punctuation process develop by [Alp Oktem](https://github.com/alpoktem) at TALN-UPF.

Basically, the process is composed by two steps/modules:
1. The [proscripter](https://github.com/alpoktem/Proscripter), which creates acoustically annotated speech transcripts from audio/transcript pair.
2. The [krisPunctuator](https://github.com/alpoktem/krisPunctuator) generates punctuation of acoustically annotated speech transcripts.

You'll find sample inputs [here](https://github.com/alpoktem/Proscripter/tree/master/sampledata).

Each of those components has it's own dependencies, which are summarized and disposed into a Dockerfile, so anyone (with a little docker knowledge) can build and run a docker container that allows to punctuate a speech-to-text input.

In order to try it, you should:

1. Build the docker image:

    ```
    docker build -t taln/krispunk -f Dockerfile .
    ```

2. Launch the container, bound to ``localhost:8989``:

    ```
    docker run -p 8989:80 -t taln/krispunk
    ```

After that, you'll be able to connect to ``http://localhost:8989/punkt`` and you'll see the input form.
