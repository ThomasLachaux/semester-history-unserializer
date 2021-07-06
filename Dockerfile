FROM python:3.8

WORKDIR /srv

COPY ./ ./

ENV PIPENV_VENV_IN_PROJECT="enabled"
RUN pip3 install pipenv && \
    pipenv install && \
    chmod -R g+w /srv


USER 5000:0

CMD pipenv run python main.py