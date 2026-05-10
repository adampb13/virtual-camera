import numpy as np

EPSILON = 1e-5

class Triangle:
    def __init__(self, v0, v1, v2, color):
        self.vertices = [np.array(v0, dtype=float), np.array(v1, dtype=float), np.array(v2, dtype=float)]
        self.color = color
        
        edge1 = self.vertices[1] - self.vertices[0]
        edge2 = self.vertices[2] - self.vertices[0]
        
        cross = np.cross(edge1, edge2)
        norm = np.linalg.norm(cross)
        if norm > EPSILON:
            self.normal = cross / norm
        else:
            self.normal = np.array([0.0, 1.0, 0.0], dtype=float)
            
        self.d = -np.dot(self.normal, self.vertices[0])

class BSPNode:
    def __init__(self):
        self.polygons = []
        self.normal = None
        self.d = None
        self.front = None
        self.back = None

def classify_vertex(vertex, normal, d):
    dist = np.dot(vertex, normal) + d
    if dist > EPSILON:
        return 1
    elif dist < -EPSILON:
        return -1
    return 0

def split_triangle(triangle, normal, d):
    # Splits a triangle by a plane and returns a tuple: (front_triangles, back_triangles)
    # The result lists contain new Triangle objects.
    front_verts = []
    back_verts = []
    
    verts = triangle.vertices
    dists = [np.dot(v, normal) + d for v in verts]
    
    for i in range(3):
        v_curr = verts[i]
        d_curr = dists[i]
        
        v_next = verts[(i + 1) % 3]
        d_next = dists[(i + 1) % 3]
        
        if d_curr >= -EPSILON:
            front_verts.append(v_curr)
        if d_curr <= EPSILON:
            back_verts.append(v_curr)
            
        # Check if edge crosses the plane
        if (d_curr > EPSILON and d_next < -EPSILON) or (d_curr < -EPSILON and d_next > EPSILON):
            t = d_curr / (d_curr - d_next)
            intersect = v_curr + t * (v_next - v_curr)
            front_verts.append(intersect)
            back_verts.append(intersect)
            
    # Triangulate polygons into triangles
    def triangulate(vertices, color):
        tris = []
        if len(vertices) >= 3:
            for i in range(1, len(vertices) - 1):
                tris.append(Triangle(vertices[0], vertices[i], vertices[i+1], color))
        return tris
        
    front_tris = triangulate(front_verts, triangle.color)
    back_tris = triangulate(back_verts, triangle.color)
    
    return front_tris, back_tris

def build_bsp(triangles):
    if not triangles:
        return None
        
    node = BSPNode()
    
    # Pick a splitting plane from the first triangle
    splitter = triangles[0]
    node.normal = splitter.normal
    node.d = splitter.d
    
    node.polygons.append(splitter)
    
    front_list = []
    back_list = []
    
    for tri in triangles[1:]:
        # Classify the vertices of the triangle to see where it belongs
        front = False
        back = False
        for v in tri.vertices:
            cls = classify_vertex(v, node.normal, node.d)
            if cls > 0:
                front = True
            elif cls < 0:
                back = True
                
        if front and back:
            # It straddles the plane, split it!
            f_tris, b_tris = split_triangle(tri, node.normal, node.d)
            front_list.extend(f_tris)
            back_list.extend(b_tris)
        elif front: # Front
            front_list.append(tri)
        elif back: # Back
            back_list.append(tri)
        else: # On the plane
            # To break ties/z-fighting, we can put it in front list or node polygons
            if np.dot(tri.normal, node.normal) > 0:
                node.polygons.append(tri)
            else:
                back_list.append(tri)
                
    if front_list:
        node.front = build_bsp(front_list)
    if back_list:
        node.back = build_bsp(back_list)
        
    return node

def traverse_bsp(node, camera_pos):
    # Painter's Algorithm: returns triangles ordered back-to-front!
    if not node:
        return []
        
    result = []
    # Check on which side of the node's plane the camera lies
    dist = np.dot(camera_pos, node.normal) + node.d
    
    if dist > 0:
        # Camera is in front of the plane. Render BACK, then NODE, then FRONT.
        result.extend(traverse_bsp(node.back, camera_pos))
        result.extend(node.polygons)
        result.extend(traverse_bsp(node.front, camera_pos))
    else:
        # Camera is behind the plane. Render FRONT, then NODE, then BACK.
        result.extend(traverse_bsp(node.front, camera_pos))
        result.extend(node.polygons)
        result.extend(traverse_bsp(node.back, camera_pos))
        
    return result
