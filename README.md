# Flask Bucket List API

A RESTful API for a bucketlist web app built with Flask

## How to Setup the Project
1. Clone the repo by running ```git clone https://github.com/briankabiro/BucketList_API.git```.
2. Install the required packages:
```
pip install -r requirements.txt
```
3. Start the app by running ```python run.py```


## Tests
To test the app, run  ```nosetests``` on your terminal

## API Endpoints

| Endpoints | Methods | Description | Public Access |
| -------- | ------------- | --------- |--------------- |
| `/auth/register/` | POST  | Register a User | Yes |
|  `/auth/login/` | POST | Login a User | Yes |
| `/auth/reset-password` | POST | Reset User's Password | Yes |
| `/bucketlists/` | GET, POST | Bucketlists of a user | No |
| `/bucketlists/<id>/` | GET, PUT, DELETE | A single bucket list | No |
| `/bucketlists/<id>/items/` | GET, POST | Items in bucketlist | No |
| `/bucketlists/<id>/items/<item_id>/` | GET, PUT, DELETE| An item in a bucketlist | No |

| Method | Description |
|------- | ----------- |
| GET | Retrieves resource |
| POST | Creates resource |
| PUT | Updates a resource |
| DELETE | Deletes a resource |