# Docker
## General
Docker is an open platform for distributed applications.
Visit http://www.docker.com for further details.
For installing docker see https://docs.docker.com/linux/

## Container
This contains
* debian stretch
* texlive-base
* texlive-latex-base for lualatex
* texlive-luatex for actual luatex support (luaotfload)
* texlive-latex-extra for minted
* texlive-latex-recommended for KOMA-script
* lmodern for lmroman10-regular
* python-pygments

## Generic Docker information
### Build a container
Here we will use the name docker-build for our container
 docker build -t docker-build
The docker container is built from the docker-file in the current working dir.

### Run a command
After building the container it should be listed as an image.
 docker images
to run docker use
 docker run -it --rm -v /my/local/path:/opt/remote/path docker-build echo this is docker
Explaination:
* run docker
* in interactive mode
* overwrite existing instances
* link the local directory /my/local/path to /opt/remote/path in the container
* open the named container image 'docker-build'
* execute a command (echo or uname -r etc.)
