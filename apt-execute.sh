cp ./ali-cloud-mirror.list /etc/apt/sources.list.d;
mv /etc/apt/sources.list /etc/apt/sources-list-backup;
RUN	apt update;
apt install -y curl net-tools;