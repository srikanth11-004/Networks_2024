CN-3530  --------- ES22BTECH11006--ES22BTECH11004
Basic 
open the basic directory using terminal(cd /home/p4/tutorials/exercises/basic) and execute the following commands

make clean
make run
xterm h1
xterm h2
This will generate two separate terminal instances h1 and h2
In h2 Terminal run the following command :

bash h2-arp.sh
python server.py

#The server starts listening on port declared in the python file server.py

In h1 Terminal run
bash h1-arp.sh
python client.py
        
the following will show in the terminal -----  "Enter : "
1. Enter the request you want to send to the server in double quotes
2. If you want to close the connection enter [ctrl+c]
        
The request you entered will be printed in the H2 terminal as
        server received <request>
The response server sends will be printed in the H1 terminal as
        client received <request>
—---------------------------------------------------------------------


Star
       open  the basic directory using terminal(cd /home/p4/tutorials/exercises/star) and execute the following commands

make clean
make run
xterm h1
xterm h2
xterm h3
This will generate three separate terminal instances
In h3 Terminal run
bash h3-arp.sh
python server.py

The server starts listening on port declared in the server.py file1 
In h2 Terminal run
bash h2-arp.sh
python cache.py
        
        The cache starts listening on port.

In h1 terminal run
bash h1-arp.sh
python client.py

the following will show up in the terminal ---- "Enter : " 

1. Enter the request you want to send to the server in double quotes
2. If you want to close the connection enter [ctrl+c]


The request you entered will be printed in the H2 terminal as
 "cache received <request>"
The response cache sends will be printed in the H1 terminal as
 "client received <request>"