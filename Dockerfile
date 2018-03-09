FROM ubuntu:16.04
LABEL maintainer=”Eckhart” 
LABEL Remove image distortion

# install Python
RUN apt-get -y update && apt-get install -y python2.7 python-pip

# install iCommands
#RUN apt-get install irods-icommands

# install required Python modules
#RUN pip install matplotlib=='1.5.1'
RUN pip install astropy=='2.0.2'
RUN pip install scipy=='0.17.0' 
RUN pip install argparse

# add a file
#ADD apply_dewarp_soln.py /usr/src/
ADD . usr/src/

# verify permissions
RUN chmod +x /usr/src/apply_dewarp_soln.py

# alternative way of obtaining Python modules
# COPY requirements.txt [...location here…]
# RUN pip2 install -r requirements.txt

# fetch the data from a CyVerse Atmosphere volume
# (passed locally)

# the below script contains a path stem to fetch the data; is there a more generalizable 
# way of writing the path in the script? 

# run the application
CMD ["python", "/usr/src/apply_dewarp_soln.py"]

