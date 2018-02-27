if [ $1 == "-s" ]
    # server
then
    docker run -d -e XML_SAVE_PATH=. -e IMAGE_SAVE_PATH=. -v $(pwd)/:/var/www/app --net=host -ti annotation
elif [ $1 == "-d" ]
    # debug
then
    docker run --rm -e XML_SAVE_PATH=. -e IMAGE_SAVE_PATH=. -v $(pwd)/:/var/www/app --net=host -ti annotation /bin/bash
elif [ $1 == "-r" ]
then
    # remove
    docker rm -f $(docker ps -a -q)
elif [ $1 == "-h" ]
then
    echo '-s: [server] lauch server'
    echo '-d: [debug]  enter docker container'
    echo '-r: [remove] remove all containers'
else
    "Unknown argument run.sh -h to see more."
fi
