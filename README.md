1- install globus sdk on the client(globus compute)
2- install globus endpoint on the remote computing system
3- create venv using conda and python 3.10.x
4- create endpoint
5- create acl_dependencies directory at /home/<usr>/.globus_compute/<endpoint>
6- copy globus_endpoint_files in  /home/<usr>/.globus_compute/<endpoint>/acl_dependencies
7- copy testing profiles and jupyter notebooks at the client node
8- run the notebook from that client. Note v01 shows the complete workflow with ORNL instrument files (kept for potential development purposes), while v02 is for reproducibility.
9- have fun!
