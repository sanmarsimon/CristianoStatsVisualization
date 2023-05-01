FROM python:3.9.10

WORKDIR /home/git/INF8808_Project

COPY requirements.txt ./

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./
ENV PORT=9900
ENV HOST=51.158.60.122

EXPOSE 9900

CMD [ "python", "./app.py"]
