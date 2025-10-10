# ACL-mini-app

## Electrochemistry Workflow for Normality Testing 
Electrochemistry workflow is developed to test the normality of voltammetry (I-V)
measurements prior to conduct domain computations associated with an electrochemistry
application, such as battery testing and production.
The measurements are collected as part of a flow reaction on a certain electrolyte
solution using cyclic voltammetry (CV) electrochemical experiment [[1]](#1),[[2]](#2).

## References
<a id="1">[1]</a> 
A. Al-Najjar, N. Rao, et al, “Cross-facility orchestration of electrochemistry
experiments and computations,” in Proceedings of the SC ’23 Workshops of The
International Conference on High Performance Computing, Network, Storage,
and Analysis, SC-W ’23, ( New York, NY, USA ), p. 2118–2125,
Association for Computing Machinery, 2023.

<a id="2">[2]</a>
A. Al-Najjar, N. S. V. Rao, et al, “Normality of i-v measurements using ml,
” in 2023 IEEE 19th International Conference on e-Science (e-Science),
pp. 1–2, 2023.



## Ecosystem Design
The ecosystem spans multiple instrument and computing facilities distributed across multiple sites for real-time measurement collection and analytics.
The ecosystem includes Autonomous Chemistry Laboratory (ACL) at ORNL
where the flow reaction is conducted and (I-V) measurements are collected.
The ecosystem also includes computing systems located at different facilities leveraged for real-time inference.
The workflow is orchestrated from a remote agent capable of accessing ACL and computing facilities. 
In this demonstration the orchestrator collects I-V measurements from ACL over Pyro 
and transfer them over Globus compute to an endpoint configured on remote computing system. 
Custom domain-informed ML modules have been developed and deployed on the remote computing
systems for testing the normality of I-V measurements.

## Mini-APP

 A mini app is developed to simulate the electrochemistry testing workflow over a multi-site ecosystem.
 The mini-app is composed of three services deployed as docker containers. 
 
First container is __acl-electrochemistry__ that emulates the instrument side at ACL 
 to provide I-V measurements.

The second container is __iv_inference_ep__ that includes ML models for the features extraction and inference. These computation models executed as Globus endpoints. 

The third container is __workfloworchestration__ that forwards I-V measurements from __acl-electrochemistry__ to __iv_inference_ep__ with ML analytic models.


## Download, build, and run ACL-MINI-APP

1. Download the repository on a local folder.
2. Build ACL-Mini-APP docker images
   - for __acl-electrochemistry__
     - cd acl-mini-app/instrument_mService && docker build -f Dockerfile -t acl-electrochemistry:latest .
   - for __iv_inference_ep__
     - cd acl-mini-app/compute_mService && docker build -f Dockerfile -t iv_inference_ep:latest .
   - for __workfloworchestration__
     - cd acl-mini-app/workflow_orchestrator_mService && docker build -f Dockerfile -t workfloworchestration:latest .
3. Run docker containers
    - for __acl-electrochemistry__
      - docker run -it acl-electrochemistry:latest
      - python3 instrument_control.py ipServerAddress=\<acl-electrochemistry container ip\> connectionPort=5001 # You get the IP using ifconfig inside the running container
    - for __iv_inference_ep__
      - run -it iv_inference_ep:latest bash  # You will be asked to open URL and get Globus token
    - for __workfloworchestration__
      - docker run -it workfloworchestration:latest
      - python3 workflow_orchstration.py ipServerAddress=\<acl-electrochemistry container ip\> connectionPort=5001 gendpoint=endpoint03.yaml #make sure you update endpoint03 file with globus token.


