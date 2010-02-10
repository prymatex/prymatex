
INKSCAPE=$(shell which inkscape)
INKSCAPE_FLAGS=-z -C -d120


all: Prymatex_Logo.png Prymatex_Splash.png



%.png: %.svg
	${INKSCAPE} ${INKSCAPE_FLAGS} $^ -e $@
	cp $@ ../src/prymatex/resources/icons/


clean:
	-rm -rf *.png
	
re: clean all
