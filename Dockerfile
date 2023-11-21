FROM tensorflow/tensorflow:latest-gpu-jupyter

RUN pip3 install keras --no-deps
RUN pip3 install opencv-python
RUN pip3 install scipy
RUN pip3 install pyyaml
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install matplotlib
RUN pip3 install -U scikit-learn
RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y
