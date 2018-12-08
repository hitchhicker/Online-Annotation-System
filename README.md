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
Go to [localhost:8000/login](localhost:8000/login)
 - `login`: bingbinadmin
 - `password`: bingbinpass
## Run unit test
```commandline
export PYTHONPATH=.
pytest tests
```
