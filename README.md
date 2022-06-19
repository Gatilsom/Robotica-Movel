# Robotica-Movel

## Trabalho Sobre Robótica Móvel e Navegação Autônoma

#### Equipe:

        Agustinho Cássio Silva Netto
        Karen Barbosa Cesar

#### Instruções:

1. Criar um mundo no Gazebo representando sua casa

    http://gazebosim.org/tutorials?tut=build_world
    
    https://gazebosim.org/tutorials?tut=building_editor
    
    https://answers.gazebosim.org//question/15245/sdf-and-world-file-correct-usage/
    
    http://gazebosim.org/tutorials?tut=ros_roslaunch
    
2. Criar o mapa desse mundo usando teleoperação com o Turtlebot e o pacote hector_mapping

    http://wiki.ros.org/hector_mapping
  
3. Implementar localização e navegação autônoma

    Garantir que o robô consegue passar por portas
    
    Garantir que o robô consegue passar por obstáculos não mapeados
      

#### Instalação e pré-requisitos:

1. ROS

       https://www.ros.org/
       
       http://wiki.ros.org/Installation/Ubuntu
       
       http://wiki.ros.org/ROS/Tutorials/InstallingandConfiguringROSEnvironment
       
       
2. Gazebo

       http://gazebosim.org
       
       sudo apt install ros-noetic-desktop-full
       
       
  
3. Turtlebot

    ```shell
    sudo apt install ros-noetic-turtlebot3 && 
    sudo apt install ros-noetic-turtlebot3-gazebo
    ```

4. Mapeamento

    ```shell
    sudo apt install ros-noetic-hector-slam
    ```

5. Teleoperação

   ```shell
    sudo apt install ros-noetic-teleop-tools
    ```

6. Localização

    ```shell
    sudo apt install ros-noetic-amcl
    ```

7. Navegação

    ```shell
    sudo apt install ros-noetic-navigation
    ```


#### Execução:

1. ##### Construção do pacote:

    ```shell
    cd ~/catkin_ws/src
    catkin_create_pkg trab02_pkg rospy std_msgs geometry_msgs
    cd ~/catkin_ws/src/trab02_pkg
    mkdir nodes launch maps worlds
    cd ~/catkin_ws && catkin_make
    rospack profile
    ```
2. ##### Construção do mundo através do Gazebo:

    após modelagem salve o seguinte arquivo na pasta "worlds"
    ```shell
    my_house.world
    ```
3. ##### Abertura de mundo e mapeamento:
    
    3.1 Método manual:
    
    terminal 1:
    ```shell
    cd ~/catkin_ws
    source devel/setup.bash
    rospack profile
    export TURTLEBOT3_MODEL=burger
    roslaunch trab02_pkg turtlebot_house_simulator.launch
    ```
    terminal 2:
    ```shell
    source devel/setup.bash
    export TURTLEBOT3_MODEL=burger
    roslaunch turtlebot3_slam turtlebot3_slam.launch slam_methods:=hector
    ```
    terminal 3:
    ```shell
    source devel/setup.bash
    export TURTLEBOT3_MODEL=burger
    roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch
    ```
    após realizar todo o mapeamento movendo o robô atraves do teclado:
    
    terminal 4:
    ```shell
    source devel/setup.bash
    rosrun map_server map_saver -f ~/catkin_ws/src/trab02_pkg/maps/map1
    rospack profile
    ```

    3.2 Método alternativo:
    
    terminal 1:
    ```shell
    cd ~/catkin_ws
    source devel/setup.bash
    rospack profile
    export TURTLEBOT3_MODEL=burger
    roslaunch trab02_pkg turtlebot_house_simulator.launch
    ```
    terminal 2:
    ```shell
    source devel/setup.bash
    export TURTLEBOT3_MODEL=burger
    roslaunch trab02_pkg slam_localization.launch slam_mode:=true teleop_mode:=true
    ```
    após realizar todo o mapeamento movendo o robô atraves do teclado:
    
    terminal 3:
    ```shell
    source devel/setup.bash
    rosrun map_server map_saver -f ~/catkin_ws/src/trab02_pkg/maps/map1
    rospack profile
    ```
    
4. ##### Localização:
    
    terminal 1:
    ```shell
    cd ~/catkin_ws
    source devel/setup.bash
    rospack profile
    export TURTLEBOT3_MODEL=burger
    roslaunch trab02_pkg turtlebot_house_simulator.launch
    ```
    terminal 2:
    ```shell
    source devel/setup.bash
    export TURTLEBOT3_MODEL=burger
    roslaunch trab02_pkg slam_localization.launch localization_mode:=true teleop_mode:=true
    ```
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
