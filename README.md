# Northrop Grumman Maritime Optical Tracking Challenge


<p align="left"> <a href="https://www.linux.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-original.svg" alt="linux" width="40" height="40"/> </a> <a href="https://www.mathworks.com/" target="_blank" rel="noreferrer"> <img src="https://upload.wikimedia.org/wikipedia/commons/2/21/Matlab_Logo.png" alt="matlab" width="40" height="40"/> </a> <a href="https://opencv.org/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/opencv/opencv-icon.svg" alt="opencv" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> <a href="https://pytorch.org/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/pytorch/pytorch-icon.svg" alt="pytorch" width="40" height="40"/> </a> </p>

[MTech Competition Website](http://mtech.umd.edu/ng/challenges/northrop-grumman-mission-systems-innovation-challenge-multiple-maritime-target-optical-tracking.html
 "Competition Website") 
<p align="left">
<img src="cert.png"/width=300 height=240>
<img src="images/fleet5.jpg"/height=240>
<img src="images/iou1.jpg"/height=240>
</p>
 
Competed in a Northrop Grumman Competition sponsored and hosted at UMD and placed 1/15 teams of 1-4. Developed a Python/MATLAB application to detect, classify, and enumerate a variety of maritime vessels in real-time. More specifically, the application kept an accurate frame-by-frame catalogue of such vessels, and categorized them into civilians, warships, aircraft carriers, and submarines each with a numerical identifier. 

A csv file was also generated for accuracy checking. The competition spanned a 6 week period, and mentor meetings were biweekly. Research on object detection and utilization of open source machine learning software such as YOLOv5 and Google Colab were used to supplement project success. Custom training and testing data was gathered from Google and Bing Images. 

Research was also needed on tracking, as inaccuracies/frame drops within the models needed reconcilation. Originally planed to use Kalman Filter (linear quadratic estimation) for filling in prediction frame gaps. Settled with naive Eucledian distance "last seen" data structure due to time constraints. 

## Demos
<p float="left">
  <img src="images/gifs/sailing0.gif"/width=500 height=285>
  <img src="images/gifs/sailing1.gif"/width=500 height=285>
  <img src="images/gifs/models0.gif"/width=500 height=285>
  <img src="images/gifs/models1.gif"/width=500 height=285>
  <img src="images/gifs/models2.gif"/width=500 height=285>
  <img src="images/gifs/warships.gif"/width=500 height=285>
</p>

## Screenshots
<p float="left">
  <img src="images/screenshots/screenshot0.png"/width=333 height=189>
  <img src="images/screenshots/screenshot1.png"/width=333 height=189>
  <img src="images/screenshots/screenshot2.png"/width=333 height=189>
  <img src="images/screenshots/screenshot3.png"/width=333 height=189>
  <img src="images/screenshots/screenshot4.png"/width=333 height=189>
  <img src="images/screenshots/screenshot5.png"/width=333 height=189>
  <img src="images/screenshots/screenshot6.png"/width=333 height=189>
  <img src="images/screenshots/screenshot7.png"/width=333 height=189>
  <img src="images/screenshots/screenshot8.png"/width=333 height=189>
</p>

