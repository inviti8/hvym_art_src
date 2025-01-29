import bpy
import os
import csv

HOME = os.path.dirname(os.path.realpath(__file__))
FILENAME = os.path.basename(HOME)
PATH = HOME.replace(FILENAME, '')

EPHEMERAL = 'ephemeral_tokenomics'

CSV = EPHEMERAL+'.csv'
CSV_PATH = os.path.join(PATH, CSV)

def read_csv(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
        return data
    
def get_last_item(iterator):
    last_item = None
    queue = deque(maxlen=1)
    
    for item in iterator:
        queue.append(item)
    
    if queue:
        last_item = queue[0]
    
    return last_item
    
def convert_append_row_cell(array, cell, convert):
    if convert == 'STRING':
        array.append(str(cell))
    elif convert == 'FLOAT':
        array.append(float(cell))
    elif convert == 'INT':
        array.append(int(cell))
    else:
        array.append(cell)
    
def csv_column(data, col, convert='NONE', dataIter=1):
    array = []
    col_data = enumerate(data)
    
    for y, row in col_data:
        if y == 0:
            continue
        convert_append_row_cell(array, row[col], convert)
        
    return array

def csv_column(data, col, convert='NONE', dataIter=1):
    array = []
    col_data = enumerate(data)
    cells = []
    
    for y, row in col_data:
        if y == 0:
            continue
        cells.append(row[col])
        if y == 1:#always include first element in data
            convert_append_row_cell(array, row[col], convert)
        if y % dataIter != 0:
            continue
        convert_append_row_cell(array, row[col], convert)
        
    #convert_append_row_cell(array, cells[-1], convert)
        
    return array
        
def mesh_update():
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    
def add_attr(obj_name, attr_name, type='FLOAT', domain='POINT'):
    attr = bpy.data.meshes[obj_name].attributes.new(attr_name, type, domain)
    return attr

def create_axis_offset_array(offset, range_data):
    arr = []
    for i in range(len(range_data)):
        arr.append(offset*i)
        
    return arr

def create_zero_array(range_data):
    arr = []
    for i in range(len(range_data)):
        arr.append(0)
        
    return arr

def create_point_vectors(x, y, z, range_data):
    coords = []
    for i in range(len(range_data)):
        coords.append(x[i])
        coords.append(y[i])
        coords.append(z[i])
        
    return coords

data = read_csv(CSV_PATH)
#Data set is large so only process every 11th data point
dataIter = 8
X_Offset = 1


Ephemeral_Mint_Cycle = csv_column(data, 6, 'INT', dataIter)

Reward_Per_Acct = csv_column(data, 7, 'FLOAT', dataIter)
TotalRewards = csv_column(data, 8, 'FLOAT', dataIter)

print(Ephemeral_Mint_Cycle)


'''
Generate vertices from the loaded data
'''
#get the object
obj = bpy.context.active_object
#add a new geometry node, named 'make_verts'
g_node = obj.modifiers.new('make_verts', 'NODES')
#assign new geometry node, to one created in the scene with the name: 'make_verts'
g_node.node_group = bpy.data.node_groups['make_verts']

'''
________________________________________________________


EPHEMERAL MINT DATA
________________________________________________________
'''
ActiveDataSet = Reward_Per_Acct
#Set number of verts based on data length
g_node["Socket_2"] = len(ActiveDataSet)

#force update mesh to show in viewport
mesh_update()

#apply the modifier and collapse the stack
bpy.ops.object.modifier_apply(modifier=g_node.name)

#Create custom attribut to hold generator samples
att = add_attr(obj.data.name, 'mint_cycles', 'INT')
#Generate point data for custom attributes
att.data.foreach_set('value', Ephemeral_Mint_Cycle)

attr = add_attr(obj.data.name, 'reward_per_acct_vec', 'FLOAT_VECTOR')
x = create_axis_offset_array(X_Offset, ActiveDataSet)
y = ActiveDataSet
z = create_zero_array(ActiveDataSet)

vectors = create_point_vectors(x, y, z, x)
attr.data.foreach_set('vector', vectors)

ActiveDataSet = TotalRewards
attr = add_attr(obj.data.name, 'total_rewards_vec', 'FLOAT_VECTOR')
x = create_axis_offset_array(X_Offset, ActiveDataSet)
y = ActiveDataSet
z = create_zero_array(ActiveDataSet)


vectors = create_point_vectors(x, y, z, x)
attr.data.foreach_set('vector', vectors)
