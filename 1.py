kotlin

sudo add-apt-repository ppa:kotlin/kotlin

sudo apt-get update
sudo apt-get install kotlin

kotlin -version

JS

sudo apt-get update
sudo apt-get install nodejs

sudo apt-get install npm

node -v


java
sudo apt-get install default-jdk
java -version

# Используем официальный образ Ubuntu как базовый образ
FROM ubuntu:latest

# Обновляем список пакетов
RUN apt-get update -y

# Устанавливаем Python
RUN apt-get install -y python3 python3-pip

# Устанавливаем Node.js и npm
RUN apt-get install -y nodejs npm

# Устанавливаем Java (OpenJDK)
RUN apt-get install -y openjdk-11-jdk

# Устанавливаем Kotlin
RUN curl -s https://get.sdkman.io | bash \
  && bash -c "source $HOME/.sdkman/bin/sdkman-init.sh \
  && sdk install kotlin \
  && sdk install kscript"

# Добавляем путь к Kotlin в PATH
ENV PATH $PATH:/root/.sdkman/candidates/kotlin/current/bin

# Устанавливаем необходимые библиотеки для управления контейнером
RUN pip3 install docker

