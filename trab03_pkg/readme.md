# Robotica-Movel

## Trabalho Sobre Manipuladores Robóticos


Disciplina: Tópicos Especiais em Automação - Robótica Aplicada

Professor: Vinícius Schettino   <https://github.com/vbschettino/>

Instituição: CEFET-MG Campus Leopoldina


#### Equipe:

        Agustinho Cássio Silva Netto
        Karen Barbosa Cesar


#### Instruções:

Movimentar (fake) um braço robótico de um ponto a outro desviando de obstáculos fixos:

        - Usando a interface gráfica do RViz
        
        - Usando as API’s em Python ou C++


#### Instalação e pré-requisitos:

1. ROS

       https://www.ros.org/
       
       http://wiki.ros.org/Installation/Ubuntu
       
       http://wiki.ros.org/ROS/Tutorials/InstallingandConfiguringROSEnvironment
       
       
2. MoveIt
    ```shell
    sudo apt update
    sudo apt install ros-noetic-moveit
    cd ~/catkin_ws/src
    git clone https://github.com/ros-planning/moveit_tutorials.git
    git clone https://github.com/ros-planning/panda_moveit_config.git
    # There seems to be a bug in the binary version of panda
    rosdep update
    rosdep install moveit_tutorials --ignore-src
    rosdep install panda_moveit_config --ignore-src
    cd ~/catkin_ws/catkin_make
    source devel/setup.bash
    rospack profile
    ```
    
#### Execução:

terminal_1:

```shell
    cd ~/catkin_ws
    source devel/setup.bash
    roslaunch trab03_pkg moveit_exemplo.launch
```
    
para repetir a movimentação faça:

terminal_2:

```shell
    cd ~/catkin_ws
    source devel/setup.bash
    rosrun trab03_pkg moveit_exemplo.py
```
