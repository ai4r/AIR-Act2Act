# AIR-Act2Act Dataset

### Human-Human Interaction Dataset for Training Robots Nonverbal Interaction Behaviors  


## Introduction

To better interact with users, a social robot should understand the users’ behavior, infer the intention, and respond appropriately. Machine learning is one way of implementing robot intelligence. It provides the ability to automatically learn and improve from experience instead of explicitly telling the robot what to do. Social skills can also be learned through watching human-human interaction videos. However, human-human interaction datasets are relatively scarce to learn interactions that occur in various situations. Moreover, we aim to use service robots in the elderly-care domain; however, there has been no interaction dataset collected for this domain. For this reason, we introduce a human-human interaction dataset for teaching non-verbal social behaviors to robots.

Our dataset has the following strengths:

- It is the only interaction dataset of the elderly;
- It provides robotic data to be learned;
- It is one of the largest interaction datasets that provides 3D skeletal data;
- It can be used to not only teach social skills to robots but also benchmark action recognition algorithms.  


## Download
Please follow the link below, and join as a member to get to the download page:
- [http://nanum.etri.re.kr:8080/etriPortal/login?language=en](http://nanum.etri.re.kr:8080/etriPortal/login?language=en)  


## Pre-process
If you have downloaded only sample data, you can view the data without pre-processing.  
But, if you have downloaded full dataset, you should run [preprocess.py](https://github.com/ai4r/AIR-Act2Act/blob/master/preprocess.py) to make folder structure as follows:

(data name)/  
   ├─ (data name).avi  
   ├─ (data name)_depth/  
   ├─ (data name)_body/  
   ├─ (data name).joint  
   ├─ (data name).~joint  
   ├─ (data name).nao  
   └─ (data name).pepper  

The name of each data is in the format of CcccPpppAaaaSsss (e.g., C003P100A010S005),  
in which ccc is the camera ID, ppp is the performer ID, aaa is the interaction scenario ID, and sss is the setup number.

You need to modify the folder names in [preprocess.py](https://github.com/ai4r/AIR-Act2Act/blob/master/preprocess.py) where input files and output files are located.  
Note that, depth map and refined 3d skeletal data must be present to view the data.  


## How to view data

0. Run [viewer.py](https://github.com/ai4r/AIR-Act2Act/blob/master/viewer.py)
1. Open data folder
1. Select data
1. Click 'play' button

![viewer](https://user-images.githubusercontent.com/13827622/58681405-2a105000-83a7-11e9-9946-698b33d31967.png)  


## Installation

The scripts are tested on Windows 10 and Anaconda Python 3.6.  
You need to install the following modules.

$ pip install pillow opencv-python simplejson
$ conda install matplotlib


## Dataset Summary

|Item|Description|
|:--- |:--- |
|Number of samples|5,000 (with three different points-of-view)|
|Number of interaction scenarios|10|
|Number of subjects|100 elderly people, 2 young people|
|Collection environment|1) apartment, 2) senior welfare center|
|Data modalities|RGB video, depth map, body index, 3D skeleton, Robotic data|
|Sensor|Kinect v2|  


## Interaction Scenarios

We asked participants to perform each scenario five times. Each interaction scenario is defined as a pair of coordinated behaviors: an initiating behavior performed by an elderly person (E), and a responsive behavior performed by a partner (R). The initiating behaviors consisted of eight greeting behaviors and an additional two behaviors of high-five and hit. The responsive behaviors were designed so that, when performed by service robots, they would be acceptable to people as natural and humble reactions. Since we did not instruct the participants to act in an exact pattern, there were large variations in intra-class action trajectories.  

||Interaction Scenario|
|:---: |:--- |
|1|E: enters into the service area through the door.<br>R: bows to the elderly person.|
|2|E: stands still without a purpose.<br>R: stares at the elderly person for a command.|
|3|E: calls the robot.<br>R: approaches the elderly person.|
|4|E: stares at the robot.<br>R: scratches its head from awkwardness.|
|5|E: lifts his arm to shake hands.<br>R: shakes hands with the elderly person.|
|6|E: covers his face and cries.<br>R: stretches his hands to hug the elderly person.|
|7|E: lifts his arm for a high-five.<br>R: high-fives with the elderly person.|
|8|E: threatens to hit the robot.<br>R: blocks the face with arms.|
|9|E: beckons to go away.<br>R: turns back and leaves the service area.|
|10|E: turns back and walks to the door. <br>R: bows to the elderly person.|  


## Collection Setup

Our interaction data were collected in an apartment and a senior welfare center where service robots are likely to be used. For each scenario, three cameras were set up at the same height; however, were positioned to capture different views. Two cameras were placed next to each person to capture the behaviors from the point of view of the other person. The last camera was placed in a position where both participants were visible in order to gather information of the participants relative to each other. The position of each camera was adjusted each time to take into consideration the movement range of the participants. In total, the entire dataset has 5,000 interaction samples with three different views, where each view lasts for about 6 s.

- The apartment environment

<img src="https://user-images.githubusercontent.com/13827622/93292569-d6867780-f820-11ea-90da-80dc79ffffbb.png" width="400">

- The senior welfare center environment

<img src="https://user-images.githubusercontent.com/13827622/93292638-f3bb4600-f820-11ea-89d2-3d00410ba203.png" width="400">


## Collected Data

|Data Modality|Resolution|File Format|<center>Size</center>|
|:---: |:---: |:---: |---: |
|RGB video|1920 X 1080|AVI|45.37 GB|
|Depth map|512 X 424|PNG|472.07 GB|
|Body index|512 X 424|PNG|2.12 GB|
|3D skeleton|25 joints|JSON|2.26 GB|
|Robotic data|10 joint angles|JSON|47.0 MB|
|||**Total**|521.88 GB|  


## Publication

All documents and papers that report on research that uses the AIR-Act2Act dataset should cite the following paper:

- Woo-Ri Ko, Minsu Jang, Jaeyeon Lee and Jaehong Kim, "AIR-Act2Act: Human-human interaction dataset for teaching non-verbal social behaviors to robots," [*arXiv preprint arXiv:2009.02041*](https://arxiv.org/abs/2009.02041), 2020.

   ```
   @article{ko2020air,
     title={{AIR-Act2Act: Human-human interaction dataset for teaching non-verbal social behaviors to robots}},
     author={Ko, Woo-Ri and Jang, Minsu and Lee, Jaeyeon and Kim, Jaehong},
     journal={arXiv preprint arXiv:2009.02041},
     year={2020}
   }
   ```


## Contact
Please email wrko@etri.re.kr if you have any questions or comments.  


## Acknowledgment
The protocol and consent of data collection were approved by the Institutional Review Board (IRB) at Suwon Science College, our joint research institute.

This work was supported by the Institute of Information & communications Technology Planning & Evaluation (IITP) grant funded by the Korea government (MSIT) (No. 2017-0-00162, Development of Human-care Robot Technology for Aging Society)  
