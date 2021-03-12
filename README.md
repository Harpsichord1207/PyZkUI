# PyZkUI

**A Simple Zookeeper UI tool.**   
Backend: Python/Flask/Kazoo/Waitress.  
Frontend: Bootstrap/jQuery.


### Installation

- `pip install pyzkui`


### Run

- execute `PyZkServer` to start a server
    - use `--host` to bind host, default is `127.0.0.1`
    - use `--port` to set port, default is `8088`
    - use `--debug` to active flask debug mode, default is `False`
    - use `--threads` to set threads num, default is `2`, can not be used in debug mode