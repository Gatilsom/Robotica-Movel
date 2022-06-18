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

    salvar o seguinte arquivo na pasta "worlds"
    ```shell
    my_house.world
    ```
