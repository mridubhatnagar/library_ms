FROM ubuntu  

RUN apt-get update
RUN apt-get install -y python3.10 python3-pip

WORKDIR /opt/app 
COPY . /opt/app 

COPY app/requirements.txt /opt/app/

COPY app/config.py /opt/app

RUN pip install --no-cache-dir -r requirements.txt

COPY migrations /opt/app/.

# # Run database migrations
# RUN FLASK_APP=/opt/app flask db upgrade

ENTRYPOINT FLASK_APP=/opt/app/app flask run --host=0.0.0.0