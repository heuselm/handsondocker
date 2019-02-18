# Use your own base image
FROM python
#Set Up working directory
WORKDIR /app
#Copy all the code to working directory
COPY . /app
#Install Dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt
#Expose port to communicate 
EXPOSE 8011
# command to run APP
CMD ["python","app.py"]
