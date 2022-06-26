#!/usr/bin/env python3

import sys
import copy
from math import pi

import rospy
from moveit_commander import *
from tf import transformations
from geometry_msgs.msg import PoseStamped, Quaternion


def create_scene(scene, reference_frame, object_initial_position):
    scene_objects = []

    # cria superfície de suporte
    table_name = 'table'
    table_size = (0.7, 1, 0.5)
    table_pose = PoseStamped()
    table_pose.header.frame_id = reference_frame
    table_pose.pose.orientation.w = 1.0
    table_pose.pose.position.x = 0.7
    table_pose.pose.position.z = 0.0
    scene.add_box(table_name, table_pose, size=table_size)
    scene_objects.append(table_name)

    # cria objeto agarrável
    can_name = 'can'
    can_height = 0.3
    can_size = (0.1, 0.05, 0.15)
    can_pose = PoseStamped()
    can_pose.header.frame_id = reference_frame
    can_pose.pose.orientation.w = 1.0
    can_pose.pose.position.x = table_pose.pose.position.x
    can_pose.pose.position.y = table_pose.pose.position.y + object_initial_position
    can_pose.pose.position.z = 0.35
    scene.add_box(can_name, can_pose, size=can_size)
    scene_objects.append(can_name)

    # cria obstáculo
    obstacle_name = 'obstacle'
    obstacle_size = (0.4, 0.07, 0.4)
    obstacle_pose = PoseStamped()
    obstacle_pose.header.frame_id = reference_frame
    obstacle_pose.pose.orientation.w = 1.0
    obstacle_pose.pose.position.x = table_pose.pose.position.x
    obstacle_pose.pose.position.y = table_pose.pose.position.y
    obstacle_pose.pose.position.z = table_pose.pose.position.z + table_size[2]/2 + obstacle_size[2]/2
    scene.add_box(obstacle_name, obstacle_pose, size=obstacle_size)
    scene_objects.append(obstacle_name)

    return scene_objects


def create_move_group():
    move_group = MoveGroupCommander('panda_arm')
    move_group.set_max_velocity_scaling_factor(0.3)
    move_group.set_max_acceleration_scaling_factor(0.5)
    return move_group, move_group.get_end_effector_link()


def create_artificial_scene(move_group, object_initial_position):
    rospy.sleep(1)
    scene_objects = create_scene(scene, 'world', object_initial_position)
    move_group.set_support_surface_name('table')
    rospy.sleep(1)
    return scene_objects


def def_initial_pose():
    object_initial_pose = scene.get_object_poses(['can'])['can']
    object_initial_pose.position.x -= 0.25
    object_initial_pose.orientation = Quaternion(*transformations.quaternion_from_euler(0, -pi/2, pi))
    object_target_pose = copy.deepcopy(object_initial_pose)
    object_target_pose.position.y *= -1
    return object_initial_pose, object_target_pose
    

def near_object(move_group, object_initial_pose):
    rospy.sleep(1)
    move_group.clear_pose_targets()
    move_group.set_pose_target(object_initial_pose, end_effector_link='panda_hand')
    move_group.go(wait=True)
    move_group.stop()
    move_group.clear_pose_targets()
    rospy.sleep(1)
    pass


def pick_object(scene, scene_objects):
    scene.attach_box(eef_link, 'can', touch_links=robot.get_link_names(group='hand'))
    scene_objects.remove('can')
    pass
	

def move_object(move_group, object_target_pose):
    rospy.sleep(1)
    move_group.set_pose_target(object_target_pose, end_effector_link='panda_hand')
    move_group.go(wait=True)
    move_group.stop()
    move_group.clear_pose_targets()
    rospy.sleep(1)
    pass
    

def place_object(scene, scene_objects, eef_link):
    scene.remove_attached_object(eef_link, name='can')
    scene_objects.append('can')
    pass


def back_initial_position(move_group):
    rospy.sleep(1)
    move_group.set_named_target('ready')
    move_group.go(wait=True)
    move_group.stop()
    move_group.clear_pose_targets()
    rospy.sleep(1)
    pass


repeat = True                               # variável auxiliar utilizada para repetição da cena
object_initial_position = 0.2               # posição relativa ao obstáculo
robot = RobotCommander()                    # criação do robô
scene = PlanningSceneInterface()            # dispobiliza uma interface para compreensão interna do robô e o mundo
scene_objects = []                          # lista de objetos contidos na cena
move_group, eef_link = create_move_group()  # cria uma interface para planejamento e execução de movimentos


def main():
    global repeat, robot, scene, move_group, eef_link, object_initial_position
	
	# inicializacão do nó master
    roscpp_initialize(sys.argv)
    rospy.init_node("move_group_python_interface_tutorial", anonymous=True)
    
    while repeat:
    
        # cria uma cena artifial para o robô
        scene_objects = create_artificial_scene(move_group, object_initial_position)
        
        # define a pose inicial e o objeto que será agarrado
        object_initial_pose, object_target_pose = def_initial_pose()
        
        # se aproxima do objeto
        near_object(move_group, object_initial_pose)

        # agarra (caputura) o objeto
        pick_object(scene, scene_objects)

        # movimenta o objeto enquanto desvia dos obstáculos
        move_object(move_group, object_target_pose)

        # posiciona o objeto
        place_object(scene, scene_objects, eef_link)

        # retorna à configuração inicial
        back_initial_position(move_group)

        arg = input("\n\n deseja repetir [y/n] ?	")
        if arg == "y":
            object_initial_position = object_initial_position * (-1)
            repeat = True
        elif arg == "n":
            repeat = False
            scene.clear()
            rospy.sleep(1)
    pass



if __name__ == "__main__":
    main()

