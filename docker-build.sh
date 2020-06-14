#!/bin/bash

# script checks for correct installation and executes build-documentation afterwards
# output is verbose
#
# check installation
if [ ! $(docker -v | grep -c -w version) -eq 1 ]; then
	echo "docker not found. installing."
	sudo apt-get -y -q install docker.io
fi
if [ ! $(groups | grep -c -w docker) -eq 1 ]; then
	echo "adding current user to docker group."
	sudo usermod -aG docker $(whoami)
	echo "please log off for changes to take affect."
	exit 0
fi
# build containter
echo "start building Docker container 'texlive2016-pygments'"
docker build -t texlive2016-pygments -f docker/Dockerfile .
# show current LuaLaTEX version
echo "LuaLaTEX " $(docker run -it --rm -v $(pwd):/opt/latex texlive2016-pygments lualatex -v | egrep -o "Version\ ([0-9.]+)")
#
# clean up previously generated minted output
# uncomment this if an error occured!
# docker run -it --rm -v $(pwd):/opt/latex texlive2016-pygments rm -R /opt/latex/_minted-*
#
echo "building coding_conventions.pdf"
docker run -it --rm -v $(pwd):/opt/latex texlive2016-pygments lualatex --shell-escape coding_conventions.tex
echo "building coding_bestpractices.pdf"
docker run -it --rm -v $(pwd):/opt/latex texlive2016-pygments lualatex --shell-escape coding_bestpractices.tex
