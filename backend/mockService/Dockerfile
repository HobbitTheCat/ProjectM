FROM python:3.13-slim AS build
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt
COPY . /app

FROM python:3.13-slim
LABEL maintainer="Egor Semenov"
WORKDIR /app
COPY --from=build /app /app
COPY --from=build /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8004

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004"]