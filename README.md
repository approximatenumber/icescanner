# Installation

```
pip3 install pipenv
pipenv install
```

# Run

```
pipenv shell
python3.7 icescanner.py run config/config.yaml
```

# Run only diagnostics
```
pipenv shell
python3.7 icescanner.py diagnostics config/config.yaml
```
# Configuration file

Main configuration file.

* `common`: common section
  * `server_ip`: IP address of main server
  * `shot_frequency`: timeout between shots
* `credentials`: credentials
  * `cameras`: camera section
* `devices`: devices section
  * `device_type`:
    * `ip`: IP address of device
    * `is_enabled`: use `False` to disable this device

## Configuration example:
```yaml
# port = left
# star = right
# stern = rear
# fore = front

common:
  server_ip: 192.168.0.168
  shot_frequency: 30s
  root_dir: /opt/datasets

credentials:
  cameras: &default_camera_creds
    username: user
    password: pass

devices:
  cameras:
    port_camera:
      is_enabled: False
      ip: 192.168.1.1
    star_camera:
      is_enabled: False
      ip: 192.168.1.2
    stern_camera:
      is_enabled: False
      ip: 192.168.1.3
    fore_camera:
      is_enabled: False
      ip: 192.168.1.4
  lidars:
    port_lidar:
      is_enabled: True
      ip: 192.168.0.178
    star_lidar:
      is_enabled: True
      ip: 192.168.0.188
    stern_lidar:
      is_enabled: False
      ip: 192.168.1.7
    fore_lidar:
      is_enabled: False
      ip: 192.168.1.8
```
