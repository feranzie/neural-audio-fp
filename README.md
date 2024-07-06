
#install nvidia driver
sudo apt update
sudo apt upgrade -y

sudo apt install build-essential dkms


sudo apt install nvidia-driver-470
sudo reboot

#install docker
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install -y docker-ce

#config nvidia docker
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt update

sudo apt install -y nvidia-docker2
sudo systemctl restart docker


#pull docker image

sudo docker pull mimbres/neural-audio-fp:cuda11.2.0-cudnn8

#commands
# run docker
sudo docker run --gpus all -it --rm mimbres/neural-audio-fp:cuda11.2.0-cudnn8 /bin/bash

pip install kaggle
apt-get update
apt-get install -y vim
vim kaggle.json ---paste creds
mkdir ~/.kaggle/
cp kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json
kaggle datasets download -d mimbres/neural-audio-fingerprint



# install unzip
apt-get update
apt-get install unzip

unzip neural-audio-fingerprint.zip

#change name of folder
mv neural-audio-fp-dataset fingerprint_dataset_icassp2021

cd neural-audio-fp
CUDA_VISIBLE_DEVICES=0 python run.py train CHECKPOINT --max_epoch=20 -c default



sudo docker run --gpus all -it --rm neural-audio:4 /bin/bash
cp neural-audio-fp/eval/test_ids_icassp2021.npy .



sudo docker cp /home/paperspace/test_ids_icassp2021.npy 2bbd74c36673:/work/neural-audi
o-fp/eval/
86678_SENSAZIONI.wav



python run.py train custom --max_epoch=20 -c default


# add SSH to machine
echo "" >> ~/.ssh/authorized_keys