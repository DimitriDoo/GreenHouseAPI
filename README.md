# GreenHouseAPI
The GreenHouse API helps users see and manage their greenhouse information. 

## Available EndPoints:

```
GET: /greenhouses/<int:greenhouseId>
POST: /greenhouses/<int:greenhouseId>
```

### GET REQUEST
The get request works by submitting URL parameters start, end and type

The type parameter can be used to search from a specific sensor. 
This done by adding 'type=[sensorType]'. 

To see valid sensor names you can see the valid json request.
These names are the same for the GET request.

Currently this can only be done by also searching a specific time interval

```python
if len(sensorType) != 0:
    docs = list(db.instanceData.aggregate([
        {"$match": {"time": {"$gt": start, "$lt": end}}},
        {"$project":
             {"greenhouseId": greenhouseId, f"{sensorType}": f"${sensorType}"}
        }
    ]))
```

A basic GET request will return an array of all the documents with the specified greenhouseId

#### Request URL: http://127.0.0.1:5000/greenhouses/124
#### Output:
```json
[
  {
    "_id": "6384e89c95b5acf59b9989a6",
    "greenhouseId": 124,
    "humidity": 23.5,
    "lumens": 0.75,
    "temp": 20.0,
    "time": "Mon, 28 Nov 2022 11:58:04 GMT"
  },
  {
    "_id": "6384e8b695b5acf59b9989a7",
    "greenhouseId": 124,
    "humidity": 23.5,
    "lumens": 0.75,
    "temp": 20.0,
    "time": "Mon, 28 Nov 2022 11:58:30 GMT"
  },
  {
    "_id": "638eb0c5efdd20372994c8e5",
    "greenhouseId": 124,
    "humidity": 27.3,
    "lumens": 200,
    "temp": 26,
    "time": "Mon, 05 Dec 2022 22:02:29 GMT"
  }
]
```
### Get Request with time interval
This request bellow uses URL parameters in order to search in between a set time interval.


#### Request URL: http://127.0.0.1:5000/greenhouses/124?start=2021-11-28T11:58:30&end=2025-11-28T11:58:04
#### Output:
```json
[
  {
    "_id": "6384e89c95b5acf59b9989a6",
    "greenhouseId": 124,
    "humidity": 23.5,
    "lumens": 0.75,
    "temp": 20.0
  },
  {
    "_id": "6384e8b695b5acf59b9989a7",
    "greenhouseId": 124,
    "humidity": 23.5,
    "lumens": 0.75,
    "temp": 20.0
  },
  {
    "_id": "638eb0c5efdd20372994c8e5",
    "greenhouseId": 124,
    "humidity": 27.3,
    "lumens": 200,
    "temp": 26
  }
]
```
### Get request of Specific sensor info with time interval:
The URL bellow is used in order to search for just a specifc Sensor information in a set time frame of
a greenhouse

#### Request URL: http://127.0.0.1:5000/greenhouses/124?start=2021-11-28T11:58:30&end=2025-11-28T11:58:04&type=lumens
#### Output:

```json
[
  {
    "_id": "6384e89c95b5acf59b9989a6",
    "greenhouseId": 124,
    "lumens": 0.75
  },
  {
    "_id": "6384e8b695b5acf59b9989a7",
    "greenhouseId": 124,
    "lumens": 0.75
  },
  {
    "_id": "638eb0c5efdd20372994c8e5",
    "greenhouseId": 124,
    "lumens": 200
  }
]
```



### Example of a valid Json request POST request:
```json
{
    "humidity": 27.3,
    "temp":26,
    "lumens":200
}
```