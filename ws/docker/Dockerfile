# Base
FROM python:3.9

#Install git
RUN  apt-get install -y git

# Clone repo
RUN git clone https://github.com/DaniFdezAlvarez/shexer.git shexer_dir


# Base repo file as base dir
WORKDIR shexer_dir

# Install project dependencies (if any)
RUN pip install -r requirements.txt


# Different execution I think. Also, pass params
ENV PORT=8080

# Execute feature extraction
ENTRYPOINT python -m  ws.shexer_rest $PORT