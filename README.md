# DAaaS SSH/hosts config builder

Takes the platform register output and creates nice ssh and hosts aliases, so you can just type

```
ssh ssh_preprod_admin_panel
```

instead of having to look it up. Recommended with ssh bash completion.

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

### Step 3: Add to SSH config

```
cat ssh_config.txt >> ~/.ssh/config
```

### Step 4: Add to hosts file

```
sudo -s
cat hosts.txt >> /etc/hosts
```

### Step 5: Try it out:

```
ssh ssh_preprod_admin_panel
```

## Workspaces

TODO
