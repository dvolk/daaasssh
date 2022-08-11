# DAaaS SSH/hosts config builder

## Platform hosts

### Step 1: Get platform register json

```
curl https://username:password@host-172-16-112-161.nubes.stfc.ac.uk/hosts/ > platform.json
```

### Step 2: Run main.py

```
python3 main.py
```

This creates hosts.txt, which can be appended to /etc/hosts, and ssh_config.txt, which can be appended to ~/.ssh/config
