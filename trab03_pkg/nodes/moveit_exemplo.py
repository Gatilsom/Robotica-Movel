#!/usr/bin/env python3

import sys
import rospy

from copy import deepcopy
from math import pi
from moveit_commander import *
from tf import transformations
from geometry_msgs.msg import PoseStamped, Quaternion


class CreateScene:
    
    global scene, scene_objects
    
    def __init__(self, reference_frame, object_initial_position):
        #self.scene = scene
        #self.scene_objects = scene_objects
        self.reference_frame = reference_frame
        self.object_initial_position = object_initial_position
        
        # cria superfície de suporte
        self.table = {'name':'table', 'size':(0.7, 1, 0.5), 'pose':PoseStamped()}
        self.add_table()
        
        # cria objeto agarrável
        self.can = {'name':'can', 'height':0.3, 'size':(0.1, 0.05, 0.15), 'pose':PoseStamped()}
        self.add_can()

        # cria obstáculo
        self.obstacle = {'name':'obstacle', 'size':(0.4, 0.07, 0.4), 'pose':PoseStamped()}
        self.add_obstacle()
        pass
    
    def add_table(self):
        self.table['pose'].header.frame_id = self.reference_frame
        self.table['pose'].pose.orientation.w = 1.0
        self.table['pose'].pose.position.x = 0.7
        self.table['pose'].pose.position.z = 0.0
        scene.add_box(self.table['name'], self.table['pose'], size=self.table['size'])
        scene_objects.append(self.table['name'])
        pass
        
    def add_can(self):
        self.can['pose'].header.frame_id = self.reference_frame
        self.can['pose'].pose.orientation.w = 1.0
        self.can['pose'].pose.position.x = self.table['pose'].pose.position.x
        self.can['pose'].pose.position.y = self.table['pose'].pose.position.y + self.object_initial_position
        self.can['pose'].pose.position.z = 0.35
        scene.add_box(self.can['name'], self.can['pose'], size=self.can['size'])
        scene_objects.append(self.can['name'])
        pass
    
    def add_obstacle(self):
        self.obstacle['pose'].header.frame_id = self.reference_frame
        self.obstacle['pose'].pose.orientation.w = 1.0
        self.obstacle['pose'].pose.position.x = self.table['pose'].pose.position.x
        self.obstacle['pose'].pose.position.y = self.table['pose'].pose.position.y
        self.obstacle['pose'].pose.position.z = self.table['pose'].pose.position.z + self.table['size'][2]/2 + self.obstacle['size'][2]/2
        scene.add_box(self.obstacle['name'], self.obstacle['pose'], size=self.obstacle['size'])
        scene_objects.append(self.obstacle['name'])
        pass
    
    pass


def create_move_group():
    move_group = MoveGroupCommander('panda_arm')
    move_group.set_max_velocity_scaling_factor(0.3)
    move_group.set_max_acceleration_scaling_factor(0.2)
    return move_group


def create_artificial_scene(move_group, object_initial_position):
    global scene, scene_objects
    rospy.sleep(1)
    s = CreateScene('world', object_initial_position)
    move_group.set_support_surface_name('table')
    rospy.sleep(1)
    return s


def def_initial_pose(scene):
    object_initial_pose = scene.get_object_poses(['can'])['can']
    object_initial_pose.position.x -= 0.25
    object_initial_pose.orientation = Quaternion(*transformations.quaternion_from_euler(0, -pi/2, pi))
    object_target_pose = deepcopy(object_initial_pose)
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


def pick_object(robot, eef_link):
    global scene, scene_objects
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
    

def place_object(eef_link):
    global scene, scene_objects
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


scene = PlanningSceneInterface()            # dispobiliza uma interface para compreensão interna do robô e o mundo
scene_objects = []                          # lista de objetos contidos na cena


def main():
    
    global scene, scene_objects
    
    repeat = True                               # variável auxiliar utilizada para repetição da cena
    object_initial_position = 0.2               # posição relativa ao obstáculo
    robot = RobotCommander()                    # criação do robô
    
    move_group = create_move_group()            # cria uma interface para planejamento e execução de movimentos
    eef_link = move_group.get_end_effector_link()
	
	# inicializacão do nó master
    roscpp_initialize(sys.argv)
    rospy.init_node("move_group_python_interface_tutorial", anonymous=True)
    
    while repeat:
    
        # cria uma cena artifial para o robô
        s = create_artificial_scene(move_group, object_initial_position)
        
        # define a pose inicial e o objeto que será agarrado
        object_initial_pose, object_target_pose = def_initial_pose(scene)
        
        # se aproxima do objeto
        near_object(move_group, object_initial_pose)

        # agarra (caputura) o objeto
        pick_object(robot, eef_link)

        # movimenta o objeto enquanto desvia dos obstáculos
        move_object(move_group, object_target_pose)

        # posiciona o objeto
        place_object(eef_link)

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

