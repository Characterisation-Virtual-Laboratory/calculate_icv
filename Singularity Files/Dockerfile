FROM ubuntu:20.04 AS spython-base
ADD dependencies.R /opt/dependencies.R
LABEL MAINTAINER_NAME  Jay van Schyndel
LABEL MAINTAINER_EMAIL jay.vanschyndel@monash.edu
LABEL APPLICATION_NAME ubuntu + cuda
LABEL APPLICATION_VERSION 20.04
LABEL HARDWARE gpu
LABEL LAST_UPDATED 01-DEC-2020
ENV CUDABINPATH=/usr/local/cuda/bin
ENV CUDALIBPATH=/usr/local/cuda/lib64/stubs:/usr/local/cuda/lib64/:/usr/local/cuda/lib
ENV PATH=$PATH:$CUDABINPATH
ENV LD_LIBRARY_PATH=$CUDALIBPATH:$LD_LIBRARY_PATH
RUN echo "*********************************************************"
RUN echo "Setup and display environment"
RUN echo "*********************************************************"
RUN export LC_ALL=en_AU.UTF-8
RUN export LANGUAGE=en_AU.UTF-8
ARG DEBIAN_FRONTEND=noninteractive
RUN echo $LC_ALL
RUN echo $LANGUAGE
RUN echo $DEBIAN_FRONTEND
RUN echo "*********************************************************"
RUN echo "Install repositories"
RUN echo "*********************************************************"
RUN apt update
RUN apt-get install -y software-properties-common
RUN apt-add-repository -y 'deb http://us.archive.ubuntu.com/ubuntu/ focal main restricted'
RUN apt-add-repository -y 'deb http://us.archive.ubuntu.com/ubuntu/ focal-updates main restricted'
RUN apt-add-repository -y 'deb http://us.archive.ubuntu.com/ubuntu/ focal universe'
RUN apt-add-repository -y 'deb http://us.archive.ubuntu.com/ubuntu/ focal-updates universe'
RUN echo "*********************************************************"
RUN echo "Update repositories and install desktop"
RUN echo "*********************************************************"
RUN apt update
RUN apt upgrade -y
RUN apt install -y locales
RUN locale-gen en_AU.UTF-8
RUN apt install -y wget ubuntu-desktop vim software-properties-common git cmake mesa-utils sudo build-essential gpg-agent
RUN echo "*********************************************************"
RUN echo "Installing CUDA 11.0"
RUN echo "*********************************************************"
RUN apt-get install -y g++ freeglut3-dev build-essential libx11-dev libxmu-dev libxi-dev libglu1-mesa libglu1-mesa-dev mesa-utils libgl1-mesa-glx
RUN apt-get install -y gcc-10
RUN cd /tmp
RUN wget https://developer.download.nvidia.com/compute/cuda/11.0.3/local_installers/cuda_11.0.3_450.51.06_linux.run
RUN chmod +x cuda_11.0.3_450.51.06_linux.run
RUN ./cuda_11.0.3_450.51.06_linux.run --silent --toolkit --toolkitpath=/usr/local/cuda-11.0/ --samples --samplespath=/usr/local/cuda-11.0-samples/ --override
RUN ln -s /usr/local/cuda-11.0 /usr/local/cuda
RUN ln -s /usr/bin/gcc-6 /usr/local/cuda/bin/gcc
RUN ln -s /usr/bin/g++-6 /usr/local/cuda/bin/g++
RUN rm -rf cuda_11.0.3_450.51.06_linux.run
RUN echo "*********************************************************"
RUN echo "Installing python dependencies"
RUN echo "*********************************************************"
RUN apt install -y python3-pip python3-pyqt5 pyqt5-dev python3-tk python3-pandas python3-fire python3-tabulate python3-colorama
RUN echo "*********************************************************"
RUN echo "Installing vglrun and TurboVNC"
RUN echo "*********************************************************"
RUN wget https://swift.rc.nectar.org.au/v1/AUTH_810/CVL-Singularity-External-Files/turbovnc_2.2.5_amd64.deb
RUN dpkg -i turbovnc_2.2.5_amd64.deb
RUN wget https://swift.rc.nectar.org.au/v1/AUTH_810/CVL-Singularity-External-Files/virtualgl_2.6.4_amd64.deb
RUN dpkg -i virtualgl_2.6.4_amd64.deb
RUN apt update
RUN apt -y upgrade
RUN rm -rf turbovnc_2.2.5_amd64.deb virtualgl_2.6.4_amd64.deb
RUN echo "*********************************************************"
RUN echo "Installing R and dependencies"
RUN echo "*********************************************************"
RUN apt -y install dirmngr gnupg apt-transport-https ca-certificates software-properties-common
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
RUN add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/'
RUN apt -y install r-base
RUN apt update
RUN apt -y install r-base gdebi-core libssl-dev curl libxml2-dev libcurl4-openssl-dev
RUN cd /tmp/ && wget https://download1.rstudio.org/desktop/bionic/amd64/rstudio-1.4.1106-amd64.deb
RUN gdebi -q -n /tmp/rstudio-1.4.1106-amd64.deb
RUN rm -rf /tmp/rstudio-1.4.1106-amd64.deb
RUN Rscript /opt/dependencies.R
CMD $*
