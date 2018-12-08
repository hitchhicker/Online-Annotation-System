# Online-Annotation-System
An Online Image Annotation System
## Quick start
### Create local data folder
```commandline
mkdir -p data/xmls
mkdir data/images
```
### Build docker image
```commandline
docker-compose rm -f && docker-compose build app
```
### Launch container
```commandline
docker-compose up
```
For mac user, get docker IP using the following command
```commandline
docker-machine ip
```
Then go to **{docker-machine ip}:8000/login**

For linux users: go directly **localhost:8000/login**
 - `login`: bingbinadmin
 - `password`: bingbinpass
## Run unit test
```commandline
export PYTHONPATH=.
pytest tests
```
