
ICONS = ../icons/command.png ../icons/snippet.png ../icons/perference.png ../icons/menu.png ../icons/command.png ../icons/drag.png ../icons/language.png ../icons/template.png ../icons/bundle.png

all: ${ICONS}
	

../icons/%.png: bundle.svg
	inkscape -i $(patsubst ../icons/%.png,%,$@) -d 24 -e $@ $^
	convert $@ $@



clean:
	@rm -rf ${ICONS}

re: clean all
