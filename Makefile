
env:
	bash -c "python3 -m venv venv"
	bash -c "source venv/bin/activate && pip install --upgrade pip"
	bash -c "source venv/bin/activate && pip install -r requirements.txt"

virtualbox-0a:
	bash -c "source venv/bin/activate && bin/generate_Vagrantfile.py vb -c 1 -f 0 -t 1"

virtualbox-0b:
	bash -c "source venv/bin/activate && bin/generate_Vagrantfile.py vb -f 5 -t 6"

virtualbox-1:
	bash -c "source venv/bin/activate && bin/generate_Vagrantfile.py vb -c 2,3 -f 2 -t 4"

up:
	vagrant up

status:
	vagrant status

playbook:
	ansible-playbook -i playbooks/inventory/wolk.ini playbooks/wolk.yml --vault-pass ~/tmp/kubernetes.txt

all-1:
	env
	virtualbox-1
	up