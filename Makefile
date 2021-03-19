
env:
	bash -c "python3 -m venv venv"
	bash -c "source venv/bin/activate && python -m pip install --upgrade pip"
	bash -c "source venv/bin/activate && python -m pip install -r requirements.txt"

virtualbox-0:
	bash -c "source venv/bin/activate && bin/generate_Vagrantfile.py vb -f 0 -t 1 -n 5,6"

virtualbox-1:
	bash -c "source venv/bin/activate && bin/generate_Vagrantfile.py vb -f 2 -t 4"

up:
	vagrant up

status:
	vagrant status

playbook:
	ansible-playbook -i playbooks/inventory/wolk.ini playbooks/wolk.yml --vault-password-file ~/tmp/kubernetes.txt

all-1: env virtualbox-1 up playbook

destroy:
	vagrant destroy -f
	#deactivate
	#rm -rf venv
