SOURCES = $(wildcard *.c)
TARGETS = $(patsubst %.c,%,${SOURCES})

all: ${TARGETS}
	
	
%: %.c
	@echo $^ -> $@
	gcc -lonig -o $@ $^ 
	
	
