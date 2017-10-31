FROM ubuntu:16.04

MAINTAINER Roberto Carlini <roberto.carlini@upf.edu>

RUN apt-get update && apt-get install -y \
    git \
    praat \
    python-pip \
    r-base

RUN R -e "install.packages('data.table', repos = 'http://cran.uk.r-project.org')"
RUN R -e "install.packages('plyr', repos = 'http://cran.uk.r-project.org')"
RUN R -e "install.packages('geometry', repos = 'http://cran.uk.r-project.org')"
RUN R -e "install.packages('magic', repos = 'http://cran.uk.r-project.org')"
RUN R -e "install.packages('abind', repos = 'http://cran.uk.r-project.org')"
RUN R -e "install.packages('mFilter', repos = 'http://cran.uk.r-project.org')"
RUN R -e "install.packages('orthopolynom', repos = 'http://cran.uk.r-project.org')"

RUN pip install numpy theano
RUN pip install flask

RUN mkdir opt/punkt_code
WORKDIR opt/punkt_code

RUN git clone https://github.com/alpoktem/Proscripter.git
RUN git clone https://github.com/alpoktem/krisPunctuator.git

COPY punk_server.py .

CMD ["python", "punk_server.py"]
