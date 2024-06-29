path_material = "Material/"                      # Directory of all materials
path_element = path_material + "element/"        # Elements used by matching
path_graph = path_material + "graph/"            # Location of mapped graph
path_picture = path_material + "picture/"          # Raw pictures of the game

'''
"threshold" is an important value. If threshold is set too high, the matching
may fail; If it's set too low, the program can not distinguish three types hollow.
'''
threshold = 0.975                                  # Threshold of matching

deviation = 20                                   # Deviation of the same result
