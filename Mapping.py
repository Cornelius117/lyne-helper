import conf
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm

'''
First part of the project. Get pictures from the game 
'''

def getPicture():
    # TODO: get screenshot of the game and save it in directory
    path = cv2.imread(conf.path_material + "1test_u2.jpg")
    # 1600 * 2560, 程序是按这个大小写的，之后需要修改增加自动调整大小缩放功能
    return path


def mapping():
    raw_p = getPicture()

    vertex1_end_p = cv2.imread(conf.path_element + "rhombus_endpoint.jpg")
    vertex1_mid_p = cv2.imread(conf.path_element + "rhombus_node.jpg")
    vertex2_end_p = cv2.imread(conf.path_element + "square_endpoint.jpg")
    vertex2_mid_p = cv2.imread(conf.path_element + "square_node.jpg")
    vertex3_end_p = cv2.imread(conf.path_element + "triangle_endpoint.jpg")
    vertex3_mid_p = cv2.imread(conf.path_element + "triangle_node.jpg")

    hollow2_p = cv2.imread(conf.path_element + "hollow2.jpg")
    hollow3_p = cv2.imread(conf.path_element + "hollow3.jpg")
    hollow4_p = cv2.imread(conf.path_element + "hollow4.jpg")

    node_name = [vertex1_end_p, vertex1_mid_p, vertex2_end_p, vertex2_mid_p,
                 vertex3_end_p, vertex3_mid_p, hollow2_p, hollow3_p, hollow4_p]
    node_list = []
    for i in range(9):
        node_list.append([])

    for i in range(9):
        node_p = node_name[i]
        result = cv2.matchTemplate(raw_p, node_p, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= conf.threshold)
        locations = list(zip(*locations[::-1]))
        match_info = {}


        for loc in locations:
            x, y = loc
            match_value = result[y, x]
            #match_info[(x, y)] = match_value
            skip = False
            for (prev_x, prev_y), prev_match_value in match_info.items():
                if abs(x - prev_x) <= conf.deviation and abs(y - prev_y) <= conf.deviation:
                    skip = True
                    break
            if not skip:
                match_info[(x, y)] = match_value

        for (x, y), mv in match_info.items():
            node_list[i].append([x, y])

    for i in range(9):
        print(node_list[i])

    graph = makeGraph(node_list)

    file = open(conf.path_graph + "graph.txt", mode='w', encoding='utf-8')
    for line in graph:
        file.write(''.join(line) + "\n")
    file.close()


def makeGraph(node_list):
    axis_x = []
    axis_y = []
    for nl in node_list:
        for [x, y] in nl:
            skip = False
            for prev_x in axis_x:
                if abs(x - prev_x) <= conf.deviation:
                    skip = True
                    break
            if not skip:
                axis_x.append(x)

            skip = False
            for prev_y in axis_y:
                if abs(y - prev_y) <= conf.deviation:
                    skip = True
                    break
            if not skip:
                axis_y.append(y)

    axis_x.sort()
    axis_y.sort()

    print(axis_x)
    print(axis_y)

    '''
    0: blank
    2: hollow2
    3: hollow3
    4: hollow4
    a: rhombus_endpoint
    b: rhombus_node
    m: square_endpoint
    n: square_node
    x: triangle_endpoint
    y: triangle_node
    '''
    letter = ['a', 'b', 'm', 'n', 'x', 'y', '2', '3', '4']
    graph = []
    for i in range(len(axis_y)):
        graph.append([])
        for j in range(len(axis_x)):
            graph[i].append('0')

    for i in range(len(node_list)):
        for [x, y] in node_list[i]:
            index0, index1 = findLocation(x, y, axis_x, axis_y)
            graph[index0][index1] = letter[i]

    for i in range(len(graph)):
        print(graph[i])

    return graph

def findLocation(x, y, axis_x, axis_y):
    index0 = -1
    index1 = -1
    for i in range(len(axis_x)):
        coordinate_x = axis_x[i]
        if abs(coordinate_x - x) <= conf.deviation:
            index1 = i
            break

    for i in range(len(axis_y)):
        coordinate_y = axis_y[i]
        if abs(coordinate_y - y) <= conf.deviation:
            index0 = i
            break

    return index0, index1


if __name__ == '__main__':
    mapping()