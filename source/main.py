import cv2
import torch
import argparse
from utilities import *
from tracker import *
import time
import csv
import numpy as np
from models.experimental import attempt_load
from utils.datasets import LoadImages
from utils.general import non_max_suppression, scale_coords

model = version = source = img = thick = conf = font =  destination = iou =  label_type = no_run = rand_col = show_ver = None
colors = [(147, 51, 255), (255, 51, 51), (68, 209, 52), (52, 130, 209), (0,0,0), (40,40,40),(120,120,60)]
speed = []
temp2 = []
temp3 = []
dash = '-' * 80
twirl = ['|', '/', '-', '\\']

def globs():
    print(f'version = {version}')
    print('source = ' + source)
    print(f'img = {img}')
    print(f'thick = {thick}')
    print(f'conf = {conf}')
    print(f'font = {font}')
    print(f'destination = {destination}')
    print(f'iou = {iou}')
    print(f'label_type = {label_type}')
    print(f'no_run = {no_run}')
    print(f'rand_col = {rand_col}')
    print(f'show_ver = {show_ver}')

def debug(frame, iden, center, s1, s2, radii = [200, 150, 100, 50]):
    if len(radii) >= 4:
        if iden == s2:
            if center not in temp2:
                #print(f'center = {center}')
                temp2.insert(0, center)
        if iden == s1:
            if center not in temp3:
                #print(f'center = {center}')
                temp3.insert(0, center)
        g = 0
        
        while g < len(temp2):
            #print(f'points = {temp2[g]}')
            if g == 1:
                cv2.circle(frame, temp2[g],5,(255, 255,255), thickness=-1)
            else:
                cv2.circle(frame, temp2[g],5,(0,0,255), thickness=-1)
            g += 1
            
        g = 0
        while g < len(temp3):
            if g ==1 :
                cv2.circle(frame, temp3[g],5,(255, 255,255), thickness=-1)
            else:
                cv2.circle(frame, temp3[g],5,(0,0,255), thickness=-1)
            g += 1

        dists2, dist, dists1 = 1000, 1000, 1000
        if len(temp2) > 1:
            dists2 = math.hypot(center[0] - (temp2[1])[0], center[1] - (temp2[1])[1])
        if len(temp3) > 1:
            dists1 = math.hypot(center[0] - temp3[1][0], center[1] - temp3[1][1])
        
        if iden == s2:
            dist = dists2
        else:
            dist = dists1
        red = (0,0,255)
        green = (0, 255, 0)
        rangs = [(radii[0], red), (radii[1],red), (radii[2],red), (radii[3],red)]
        g = 0
        while g < len(rangs):
            rng, _ = rangs[g]
            if dist <= rng:
                rangs[g] = rng, green
            g += 1

        if iden == s2 or iden == s1:
            cv2.circle(frame,center,rangs[0][0],rangs[0][1], thickness=2)
            cv2.circle(frame,center,rangs[1][0],rangs[1][1], thickness=2)
            cv2.circle(frame,center,rangs[2][0],rangs[2][1], thickness=2)
            cv2.circle(frame,center,rangs[3][0],rangs[3][1], thickness=2)

def proccess(frame, ships_in_frame, tracker, curr):
    type_count = {"carrier": 0, "warship": 0, "civilian": 0, "submarine": 0}
    h, w, _ = frame.shape
    ships_in_frame = tracker.update(ships_in_frame, curr, h, w)
    
    if show_ver:
        draw_text(frame, f'- Version {version} {curr:04}-', (0, 0), (0, 60), (0, 0, 0), thick )
        draw_text(frame, f'conf {conf} img {img} iou {iou}', (0, 60), (60, 120), (255, 0, 0), thick )
        # draw_text(frame, f'img {img}', (60, 120), (120, 180), (0, 255, 0), thick )

    for ship in ships_in_frame:
        x, y, x2, y2, confidence, ship_type, name, iden = ship
        p1, p2 = (int(x), int(y)), (int(x2), int(y2))
        #type_count[name] += 1
        label = f'{iden}: ' + name if label_type else f'{iden}: ' + name + f' {round(confidence, 2)}'
        center = ((p2[0] + p1[0]) // 2 ), ((p1[1] + p2[1]) // 2)
        cx, cy = center
        if ship_type == 3:
            center = cx, int(cy*1.1) 
        #debug(frame, iden, center, 11, 9)
        cv2.rectangle(frame, p1, p2, colors[ship_type], thick, lineType=cv2.LINE_AA)
        cv2.circle(frame, center,5,(0,0,255), thickness=-1)
        draw_text(frame, label, p1, p2 , colors[ship_type], thick)                       
    return frame

def draw_text(frame, text, p1, p2, color, thickness):
    w, h = cv2.getTextSize(text, 0, fontScale=font / 3, thickness=thickness)[0]
    outside = p1[1] - h - 3 >= 0
    p2 = p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3
    cv2.rectangle(frame, p1, p2, color, -1, lineType = cv2.LINE_AA)
    cv2.putText(frame, text, (p1[0], p1[1] - 2 if outside else p1[1] + h + 2), 0, font / 3, (255, 255, 255),
                        thickness=thick, lineType=cv2.LINE_AA)

def parse():
    parser = argparse.ArgumentParser(description="Ship Detection")
    parser.add_argument('--version', '-v', type = int, default = 13, choices= range(1,15), help = 'version number [1 - 9]')
    parser.add_argument('--source', '-s', type = str, default='../stimulus/new2.mp4', help = 'video source path')
    parser.add_argument('--img', '-i', type = int , choices = range(100, 1081), default=416, help = 'inference size [320 416 640]', metavar="100-1000")
    parser.add_argument('--thick', '-t', type = int , choices=range(1, 6), default=2, help = 'line thickness [.25 - 3.0]')
    parser.add_argument('--conf', '-c', type = float , choices=Range(.1, 1), default=.4, help = 'confidence threshold [.4 - 1.0]')
    parser.add_argument('--font', '-f', type = int , choices=range(1, 6), default=3, help = 'font scale [.25 - 3.0]')
    parser.add_argument('--destination', '-d', type = str, nargs=2 , default= ['runs/videos/exp.mp4', 'runs/csv/exp.csv'], help = 'destination folder tuple: (video destination, text destination')
    parser.add_argument('--iou',  type = float, default= .45 , choices= Range(.1,1), help = 'set intersection of union threshold [.1 - 1.0]')
    parser.add_argument('--label', '-l', dest = 'label_type',  action = 'store_false', default= True , help = 'toggle lable type')
    parser.add_argument('--no-run', '-n', dest = 'no_run',  action = 'store_true', default= False , help = 'toggle lable type')
    parser.add_argument('--color', '-col', dest = 'rand_col',  action = 'store_true', default= False , help = 'toggle random colors')
    parser.add_argument('--show_ver', dest = 'show_ver',  action = 'store_true', default= False , help = 'show version and inference numbers')

    args = parser.parse_args()
    globals().update(vars(args))
    global model, colors
    model = attempt_load('../' + f'models/model{version}.pt', map_location='cpu')
    if rand_col:
        colors = [tuple(np.random.randint(0, 255, size=3).tolist()) for i in range(1, 5)]
    
def predict():
    global img, conf, source
    stride, source, bs = int(model.stride.max()), source, 1
    dataset = LoadImages(source, img_size=img, stride=stride, auto=True)
    vid_path, vid_writer = [None] * bs, [None] * bs
    names = model.names
    tracker = DistTracker()
    save_path =  uniquify('../' + destination[0])
    save_path2 = uniquify('../' + destination[1])
    count = 1
    for path, imgD, im0s, vid_cap in dataset:
        start = time.time()
        imgD = torch.from_numpy(imgD).to('cpu')
        imgD = imgD.float()
        imgD = imgD / 255.0 

        if len(imgD.shape) == 3:
            imgD = imgD[None]

        pred = model(imgD, augment=False, visualize=False)[0]
        pred = non_max_suppression(pred, conf, iou, None, False, max_det=1000)

        for i, det in enumerate(pred):
            s, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]

            if len(det):
                det[:, :4] = scale_coords(imgD.shape[2:], det[:, :4], im0.shape).round()
                arr = []

                for *xyxy, confi, cls in det:
                    c = int(cls)
                    arr.append( (int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3]), round(float(confi),3), c, names[c]))
            else:
                arr = []
            proccess(im0, arr, tracker, count)
            
            if vid_path[i] != save_path:
                vid_path[i] = save_path
                if isinstance(vid_writer[i], cv2.VideoWriter):
                    vid_writer[i].release()
                if vid_cap:  # video
                    fps = vid_cap.get(cv2.CAP_PROP_FPS)
                    w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    length = int(vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))
                vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

            vid_writer[i].write(im0)
            end = time.time()
            runtime = round(end - start, 3)

            if len(speed) >= 30:
                        speed.pop()
                        speed.insert(0, runtime)
            else:
                speed.insert(0, runtime)
            time_remaining = (length - count - 1)*np.mean(speed)

            print('{:<10s}{:>8s}{:>16s}{:>12s}'.format('{}'.format(f'({count}/{length})'),'{}'.format(f'{twirl[count%4]}')
                      ,'{}'.format(f'{int(1/runtime)}fps'),'{}'.format(f'{int(time_remaining)}s')),end="\r", flush=True)
            # print('{:<10s}{:>4s}{:>12s}{:>8s}'.format('{}'.format(f'({count}/{length})'),'{}'.format(f'{twirl[count%4]}')
            #           ,'{}'.format(f'{int(1/runtime)}fps'),'{}'.format(f'{int(time_remaining)}s')))
            

        count += 1

    

    with open(save_path2, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for elem in tracker.csv_arr:
            writer.writerow(elem[:(3*tracker.id_count)]) 
    
    print(f'saved video to {save_path}')
    print(f'saved csv to {save_path2}')

if __name__ == '__main__':
      parse()      
      if no_run:
          globs()
      else:
        start = time.time()
        #print(dash)
        #print(f'MODEL: {version} SOURCE: {source}')
        #print(dash)
        print('{:<10s}{:>10s}{:>12s}{:>14s}'.format('{}'.format('Frame'),'{}'.format('Ships'),'{}'.format(f'FPS'),'{}'.format('ETA')))
        print(dash)
        predict()    
        end = time.time()
        print(f'Completed in {round(end - start, 2)} seconds')

