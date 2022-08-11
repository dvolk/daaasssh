# DAaaS SSH config builder

Nice platform and workspace ssh aliases:

```
ssh pl_preprod_admin_panel

ssh wk_v1119120_isis_sans2d_preprod_sans
```

Platform hosts are prefixed with `pl_` and workspaces are prefixed with `wk_`

## Setup

*This will overwrite your ssh config*

```
P_USERNAME=... P_PASSWORD=... W_DEV_USERNAME=... W_DEV_PASSWORD=... W_PROD_USERNAME=... W_PROD_PASSWORD=... python3 main.py go
```
