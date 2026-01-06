import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

# ==========================================
# 1. CONFIGURATION
# ==========================================
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TARGET_FPS = 60

# Colors
C_SKY = (0.12, 0.12, 0.18)
C_GRASS = (0.15, 0.35, 0.15)
C_ROAD = (0.2, 0.2, 0.22)
C_MARKING = (0.9, 0.9, 0.9)
C_CAR = [(0.8, 0.2, 0.2), (0.2, 0.5, 0.8), (0.8, 0.8, 0.2), (0.9, 0.5, 0.1), (0.3, 0.3, 0.8), (0.8, 0.8, 0.8)]
C_RAIN = (0.7, 0.7, 0.8)
C_SKID = (0.5, 0.5, 0.5) 

# Dimensions
BLOCK_SIZE = 80.0
ROAD_WIDTH = 16.0
LANE_WIDTH = ROAD_WIDTH / 2.0
MAP_LIMIT = 300 

# ==========================================
# 2. UTILS
# ==========================================
def draw_cube(x, y, z, sx, sy, sz, color):
    glPushMatrix()
    glTranslatef(x, y + sy/2, z)
    glScalef(sx, sy, sz)
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex3f(-0.5, -0.5, 0.5); glVertex3f(0.5, -0.5, 0.5); glVertex3f(0.5, 0.5, 0.5); glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, -0.5, -0.5); glVertex3f(-0.5, 0.5, -0.5); glVertex3f(0.5, 0.5, -0.5); glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5); glVertex3f(-0.5, -0.5, 0.5); glVertex3f(-0.5, 0.5, 0.5); glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5); glVertex3f(0.5, 0.5, -0.5); glVertex3f(0.5, 0.5, 0.5); glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5); glVertex3f(-0.5, 0.5, 0.5); glVertex3f(0.5, 0.5, 0.5); glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5); glVertex3f(0.5, -0.5, -0.5); glVertex3f(0.5, -0.5, 0.5); glVertex3f(-0.5, -0.5, 0.5)
    glEnd()
    glPopMatrix()

def draw_refined_car(color):
    # Chassis
    glColor3f(*color)
    glPushMatrix()
    glScalef(2.2, 1.2, 4.6); glTranslatef(0, 0.5, 0)
    glBegin(GL_QUADS)
    v = [(-0.5,-0.5,0.5), (0.5,-0.5,0.5), (0.5,0.5,0.5), (-0.5,0.5,0.5),
         (-0.5,-0.5,-0.5), (-0.5,0.5,-0.5), (0.5,0.5,-0.5), (0.5,-0.5,-0.5),
         (-0.5,0.5,-0.5), (-0.5,0.5,0.5), (0.5,0.5,0.5), (0.5,0.5,-0.5),
         (-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,-0.5,0.5), (-0.5,-0.5,0.5),
         (0.5,-0.5,-0.5), (0.5,0.5,-0.5), (0.5,0.5,0.5), (0.5,-0.5,0.5),
         (-0.5,-0.5,-0.5), (-0.5,-0.5,0.5), (-0.5,0.5,0.5), (-0.5,0.5,-0.5)]
    for p in v: glVertex3f(*p)
    glEnd()
    glPopMatrix()
    # Cabin
    c2 = (max(0, color[0]-0.2), max(0, color[1]-0.2), max(0, color[2]-0.2))
    glColor3f(*c2)
    glPushMatrix()
    glTranslatef(0, 1.4, -0.2); glScalef(1.8, 0.8, 2.5)
    glBegin(GL_QUADS)
    c_glass = (0.2, 0.2, 0.3)
    glColor3f(*c_glass); glVertex3f(-0.5,-0.5,0.5); glVertex3f(0.5,-0.5,0.5); glVertex3f(0.4,0.5,0.3); glVertex3f(-0.4,0.5,0.3)
    glColor3f(*c_glass); glVertex3f(-0.5,-0.5,-0.5); glVertex3f(-0.4,0.5,-0.3); glVertex3f(0.4,0.5,-0.3); glVertex3f(0.5,-0.5,-0.5)
    glColor3f(*color); glVertex3f(-0.4,0.5,-0.3); glVertex3f(-0.4,0.5,0.3); glVertex3f(0.4,0.5,0.3); glVertex3f(0.4,0.5,-0.3)
    glColor3f(*c2); glVertex3f(0.5,-0.5,-0.5); glVertex3f(0.4,0.5,-0.3); glVertex3f(0.4,0.5,0.3); glVertex3f(0.5,-0.5,0.5)
    glVertex3f(-0.5,-0.5,-0.5); glVertex3f(-0.5,-0.5,0.5); glVertex3f(-0.4,0.5,0.3); glVertex3f(-0.4,0.5,-0.3)
    glEnd()
    glPopMatrix()
    # Lights
    glColor3f(1.0, 1.0, 0.8); glPushMatrix(); glTranslatef(0, 0.8, 2.31)
    glBegin(GL_QUADS)
    glVertex3f(-0.8, 0.1, 0); glVertex3f(-0.4, 0.1, 0); glVertex3f(-0.4, -0.1, 0); glVertex3f(-0.8, -0.1, 0)
    glVertex3f(0.4, 0.1, 0); glVertex3f(0.8, 0.1, 0); glVertex3f(0.8, -0.1, 0); glVertex3f(0.4, -0.1, 0)
    glEnd(); glPopMatrix()
    glColor3f(1.0, 0.0, 0.0); glPushMatrix(); glTranslatef(0, 0.8, -2.31)
    glBegin(GL_QUADS)
    glVertex3f(-0.8, 0.1, 0); glVertex3f(-0.4, 0.1, 0); glVertex3f(-0.4, -0.1, 0); glVertex3f(-0.8, -0.1, 0)
    glVertex3f(0.4, 0.1, 0); glVertex3f(0.8, 0.1, 0); glVertex3f(0.8, -0.1, 0); glVertex3f(0.4, -0.1, 0)
    glEnd(); glPopMatrix()
    # Wheels
    glColor3f(0.1, 0.1, 0.1)
    for wx, wz in [(-1.15, 1.2), (1.15, 1.2), (-1.15, -1.5), (1.15, -1.5)]:
        glPushMatrix(); glTranslatef(wx, 0.4, wz); glScalef(0.2, 0.8, 0.8)
        glBegin(GL_QUADS)
        for dx in [-0.5, 0.5]: glVertex3f(dx, -0.5, -0.5); glVertex3f(dx, 0.5, -0.5); glVertex3f(dx, 0.5, 0.5); glVertex3f(dx, -0.5, 0.5)
        glVertex3f(-0.5,0.5,-0.5); glVertex3f(0.5,0.5,-0.5); glVertex3f(0.5,0.5,0.5); glVertex3f(-0.5,0.5,0.5)
        glVertex3f(-0.5,-0.5,-0.5); glVertex3f(0.5,-0.5,-0.5); glVertex3f(0.5,-0.5,0.5); glVertex3f(-0.5,-0.5,0.5)
        glVertex3f(-0.5,-0.5,0.5); glVertex3f(0.5,-0.5,0.5); glVertex3f(0.5,0.5,0.5); glVertex3f(-0.5,0.5,0.5)
        glVertex3f(-0.5,-0.5,-0.5); glVertex3f(0.5,-0.5,-0.5); glVertex3f(0.5,0.5,-0.5); glVertex3f(-0.5,0.5,-0.5)
        glEnd(); glPopMatrix()

def dist_sq(x1, z1, x2, z2):
    return (x1-x2)**2 + (z1-z2)**2

# ==========================================
# 3. CORE CLASSES
# ==========================================
class RainSystem:
    def __init__(self):
        self.drops = []
        for _ in range(500):
            self.drops.append([random.uniform(-400, 400), random.uniform(0, 200), random.uniform(-400, 400), random.uniform(0.5, 1.5)])
        self.active = False
    def update(self, dt):
        if not self.active: return
        for d in self.drops:
            d[1] -= d[3] * (dt * 60) * 2 
            if d[1] < 0: d[1] = 200; d[0] = random.uniform(-400, 400); d[2] = random.uniform(-400, 400)
    def draw(self):
        if not self.active: return
        glColor3f(*C_RAIN); glBegin(GL_LINES)
        for d in self.drops:
            if d[1] < 100: glVertex3f(d[0], d[1], d[2]); glVertex3f(d[0], d[1]+3, d[2])
        glEnd()

class Camera:
    def __init__(self):
        self.azimuth = 45.0
        self.elevation = 45.0
        self.radius = 250.0
        # Pan Targets
        self.tx = 0.0
        self.tz = 0.0
    
    def update(self, keys, dt):
        # Rotation
        if keys[K_LEFT]: self.azimuth -= 90 * dt
        if keys[K_RIGHT]: self.azimuth += 90 * dt
        if keys[K_UP]: self.elevation += 30 * dt
        if keys[K_DOWN]: self.elevation -= 30 * dt
        self.elevation = max(20.0, min(80.0, self.elevation))

        # Zoom
        if keys[K_i]: self.radius = max(50.0, self.radius - 150 * dt)
        if keys[K_o]: self.radius = min(600.0, self.radius + 150 * dt)

        # Pan (WASD)
        # Calculate Forward vector relative to azimuth
        rad = math.radians(self.azimuth)
        fx = math.sin(rad)
        fz = math.cos(rad)
        # Calculate Right vector relative to azimuth
        rx = math.cos(rad)
        rz = -math.sin(rad)

        pan_speed = 200 * dt
        if keys[K_w]: # Forward
            self.tx -= fx * pan_speed
            self.tz -= fz * pan_speed
        if keys[K_s]: # Backward
            self.tx += fx * pan_speed
            self.tz += fz * pan_speed
        if keys[K_a]: # Left
            self.tx -= rx * pan_speed
            self.tz -= rz * pan_speed
        if keys[K_d]: # Right
            self.tx += rx * pan_speed
            self.tz += rz * pan_speed

    def setup_3d(self):
        glMatrixMode(GL_PROJECTION); glLoadIdentity()
        gluPerspective(45, (SCREEN_WIDTH/SCREEN_HEIGHT), 1.0, 1000.0)
        glMatrixMode(GL_MODELVIEW); glLoadIdentity()
        
        rad_az = math.radians(self.azimuth)
        rad_el = math.radians(self.elevation)
        
        # Calculate Eye offset based on Radius/Rotation
        h_rad = self.radius * math.cos(rad_el)
        off_y = self.radius * math.sin(rad_el)
        off_x = h_rad * math.sin(rad_az)
        off_z = h_rad * math.cos(rad_az)
        
        # LookAt: Eye = Target + Offset
        gluLookAt(self.tx + off_x, off_y, self.tz + off_z, self.tx, 0, self.tz, 0, 1, 0)
            
    def get_screen_coords(self, x, y, z):
        try:
            model = glGetDoublev(GL_MODELVIEW_MATRIX)
            proj = glGetDoublev(GL_PROJECTION_MATRIX)
            view = glGetIntegerv(GL_VIEWPORT)
            winx, winy, winz = gluProject(x, y, z, model, proj, view)
            return winx, SCREEN_HEIGHT - winy 
        except: return -100, -100

class TrafficLight:
    def __init__(self, x, z, direction, parent):
        self.x, self.z = x, z; self.dir = direction; self.state = 'red'
        offset = ROAD_WIDTH/2 + 2
        if direction == 'NS': self.pos = (x + offset, z - offset)
        else: self.pos = (x - offset, z - offset)
    def draw(self):
        draw_cube(self.pos[0], 0, self.pos[1], 0.6, 6, 0.6, (0.4, 0.4, 0.4))
        c = (1, 0, 0) if self.state == 'red' else ((0, 1, 0) if self.state == 'green' else (1, 1, 0))
        draw_cube(self.pos[0], 6, self.pos[1], 2, 2, 2, c)

class Intersection:
    def __init__(self, x, z, i_id):
        self.x, self.z = x, z; self.id = i_id
        self.light_ns = TrafficLight(x, z, 'NS', self); self.light_ew = TrafficLight(x, z, 'EW', self)
        self.phase = 'NS_GREEN'; self.timer = 0; self.jammed = False; self.screen_pos = (0, 0)
        self.light_ns.state = 'green'; self.light_ew.state = 'red'
    def toggle(self):
        if self.phase.startswith('NS'): self.phase = 'EW_GREEN'; self.light_ns.state = 'red'; self.light_ew.state = 'green'; self.timer = 5
        else: self.phase = 'NS_GREEN'; self.light_ew.state = 'red'; self.light_ns.state = 'green'; self.timer = 5
    def update(self, dt, emergency_mode):
        if emergency_mode == 1: self.light_ns.state = 'green'; self.light_ew.state = 'red'; return
        elif emergency_mode == 2: self.light_ns.state = 'red'; self.light_ew.state = 'green'; return
        self.timer -= dt
        if self.timer <= 0:
            if self.phase == 'NS_GREEN': self.phase = 'NS_YELLOW'; self.light_ns.state = 'yellow'; self.timer = 2.0
            elif self.phase == 'NS_YELLOW': self.phase = 'EW_GREEN'; self.light_ns.state = 'red'; self.light_ew.state = 'green'; self.timer = 6.0
            elif self.phase == 'EW_GREEN': self.phase = 'EW_YELLOW'; self.light_ew.state = 'yellow'; self.timer = 2.0
            elif self.phase == 'EW_YELLOW': self.phase = 'NS_GREEN'; self.light_ew.state = 'red'; self.light_ns.state = 'green'; self.timer = 6.0

class Car:
    def __init__(self, x, z, direction):
        self.x, self.z = x, z; self.dir = direction; self.speed = 0; self.max_speed = 0.8
        self.original_color = random.choice(C_CAR); self.color = self.original_color
        self.stuck_time = 0; self.last_int_id = -1
        self.target_turn = random.choices(['S', 'L', 'R'], weights=[40, 30, 30])[0]
        self.skidding = False; self.alive = True; self.flash_timer = 0
        self.update_vectors()
    def update_vectors(self):
        if self.dir == 'N': self.dx, self.dz = 0, -1
        elif self.dir == 'S': self.dx, self.dz = 0, 1
        elif self.dir == 'E': self.dx, self.dz = 1, 0
        elif self.dir == 'W': self.dx, self.dz = -1, 0
    def get_rotation(self):
        if self.dir == 'S': return 0   # +Z
        if self.dir == 'N': return 180 # -Z
        if self.dir == 'E': return 90  # +X
        if self.dir == 'W': return -90 # -X
        return 0
    def get_future_info(self):
        dirs = ['N', 'E', 'S', 'W']
        try: idx = dirs.index(self.dir)
        except: return self.dx, self.dz, 0, 0
        if self.target_turn == 'S': next_dir = self.dir
        elif self.target_turn == 'L': next_dir = dirs[(idx - 1) % 4]
        else: next_dir = dirs[(idx + 1) % 4]
        nx, nz = 0, 0
        if next_dir == 'N': nx, nz = 0, -1
        elif next_dir == 'S': nx, nz = 0, 1
        elif next_dir == 'E': nx, nz = 1, 0
        elif next_dir == 'W': nx, nz = -1, 0
        off = LANE_WIDTH / 2; off_x, off_z = 0, 0
        if next_dir == 'N': off_x = off
        elif next_dir == 'S': off_x = -off
        elif next_dir == 'E': off_z = off
        elif next_dir == 'W': off_z = -off
        return nx, nz, off_x, off_z
    def update(self, dt, cars, intersections, is_raining):
        if not self.alive: return 0
        self.x += self.dx * self.speed * (dt * 50); self.z += self.dz * self.speed * (dt * 50)
        should_stop = False
        closest_int = None; min_d = 9999
        for i in intersections:
            d = dist_sq(self.x, self.z, i.x, i.z)
            if d < min_d: min_d = d; closest_int = i
        dist_int = math.sqrt(min_d)
        if closest_int and dist_int < 30:
            dot = (closest_int.x - self.x)*self.dx + (closest_int.z - self.z)*self.dz
            if dot > 0:
                light = closest_int.light_ns if self.dir in ['N','S'] else closest_int.light_ew
                fnx, fnz, off_x, off_z = self.get_future_info()
                exit_x = closest_int.x + (fnx * 30) + off_x; exit_z = closest_int.z + (fnz * 30) + off_z
                exit_clear = True
                if abs(exit_x) < MAP_LIMIT and abs(exit_z) < MAP_LIMIT:
                    for c in cars:
                        if c == self: continue
                        if dist_sq(c.x, c.z, exit_x, exit_z) < 36: exit_clear = False
                if not exit_clear and dist_int < 10: closest_int.jammed = True
                check_signal = (self.target_turn == 'S'); force_go = (self.stuck_time > 5.0)
                stop_condition = (check_signal and light.state != 'green') or (not exit_clear)
                if stop_condition and (10 < dist_int < 18) and not force_go: should_stop = True
                if dist_int < 5.0 and closest_int.id != self.last_int_id: self.execute_turn(closest_int); self.last_int_id = closest_int.id
        for c in cars:
            if c == self: continue
            dx = c.x - self.x; dz = c.z - self.z; proj = dx * self.dx + dz * self.dz; lat = abs(dx * self.dz - dz * self.dx)
            if 0 < proj < 22 and lat < 3: 
                should_stop = True
                if self.skidding:
                    if proj < 5.0 and lat < 2.0: self.alive = False; c.alive = False; return 2 
        if is_raining and should_stop and not self.skidding:
            if random.random() < 0.005: self.skidding = True
        if self.skidding:
            should_stop = False; self.speed = min(self.max_speed * 1.5, self.speed + dt * 2.0)
            self.flash_timer += dt
            if int(self.flash_timer * 15) % 2 == 0: self.color = C_SKID
            else: self.color = self.original_color
        else: self.color = self.original_color
        if should_stop: self.speed = max(0, self.speed - dt*3); self.stuck_time += dt
        else: self.speed = min(self.max_speed, self.speed + dt); self.stuck_time = 0
        return 1 if self.stuck_time > 4.0 else 0
    def execute_turn(self, inter):
        if self.target_turn == 'S': self.target_turn = random.choices(['S', 'L', 'R'], weights=[40, 30, 30])[0]; return
        dirs = ['N', 'E', 'S', 'W']
        try: idx = dirs.index(self.dir)
        except: return
        if self.target_turn == 'L': new_idx = (idx - 1) % 4
        else: new_idx = (idx + 1) % 4 
        new_dir = dirs[new_idx]; self.dir = new_dir; self.update_vectors()
        off = LANE_WIDTH / 2
        if new_dir == 'N': self.x = inter.x + off; self.z = inter.z - 2
        elif new_dir == 'S': self.x = inter.x - off; self.z = inter.z + 2
        elif new_dir == 'E': self.x = inter.x + 2; self.z = inter.z + off
        elif new_dir == 'W': self.x = inter.x - 2; self.z = inter.z - off
        self.target_turn = random.choices(['S', 'L', 'R'], weights=[40, 30, 30])[0]

# ==========================================
# 4. MAIN ENGINE
# ==========================================
class TrafficSim:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("3D City Traffic Sim: Group 4")
        glEnable(GL_DEPTH_TEST); glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(*C_SKY, 1)
        self.camera = Camera(); self.rain = RainSystem()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 14, bold=True)
        self.intersections = []; self.cars = []
        self.paused = False; self.emergency_mode = 0; self.speed_mode = 1.0
        self.sim_time = 0; self.jam_count = 0; self.accident_count = 0; self.total_passed = 0; self.accumulator = 0.0
        self.reset()
    def reset(self):
        self.intersections.clear(); self.cars.clear(); self.sim_time = 0; self.emergency_mode = 0
        self.accident_count = 0; self.total_passed = 0
        coords = [-BLOCK_SIZE, 0, BLOCK_SIZE]; idx = 1
        for x in coords:
            for z in coords:
                self.intersections.append(Intersection(x, z, idx)); idx += 1
    def spawn_car(self):
        coords = [-BLOCK_SIZE, 0, BLOCK_SIZE]; spawns = []; limit = BLOCK_SIZE * 3.0
        for c in coords:
            spawns.append((-limit, c, 'E')); spawns.append((limit, c, 'W'))
            spawns.append((c, -limit, 'S')); spawns.append((c, limit, 'N'))
        s = random.choice(spawns); lx, lz = s[0], s[1]; off = LANE_WIDTH / 2
        if s[2] == 'E': lz += off
        elif s[2] == 'W': lz -= off
        elif s[2] == 'S': lx -= off
        elif s[2] == 'N': lx += off
        for c in self.cars:
            if dist_sq(c.x, c.z, lx, lz) < 144: return 
        self.cars.append(Car(lx, lz, s[2]))
    def draw_scene(self):
        glColor3f(*C_GRASS); glBegin(GL_QUADS); s = 500; glVertex3f(-s,-0.5,-s); glVertex3f(s,-0.5,-s); glVertex3f(s,-0.5,s); glVertex3f(-s,-0.5,s); glEnd()
        glColor3f(*C_ROAD); glBegin(GL_QUADS); y = 0.0; coords = [-BLOCK_SIZE, 0, BLOCK_SIZE]
        for x in coords: w=ROAD_WIDTH/2; glVertex3f(x-w,y,-s); glVertex3f(x+w,y,-s); glVertex3f(x+w,y,s); glVertex3f(x-w,y,s)
        for z in coords: w=ROAD_WIDTH/2; glVertex3f(-s,y+0.01,z-w); glVertex3f(s,y+0.01,z-w); glVertex3f(s,y+0.01,z+w); glVertex3f(-s,y+0.01,z+w)
        glEnd()
        glColor3f(*C_MARKING); glBegin(GL_LINES)
        for x in coords: 
            for z in range(-350, 350, 15): glVertex3f(x,y+0.05,z); glVertex3f(x,y+0.05,z+8)
        for z in coords:
            for x in range(-350, 350, 15): glVertex3f(x,y+0.05,z); glVertex3f(x+8,y+0.05,z)
        glEnd()
        for inter in self.intersections:
            sx, sy = self.camera.get_screen_coords(inter.x, 0, inter.z); inter.screen_pos = (sx, sy)
            if inter.jammed:
                glColor3f(0.8, 0.2, 0.2); w=ROAD_WIDTH/2+2; glBegin(GL_LINE_LOOP)
                glVertex3f(inter.x-w,y+0.2,inter.z-w); glVertex3f(inter.x+w,y+0.2,inter.z-w); glVertex3f(inter.x+w,y+0.2,inter.z+w); glVertex3f(inter.x-w,y+0.2,inter.z+w); glEnd()
            inter.light_ns.draw(); inter.light_ew.draw()
        for c in self.cars:
            glPushMatrix(); glTranslatef(c.x, 0, c.z); glRotatef(c.get_rotation(), 0, 1, 0); draw_refined_car(c.color); glPopMatrix()
        self.rain.draw()
    def draw_hud(self):
        glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity(); gluOrtho2D(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0)
        glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity(); glDisable(GL_DEPTH_TEST)
        glColor4f(0,0,0,0.7); glBegin(GL_QUADS); glVertex2f(0,0); glVertex2f(220,0); glVertex2f(220, SCREEN_HEIGHT); glVertex2f(0, SCREEN_HEIGHT); glEnd()
        def txt(s, x, y, col=(255,255,255)):
            surf = self.font.render(s, True, col); data = pygame.image.tostring(surf, "RGBA", True)
            glRasterPos2d(x, y); glDrawPixels(surf.get_width(), surf.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, data)
        txt("== TRAFFIC SIM ==", 10, 20, (255, 200, 50))
        txt(f"Time: {int(self.sim_time)}s", 10, 50)
        txt(f"On-Screen: {len(self.cars)}", 10, 70); txt(f"Total Passed: {self.total_passed}", 10, 90) 
        txt(f"Stuck/Jam: {self.jam_count}", 10, 110, (255, 100, 100)); txt(f"Accidents: {self.accident_count}", 10, 130, (255, 0, 0))
        e_color = (100, 255, 100); e_txt = "OFF"
        if self.emergency_mode == 1: e_txt = "ON (N/S)"; e_color = (255, 50, 50)
        if self.emergency_mode == 2: e_txt = "ON (E/W)"; e_color = (255, 50, 50)
        txt(f"Emergency: {e_txt}", 10, 160, e_color); txt(f"Rain: {'ON' if self.rain.active else 'OFF'}", 10, 180)
        txt("Controls:", 10, 210); txt("[I]/[O] Zoom +/-", 10, 230); txt("[W][A][S][D] Pan", 10, 250)
        txt("[E] Emergency", 10, 270); txt("[P] Rain", 10, 290); txt("[Click] Toggle Light", 10, 310)
        txt("[Arrows] Rotate/Angle", 10, 330); txt("[Space] Pause | [R] Reset", 10, 350)
        glEnable(GL_DEPTH_TEST); glMatrixMode(GL_PROJECTION); glPopMatrix(); glMatrixMode(GL_MODELVIEW); glPopMatrix()
    def run(self):
        spawn_t = 0; FIXED_DT = 1.0 / 60.0
        while True:
            dt_raw = self.clock.tick(TARGET_FPS) / 1000.0; mx, my = pygame.mouse.get_pos()
            for e in pygame.event.get():
                if e.type == QUIT: return
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE: return
                    if e.key == K_SPACE: self.paused = not self.paused
                    if e.key == K_r: self.reset()
                    if e.key == K_1: self.speed_mode = 1.0
                    if e.key == K_2: self.speed_mode = 2.0
                    if e.key == K_3: self.speed_mode = 4.0
                    if e.key == K_e: self.emergency_mode = (self.emergency_mode + 1) % 3
                    if e.key == K_p: self.rain.active = not self.rain.active
                if e.type == MOUSEBUTTONDOWN:
                    for i in self.intersections:
                        sx, sy = i.screen_pos
                        if math.sqrt((mx - sx)**2 + (my - sy)**2) < 40: i.toggle(); break 
            keys = pygame.key.get_pressed(); self.camera.update(keys, dt_raw); self.rain.update(dt_raw)
            if not self.paused:
                self.accumulator += dt_raw * self.speed_mode
                while self.accumulator >= FIXED_DT:
                    self.sim_time += FIXED_DT; spawn_t -= FIXED_DT
                    if spawn_t <= 0 and len(self.cars) < 60: self.spawn_car(); spawn_t = random.uniform(1.0, 2.0)
                    for i in self.intersections: i.jammed = False; i.update(FIXED_DT, self.emergency_mode)
                    jams = 0
                    for c in self.cars: 
                        status = c.update(FIXED_DT, self.cars, self.intersections, self.rain.active)
                        if status == 1: jams += 1
                        elif status == 2: self.accident_count += 1 
                    self.jam_count = jams
                    passed = 0; active_cars = []
                    for c in self.cars:
                        if c.alive and (abs(c.x) >= 350 or abs(c.z) >= 350): passed += 1
                        elif c.alive: active_cars.append(c)
                    self.total_passed += passed; self.cars = active_cars
                    self.accumulator -= FIXED_DT
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); self.camera.setup_3d(); self.draw_scene(); self.draw_hud(); pygame.display.flip()

TrafficSim().run()