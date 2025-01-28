import bpy
import os
import csv
from collections import deque

HOME = os.path.expanduser("~").replace('\\', '/') if os.name == 'nt' else os.path.expanduser("~")

MINTING = 'minting_tokenomics'
EPHEMERAL = 'ephemeral_tokenomics'

CSV = MINTING+'.csv'
CSV_PATH = os.path.join(HOME, 'Documents', 'oroboros_3D', CSV)

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
        
    if dataIter > 50:
        convert_append_row_cell(array, cells[-1], convert)
        
    return array

def csv_column_header(data, col):
    array = []
    for y, row in enumerate(data):
        if y == 0:
            return row[col]
        
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
#Data set is large so only process every 1000th data point
dataIter = 5000

Adjusted_XRO_To_ICP_Header = csv_column_header(data, 9)
Adjusted_XRO_To_ICP_ExchangeRate = csv_column(data, 9, 'FLOAT', dataIter)

Adjusted_XRO_To_ETH_Header = csv_column_header(data, 16)
Adjusted_XRO_To_ETH_ExchangeRate = csv_column(data, 16, 'FLOAT', dataIter)

Adjusted_XRO_To_BTC_Header = csv_column_header(data, 21)
Adjusted_XRO_To_BTC_Exchange_Rate = csv_column(data, 21, 'FLOAT', dataIter)

Generators = csv_column(data, 29, 'INT', dataIter)

One_XRO_In_ICP = csv_column(data, 30, 'FLOAT', dataIter)
One_XRO_In_ICP_STR = csv_column(data, 30, 'STRING', dataIter)

Min_Gen_From_ICP = csv_column(data, 32, 'FLOAT', dataIter)
Max_Gen_From_ICP = csv_column(data, 33, 'FLOAT', dataIter)

One_XRO_In_ETH = csv_column(data, 34, 'FLOAT', dataIter)
One_XRO_In_ETH_STR = csv_column(data, 34, 'STRING', dataIter)

Min_Gen_From_ETH = csv_column(data, 36, 'FLOAT', dataIter)
Max_Gen_From_ETH = csv_column(data, 37, 'FLOAT', dataIter)

One_XRO_In_BTC = csv_column(data, 38, 'FLOAT', dataIter)
One_XRO_In_BTC_STR = csv_column(data, 38, 'STRING', dataIter)

Min_Gen_From_BTC = csv_column(data, 40, 'FLOAT', dataIter)
Max_Gen_From_BTC = csv_column(data, 41, 'FLOAT', dataIter)

X_Offset = 1
#Switch out for different tokens
ActiveDataSet = One_XRO_In_BTC
ActiveDataSet_STR = One_XRO_In_BTC_STR
ActiveDataSet_MIN = Min_Gen_From_BTC
ActiveDataSet_MAX = Max_Gen_From_BTC



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
PRICE DATA
________________________________________________________
'''
##Set number of verts based on data length
#g_node["Socket_2"] = len(ActiveDataSet)

##force update mesh to show in viewport
#mesh_update()

##apply the modifier and collapse the stack
#bpy.ops.object.modifier_apply(modifier=g_node.name)
##Create custom attribut to hold generator samples
#att = add_attr(obj.data.name, 'generators', 'INT')
##Generate point data for custom attributes
#att.data.foreach_set('value', Generators)

##Create the custom attribute on the mesh verts
#attr = add_attr(obj.data.name, 'exchange_rate_vec', 'FLOAT_VECTOR')
#x = create_axis_offset_array(X_Offset, ActiveDataSet)
#y = ActiveDataSet
#z = create_zero_array(ActiveDataSet)

#vectors = create_point_vectors(x, y, z, x)

##Generate point data for custom attributes
#attr.data.foreach_set('vector', vectors)
'''
________________________________________________________


MIN & MAX DATA
________________________________________________________
'''
#Set number of verts based on data length
g_node["Socket_2"] = len(ActiveDataSet)

#force update mesh to show in viewport
mesh_update()

#apply the modifier and collapse the stack
bpy.ops.object.modifier_apply(modifier=g_node.name)
#Create custom attribut to hold generator samples
att = add_attr(obj.data.name, 'generators', 'INT')
#Generate point data for custom attributes
att.data.foreach_set('value', Generators)

ActiveDataSet = Min_Gen_From_BTC
attr = add_attr(obj.data.name, 'supply_min_vec', 'FLOAT_VECTOR')
x = create_axis_offset_array(X_Offset, ActiveDataSet)
y = ActiveDataSet
z = create_zero_array(ActiveDataSet)

vectors = create_point_vectors(x, y, z, x)
attr.data.foreach_set('vector', vectors)

ActiveDataSet = Max_Gen_From_BTC
attr = add_attr(obj.data.name, 'supply_max_vec', 'FLOAT_VECTOR')
x = create_axis_offset_array(X_Offset, ActiveDataSet)
y = ActiveDataSet
z = create_zero_array(ActiveDataSet)

vectors = create_point_vectors(x, y, z, x)
attr.data.foreach_set('vector', vectors)

