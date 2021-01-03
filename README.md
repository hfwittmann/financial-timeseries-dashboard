# financial-timeseries-dashboard
This post is very much about technology integration. Its aim is to build a dashboard that allows the display of financial timeseries of multiple stocks simultaneously.

This repo is used and described in the following blog post: <todo: add link>

To run, simply use the following command:

1. Get a (free) api-key from https://www.quandl.com/
1.
  - In the the backend folder
  create a file with name .env with the following contents:

  ````
  PYTHONPATH=.
  CHARACTER=?
  HOST= localhost

  quandl_api_key=<Your secret api key goes here, remove the brackets!!!>
  ````
  - In the the front end folder
create a file with name .env with the following contents:

````
PYTHONPATH=.
CHARACTER=?
HOST= backend
````


Now run

````
docker-compose -p deployment -f docker-compose.yml up --build -d
````

Your app should be now start to build. Depending on your system it might take a while.

After a while it should be up and running.

The dashboard should available at localhost:8501.
The swagger ui should be available at local: http://localhost:5000/api/ui/


In the backend folder you will find a sub-folder called data, with cached Data from the d6tflow package.