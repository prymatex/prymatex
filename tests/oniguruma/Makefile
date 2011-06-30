CC=gcc
CFLAGS=-Wall
LFLAGS=-lonig

all: basic_usage

basic_usage: basic_usage.o
	${CC} ${CFLAGS} ${LFLAGS} $^ -o $@
	
%.o: %.c
	${CC} ${CFLAGS} -c $^ -o $@