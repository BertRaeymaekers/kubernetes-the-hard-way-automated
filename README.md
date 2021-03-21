Wolk
====

This is me trying to wrap my head around Kubernetes/Docker.

So I'm roughly following Kelsey Hightowers documentation at:
https://github.com/kelseyhightower/kubernetes-the-hard-way/

And making it into something deployable with Vagrant and Ansible.

Follow the steps. For now only VirtualBox (vb) is supported.

Prerequisites
-------------

You'll need:
- python3
- vagrant
- VirtualBox (only supported backend for now)

Step 0
------

Create `group_vars/kubernetes.yml`, preferably as an ansible vault.

Have it contain the following paramters:

- `ca_server`: The server that will serve as a CA. I've tested it with localhost
- `certificate_authority_name`: The name for the CA. I've tested with 'WolkCA'
- `certificate_authority_passphrase`: The passphrase for the CA certificate.
  (i.e. have my laptop be the CA server)
- [`certificate_authority_CN`]: The common name (CN) for the CA. Defaults to certificate_authority_name.
- [`certificate_authority_O`]: The organization (0) for the CA. Defaults to 'FOOBAR'.
- `kubernetes_public_address`: The public addres of your kubenetes cluster.
- [`kubernetes_public_ip`]: The public IP address of tyour kubernets cluster.
- `kubernetes_cluster_ip_range`: The kubernetes cluster ip range (e.g. 192.168.50.0/24)
- `kubernetes_encryption_key`: A base64 encoded encryption key. Generate it with `head -c 32 /dev/urandom | base64`.
- [`kubernetes_cluster_name`]: The kubernetes cluster name. Defaults to 'kubernetes'.
 
Step 1
------

Set up the python virtualenv:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Step 2
------
 
Generate the Vagrantfile with `bin/generate_Vagrantfile.py`. For now the only
type supported is VirtualBox. Don't specify it or pass `vb` to the scripts. The
`--from`/`-f` and `--to`/`-t` parameters will determine the index of the VMs.
So that also determins how many VMs will be generated. The VMs will be named
`wolk<i>`.

**Example**: this will generate a Vagranfile with VMs wolk0, wolk1, wolk2 and wolk3:  
`bin/generate_Vagrantfile.py vb -f 0 -t 3`

