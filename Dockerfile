
FROM ubuntu:latest


RUN apt-get update -y


RUN apt-get install -y curl unzip zip


RUN apt-get install -y python3 python3-pip


RUN apt-get install -y nodejs npm


RUN apt-get install -y openjdk-11-jdk


RUN curl -s https://get.sdkman.io | bash \
  && bash -c "source $HOME/.sdkman/bin/sdkman-init.sh \
  && sdk install kotlin \
  && sdk install kscript"


ENV PATH $PATH:/root/.sdkman/candidates/kotlin/current/bin


WORKDIR ./app


COPY requirements.txt ./


RUN pip3 install -r requirements.txt
COPY . .

RUN python3 manage.py makemigrations

RUN python3 manage.py migrate


EXPOSE 8000


CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

