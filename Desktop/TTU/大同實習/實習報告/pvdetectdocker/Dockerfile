FROM python:3

RUN mkdir /code
WORKDIR /code
ADD . /code/

RUN pip install Django==2.2.3
RUN pip install azure-cosmosdb-table==1.0.6

# pyodbc driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# pyodbc
RUN apt-get update \
	&& apt-get install g++ \
	&& apt-get install -y unixodbc-dev \
	&& pip install pyodbc

# ssh
ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
	&& apt-get install -y --no-install-recommends dialog \
	&& apt-get update \
	&& apt-get install -y --no-install-recommends openssh-server \
	&& echo "$SSH_PASSWD" | chpasswd

COPY sshd_config /etc/ssh/
COPY init.sh /usr/local/bin/

RUN chmod u+x /usr/local/bin/init.sh
EXPOSE 8000 2222
#CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT ["init.sh"]