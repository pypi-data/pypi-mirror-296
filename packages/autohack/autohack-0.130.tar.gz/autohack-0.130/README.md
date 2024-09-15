# Auto Hack
* note the setup steps described here are being beta-tested.

## This package does automated vulnerability enumeration and recommends exploits.<br><br>

### How to Run on Non Kali-Linux Operating System (Recommended)
* Clone repo
* cd into repo
* Build image

    ```
    docker build -t autohack .
    ```
* Run as terminal inside container
  ```
  docker run -it autohack
  ```
  
* Run as terminal inside container and mount local folder called portal
  ```
  docker run -ti -v ${PWD}/portal:/root/portal autohack 
  ```

* Run AutoHack

  ```
  autohack -i <some ip address>
  ```
  
---  

### How to Run on Kali-Linux Operating System
* Install AutoHack Python Package

    ```
    pip install autohack
    ```
* Run AutoHack
  ```
  autohack -i <some ip address>
  ```