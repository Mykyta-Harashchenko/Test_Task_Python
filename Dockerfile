FROM ubuntu:latest
LABEL authors="garas"

ENTRYPOINT ["top", "-b"]