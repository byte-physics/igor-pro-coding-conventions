FROM debian:stretch
MAINTAINER Matthias J. Kastner matthias.kastner@byte-physics.de

# download appropriate packages
RUN	apt-get update --quiet \
	&& DEBIAN_FRONTEND=noninteractive \
	apt-get install --assume-yes --quiet --no-install-recommends \
		python \
		python-pygments \
		texlive-base \
		texlive-latex-base \
		texlive-latex-extra \
		texlive-latex-recommended \
		texlive-luatex

# clean up container
RUN DEBIAN_FRONTEND=noninteractive \
	apt-get --purge remove tex.\*-doc$ \
	&& apt-get clean

RUN DEBIAN_FRONTEND=noninteractive luaotfload-tool --update

WORKDIR /opt/latex
