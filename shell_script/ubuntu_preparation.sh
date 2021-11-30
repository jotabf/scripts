echo "alias matlab='/usr/local/MATLAB/R2017a/bin/matlab &'
alias vpnc-sd='sudo vpnc /etc/vpnc/sdumont.conf'
alias sdumont='mkdir -p ~/sshfs/sdumont-home | mkdir -p ~/sshfs/sdumont-scratch | sshfs sdumont:/prj/ctws-fwi/joao.fernandes ~/sshfs/sdumont-home | sshfs sdumont:/scratch/ctws-fwi/joao.fernandes ~/sshfs/sdumont-scratch'
alias npad='mkdir -p ~/sshfs/npad-home | mkdir -p ~/sshfs/npad-scratch | sshfs npad:/home/jbfernandes ~/sshfs/npad-home | sshfs npad:/scratch/global/jbfernandes ~/sshfs/npad-scratch'
alias yemoja='mkdir -p ~/sshfs/yemoja-home | mkdir -p ~/sshfs/yemoja-scratch | sshfs yemoja:/home/joao.bfernandes ~/sshfs/yemoja-home | sshfs yemoja:/scratch/joao.bfernandes ~/sshfs/yemoja-scratch'
alias leuven='mkdir -p ~/sshfs/leuven | sshfs leuven:/home/jbfernandes ~/sshfs/leuven'
alias macken='mkdir -p ~/sshfs/mackenzie | sshfs macken:/home/joao ~/sshfs/mackenzie'
alias ogun='mkdir -p ~/sshfs/ogun-home | mkdir -p ~/sshfs/ogun-scratch | sshfs ogun:/home/samuel.xavier ~/sshfs/ogun-home | sshfs ogun:/scratch/samuel.xavier ~/sshfs/ogun-scratch'
alias drive='google-drive-ocamlfuse -label ufrn ~/Drive'
alias uyemoja='sudo umount ~/sshfs/yemoja-home | sudo umount ~/sshfs/yemoja-scratch'
alias unpad='sudo umount -f ~/sshfs/npad-home | sudo umount -f ~/sshfs/npad-scratch'
alias uleuven='sudo umount ~/sshfs/leuven'
alias umacken='sudo umount ~/sshfs/mackenzie'
alias usdumont='sudo vpnc-disconnect | sudo umount ~/sshfs/sdumont-home | sudo umount -f ~/sshfs/sdumont-scratch'
alias uogun='sudo umount -f ~/sshfs/ogun-home | sudo umount -f ~/sshfs/ogun-scratch'
alias firessh='ssh -N -D 9090 -o ConnectTimeout=99'
" >> /home/$USER/.bashrc;

mkdir ~/.ssh; wait
echo "Host yemoja
        HostName ws-05.fieb.org.br
        User joao.bfernandes
        Port 5001
Host npad
        HostName sc.npad.imd.ufrn.br
        User jbfernandes
        Port 4422
Host leuven
        HostName leuven.dca.ufrn.br
        User jbfernandes
        Port 2222
Host macken
        HostName lspd.mackenzie.br
        User joao
        Port 2222
Host sdumont
        HostName login.sdumont.lncc.br
        User joao.fernandes
Host ogun
        HostName 200.9.65.60
        User samuel.xavier
Host sasha
	HostName sasha.imd.ufrn.br
	Port 2046
	User jfernandes
" > ~/.ssh/config

sudo touch /etc/init.d/jbInit.sh; wait


##Install Programs##
sudo apt update; wait
sudo apt install apt-transport-https ca-certificates wget software-properties-common; wait

#Sublime-text
wget -q https://download.sublimetext.com/sublimehq-pub.gpg -O- | sudo apt-key add -; wait
sudo add-apt-repository "deb https://download.sublimetext.com/ apt/stable/"; wait

sudo apt update; wait
sudo apt install sublime-text; wait

#Visual Studio Code
wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -; wait
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"; wait

sudo apt update; wait
sudo apt install code; wait

#Git
sudo apt install git; wait

#Htop
sudo snap install htop; wait

#xTerm
sudo apt install xterm; wait

#SSHFS
sudo apt install sshfs; wait

#Mendelay
xdg-open https://www.mendeley.com/repositories/ubuntu/stable/amd64/mendeleydesktop-latest/; wait

#Rambox
sudo snap install rambox; wait

#Python-PIP
sudo apt install python3-pip; wait

#OpenMPI
sudo apt-get install openmpi-bin; wait

#Ocamlfuse
sudo add-apt-repository ppa:alessandro-strada/ppa; wait
sudo apt-get update; wait
sudo apt-get install google-drive-ocamlfuse; wait

google-drive-ocamlfuse ~/Documents/; wait
sed -i 's+root_folder=.*+root_folder=1Kx_m9h2yWw9e0G2Br-u_S9GyGIWdLmMN+g' ~/.gdfuse/default/config; wait

sudo chmod 777 /etc/init.d/jbInit.sh; wait
sudo echo "google-drive-ocamlfuse ~/Documents/; wait" >> /etc/init.d/jbInit.sh; wait

#Slack
sudo snap install slack --classic

