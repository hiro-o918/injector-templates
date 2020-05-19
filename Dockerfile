FROM node:12.14.0-buster as node

FROM python:3.8-buster
LABEL maintainer="Hironori Yamamoto <mr.nikoru918@gmail.com>"

SHELL ["/bin/bash", "-c"]

ENV ROOTHOME /root
ENV WORKSPACE /app
ENV POETRY_VERSION 1.0.2

RUN mkdir -p $WORKSPACE
WORKDIR $WORKSPACE

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/$POETRY_VERSION/get-poetry.py > get-poetry.py && \
    python get-poetry.py -y --version $POETRY_VERSION

# set poetry's path
ENV PATH $ROOTHOME/.poetry/bin:$PATH

COPY pyproject.toml $WORKSPACE
COPY poetry.lock $WORKSPACE

RUN poetry config virtualenvs.create false \
    && pip install --upgrade pip \
    && poetry install -n

# install node
COPY --from=node /usr/local/bin/node /usr/local/bin/
COPY --from=node /usr/local/lib/node_modules/ /usr/local/lib/node_modules/
RUN ln -s /usr/local/bin/node /usr/local/bin/nodejs \
  && ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
  && ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npx

ENV USERNAME python
ENV USERHOME /home/$USERNAME
RUN groupadd -r $USERNAME \
    && useradd -r -m -g $USERNAME $USERNAME

COPY configs $USERHOME/.jupyter/
COPY lab $WORKSPACE/lab
RUN chown $USERNAME:$USERNAME -R $ROOTHOME $WORKSPACE $USERHOME

USER $USERNAME
ENV PATH $ROOTHOME/.poetry/bin:$PATH

CMD ["jupyter", "lab", "--ip=0.0.0.0"]
