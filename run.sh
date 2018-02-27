function check_env_var {
    if [ -z "$XML_SAVE_PATH" ]; then
        echo 'XML_SAVE_PATH was not set, please export it.'
        exit
    fi
    if [ -z "$IMAGE_SAVE_PATH" ]; then
        echo 'IMAGE_SAVE_PATH was not set, please export it.'
        exit
    fi
}
if [ $1 == "-s" ]
    # server
then
    check_env_var
    docker run -d -e XML_SAVE_PATH=$XML_SAVE_PATH -e IMAGE_SAVE_PATH=$IMAGE_SAVE_PATH -v $(pwd)/:/var/www/app --net=host -ti annotation
elif [ $1 == "-d" ]
    # debug
then
    check_env_var
    docker run --rm -e XML_SAVE_PATH=$XML_SAVE_PATH -e IMAGE_SAVE_PATH=$IMAGE_SAVE_PATH -v $(pwd)/:/var/www/app --net=host -ti annotation /bin/bash
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
