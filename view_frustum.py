from settings import *

class ViewFrustum:
    def __init__(self, camera):
        self.camera = camera


    def is_on_frustum(self, chunk)->bool:
        dr = chunk.center - self.camera.position
        cx, cy, cz = glm.dot(dr, self.camera.right), glm.dot(dr, self.camera.up), glm.dot(dr, self.camera.forward)

        if cz < NEAR-CHUNK_SPHERE_RADIUS or cz > FAR + CHUNK_SPHERE_RADIUS:
            return False
        
        if abs(cy) > (H_V_SEC * CHUNK_SPHERE_RADIUS + H_V_TAN * cz):
            return False
        
        if abs(cx) > (H_H_SEC * CHUNK_SPHERE_RADIUS + H_H_TAN * cz):
            return False
        
        return True