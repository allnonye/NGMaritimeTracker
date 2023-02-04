# Tracker that monitors ships and assigns unique ids to each ship
# Allen Onyegbado Sebastian Lyda
import math


class Ship:
    def __init__(self, iden, box, type, confidence):
        self.iden = iden
        self.box = box
        self.type = type
        self.confidence = confidence
        self.points = []
        self.left = False
        self.g_count = 0

    def reinit(self, point, box,confidence):
        self.box = box
        self.confidence = confidence
        self.points.insert(0, point)
        self.left = False
        self.g_count = 0

    def size(self):
        return 2*(self.box[1] -  self.box[0]) + 2*(self.box[3] - self.box[2])

    def name(self):
        name = 'bruh'
    
        if self.type == 0:
            name = 'carrier'
        elif self.type == 1:
            name = 'warship'
        elif self.type == 2:
            name ='civilian'
        elif self.type == 3:
            name = 'submarine'
        elif self.type == 4:
            # name = 'tanker'
            name = 'civilian'
        elif self.type == 5:
            # name = 'cargo'
            name = 'civilian'
        elif self.type == 6:
            # name = 'cruise'
            name = 'civilian'
        return name

    def guess(self):
        if len(self.points) > 1:
            dx, dy = (self.points[0][0] - self.points[1][0]), (self.points[0][1] - self.points[1][1])
            self.points.insert(0, (self.points[0][0] + dx, self.points[0][1] + dy))
            self.box = (self.box[0] + dx, self.box[1] + dx, self.box[2] + dy, self.box[3] + dy)
            self.confidence = -1


class DistTracker:
    def __init__(self):
        self.ships = []
        self.id_count = 0
        self.null_ship = Ship(-1, None, -1, -1)
        self.radius = 175
        self.edges = .7
        self.MAX_SHIPS = 100
        self.csv_arr = []
        self.init_csv()

    def init_csv(self):
        x_header = [f'{i}x' for i in range(self.MAX_SHIPS)]
        y_header = [f'{i}y' for i in range(self.MAX_SHIPS)]
        id_header = [f'{i}id' for i in range(self.MAX_SHIPS)]
        header, i = [], 0
        while i < self.MAX_SHIPS:
            header.append('{header:<5s}'.format(header = x_header[i]))
            header.append('{header:<5s}'.format(header = y_header[i]))
            header.append('{header:<5s}'.format(header = id_header[i]))
            i += 1
        # header = [f'ship{i}' for i in range(self.MAX_SHIPS)]
        self.csv_arr.append(header)

    def csv(self):
        positions = [(0, 0, -1)]*(self.MAX_SHIPS)
        
        for ship in self.ships:
            cx = ship.points[0][0]
            cy = ship.points[0][1]
            cx, cy = int(cx), int(cy)
            type = ship.type

            if type > 3:
                type = 2

            if self.id_count < self.MAX_SHIPS:
                positions[ship.iden] = (cx, cy, type)
        
        arr, i  = [], 0
        while i < len(positions):
            cx, cy, type = positions[i]
            cx, cy = int(cx), int(cy)
            if type == 3:
                cy = int(1.1*cy)
            arr.append('{cent:<5d}'.format(cent = cx))
            arr.append('{cent:<5d}'.format(cent = cy))
            arr.append('{ship_class:<5d}'.format(ship_class = type + 1))
            i += 1

        self.csv_arr.append(arr)
        
    def update(self, ship_boxes, curr, h, w):
        ships_in_frame = []
        current_ids = []

        # Iterate through each box prediction and assign the appropriate ship
        for ship_box in ship_boxes:
            x1, y1, x2, y2, confidence, ship_type, _ = ship_box
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            box = x1, x2, y1, y2
            perim = 2*(x2 -  x1) + 2*(y2 - y1)
            closest_ship = self.null_ship, 5000

            # Find which stored ship is closest to the point
            for ship in self.ships:
                distance = math.hypot(cx - ship.points[0][0], cy - ship.points[0][1])
                _, d = closest_ship
                closest_ship = (ship, distance) if distance < d else closest_ship

            s, d = closest_ship

           
            if self.id_count > 1:
                size = s.size()
            else:
                size = 100
            
            same_size = perim in range(int(.75*size), int(1.5*size)) or curr == 1
            
            # Update an existing ship's position if the new point is close to it
            if d < self.radius and s.iden >= 0 and s.iden not in current_ids and same_size:
                s.reinit((cx, cy), box, confidence)
                current_ids.append(s.iden)
                ships_in_frame.append(s)
            # If no existing ships are close to the point, then create a new ship and id
            else:
                new_ship = Ship(self.id_count, box, ship_type, confidence)
                new_ship.points.insert(0, (cx, cy))
                current_ids.append(new_ship.iden)
                ships_in_frame.append(new_ship)
                self.ships.append(new_ship)
                self.id_count += 1
        

        #Predict where ships are during dropped deteciton frames
        # recovered = []
        # edg = self.edges
        # #print(f'edges = {int((1-edg)*w)} {int(edg*w)} {int((1-edg)*h)} {int(edg*h)}')
        # for ship in self.ships:
        #     if ship not in ships_in_frame and not ship.left:
        #         x, y = ship.points[0][0], ship.points[0][1]
                
        #         # Ships can only dissapear around the edges or if they're submarines
        #         if x < (1 - edg)*w or x > edg*w or \
        #             y < (1 - edg)*h or y > edg*h or ship.type == 3:
        #             ship.left = True
        #             #print(f'ship {ship.iden} has left the frame')
        #         elif ship.g_count <= 15:
        #             ship.g_count += 1
        #             ship.guess()
        #             recovered.append(ship)

        # for ship in recovered:
        #     ships_in_frame.append(ship)

        # Old format parity
        out = []
        for ship in ships_in_frame:
            tup = ship.box[0], ship.box[2], ship.box[1], ship.box[3], \
                ship.confidence, ship.type, ship.name(), ship.iden
            out.append(tup)
        
        #print(out)
        self.csv()
        return out
                
        

                

 