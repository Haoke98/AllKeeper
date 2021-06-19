#!/bin/bash
NAME="app"
port=7000
RUN_CMD="python3 manage.py runserver 0.0.0.0:${port}"

POSITIONAL=()
model=""
mode=-1

function MyHelp(){
    echo "Please read follow:"
    echo "-h|--help              show the help message"
    echo "-restart|--restart     switch the mode to restart mode."
}


while [[ $# > 0 ]]; do
    case "${1}" in
        -f|--flag)
        echo flag: "${1}"
        shift # shift once since flags have no values
        ;;
        -s|--switch)
        echo "switch: ${1} with value: ${2}"
        shift 2 # shift twice to bypass switch and its value
        ;;
        -h|--help)
        MyHelp
        shift ;;
        -restart|--restart)
            mode=1
            shift
        ;;
        -start|--start)
            mode=0
            shift
        ;;
        -stop|--stop)
            mode=2
            shift
        ;;
        -m|--model)
            # echo "model is ${2}"
            model=${2}
            shift 2
         ;;
        *) # unknown flag/switch
        POSITIONAL+=("${1}")
        shift
        ;;
    esac
done
#echo  $POSITIONAL
#set -- "${POSITIONAL[@]}" # restore positional params
#echo $POSITIONAL

function start() {
    echo "starting now......"
    PID_FILE="./${NAME}.pid"
    LOG_FILE="./${NAME}.log"
    nohup ${RUN_CMD} > ${LOG_FILE}  2>&1 & echo $! > ${PID_FILE}
}

function stop () {
    PID=$(pgrep -f ${port})
    echo "killing now ......"
    kill $PID
}


function restart () {
    echo "restarting now ......"
    stop
    start
}


if [ $mode == 0 ]; then
       # start mode
       start

elif [ $mode == 1 ]; then
        # restart mode
        restart

elif [ $mode == 2 ]; then
        # stop mode
        stop
elif [ $mode == -1 ]; then
        #do nothing
        echo ""
else
     echo "pelease use correctly the flag."
     echo "If you don't know how to use it, please enter the --help"
fi



