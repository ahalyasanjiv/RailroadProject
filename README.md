# RailroadProject

## Live application on Heroku
```
https://avocadorails.herokuapp.com
```
Please be aware that Heroku's database might go down.

## Running it Locally

1. The AvocadoRails application uses Flask with Python3. To run it locally, clone the repository.
```
git clone https://github.com/ahalyasanjiv/RailroadProject.git
```

2. Install the requirements.
```
pip3 install -r requirements.txt
```

3. Run the application.
```
python3 application.py
```

## Database
Running the application locally requires a local Postgresql database.
The schema for the database is taken from Railroad1. However, modified data from the stops_at table from Railroad3 are used.
