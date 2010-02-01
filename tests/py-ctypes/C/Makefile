GCC=gcc
CFLAGS=-lm
TARGETS=test
LIBNAME_SHORT=mylib
LIBNAME_SO=${LIBNAME_SHORT}.so
LIBNAME=lib${LIBNAME_SO}.0

all: libs test 

test: main.o
	${GCC} ${CFLAGS} $^ -o $@ -L. -l${LIBNAME_SHORT} 

clean:
	-rm -rf ${TARGETS} *.so* *.o

re: clean all

%.o: %.c
	${GCC} -fPIC -g -c -Wall $^ -o $@

libs: ${LIBNAME}
	ldconfig -vn ./	
	
${LIBNAME}: mylib.o
	${GCC} -Wl,-soname,${LIBNAME_SO} -shared -fPIC -lm -o ${LIBNAME} $^
	ln -sf ${LIBNAME} lib${LIBNAME_SO}
	