
ckerfile reference: https://docs.docker.com/engine/reference/builder/

FROM ubuntu:16.04
LABEL maintainer=”Eckhart” 
LABEL Remove image distortion

# install Python
RUN apt-get -y update && apt-get install -y python2.7

# install iCommands
RUN apt-get install irods-icommands

# install required Python modules
RUN pip2 install matplotlib=='1.5.1'
RUN pip2 install astropy=='2.0.2'

# alternative way of obtaining Python modules
# COPY requirements.txt [...location here…]
# RUN pip2 install -r requirements.txt

# fetch the data from a CyVerse Atmosphere volume
# (passed locally)

# the below script contains a path stem to fetch the data; is there a more generalizable 
# way of writing the path in the script? 

# run the application
CMD ["python", "apply_dewarp_soln.py"]

