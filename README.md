# injector-templates
templates of injector, check how it works

## Requirements
- [Docker](https://www.docker.com/) >= 19.03
- [GNU Make](https://www.gnu.org/software/make/)

## Installation
### Clone repository
```bash
$ git clone https://github.com/hiro-o918/injector-templates
$ cd injector-templates
```

### Build image
```bash
$ make build
```

**NOTE:** <br> 
If you want use GPUs, install [nvidia-drivers](https://github.com/NVIDIA/nvidia-docker/wiki/Frequently-Asked-Questions#how-do-i-install-the-nvidia-driver) and [nvidia-docker](https://github.com/NVIDIA/nvidia-docker) first.


## How to Use
### Run lab
```bash
$ make run
```

### Run bash
```bash
$ make bash
```
