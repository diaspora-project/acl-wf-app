
# Autonomus Chemistry Laboratory (ACL) for Electrochemistry Workflow.

It is an end-to-end workflow (from instrument to a compute node) orchestrated by a Jupyter notebook located at a remote node where the user can access and steer the electrochemistry workflow. The workflow includes control an electrochemistry workstation to push a liquid catalyst to a flow reactor, where the latter is controlled by potentiostat (a chemistry instruments conducting several electrochemistry reactions). The measurement is transferred in real time to a globus compute node for analytics. The current use case is to use ML for the normality check of the collected measurements prior to achieve domain-specific computations. Further details about this workflow is avaialbe at: 

1- A. Al-Najjar, N. Rao et al., "Cross-facility orchestration of electrochemistry experiments and computations", Proceedings of the SC ’23 Workshops of The International Conference on High Performance Computing Network Storage and Analysis SC-W ’23, pp. 2118-2125, 2023.

2- A. Al-Najjar, N. S. V. Rao et al., "Normality of i-v measurements using ml", 2023 IEEE 19th International Conference on e-Science (e-Science), pp. 1-2, 2023.


## Reproducible workflow steps

1- install globus sdk on the client(globus compute)

2- install globus endpoint on the remote computing system

3- create venv using conda and python 3.10.x

4- create endpoint

5- create acl_dependencies directory at /home/<usr>/.globus_compute/<endpoint>

6- copy globus_endpoint_files in  /home/<usr>/.globus_compute/<endpoint>/acl_dependencies

7- copy testing profiles and jupyter notebooks at the client node

8- run the notebook from that client. Note v01 shows the complete workflow with ORNL instrument files (kept for potential development purposes), while v02 is for reproducibility.

9- have fun!
