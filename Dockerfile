FROM python:3.12-slim

WORKDIR "./"

RUN pip install uv

COPY uv.lock pyproject.toml ./
RUN uv sync --no-dev

ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . .

CMD ["uv", "run", "entrypoint.py"]
