sudo chmod -R 777 /kcwebplus
./server stop
mkdir /kcwebplus/app/runtime/log
nohup ./server --h 0.0.0.0 --p 39001 --w 2 start > app/runtime/log/server.log 2>&1 &
nohup ./server --h 0.0.0.0 --p 39002 --w 2 start > app/runtime/log/server.log 2>&1 &
nohup ./server --h 0.0.0.0 --p 39003 --w 2 start > app/runtime/log/server.log 2>&1 &
nohup python3.8kcw_plus server.py intapp/index/pub/clistartplan --cli > app/runtime/log/server.log 2>&1 &