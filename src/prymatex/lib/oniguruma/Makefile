# Oniguruma Makefile for Python wrapper
#
#

PLATFORM=$(shell python -c "import sys; print(sys.platform)")
H2XML = ctypeslib/scripts/h2xml.py
XML2PY = ctypeslib/scripts/xml2py.py
ONIGOUTPUT=ctypes_output/

.PHONY:  pyrex re clean

all: cython

oniguruma:
	@#TODO: Hacer compilación segun plataforma
	@echo ${PLATFORM} 
	${H2XML} -D ONIG_NORMAL oniguruma.h -o ${ONIGOUTPUT}ongdefs.xml
	${XML2PY} -c -d -l libonig.so -v -o ${ONIGOUTPUT}onig_${PLATFORM}.py ${ONIGOUTPUT}ongdefs.xml

cython: pyonig.so

%.c: %.pyx
	cython $^

%.o: %.c
	gcc -c -fPIC -I/usr/include/python2.6 $^ -o $@

pyonig.so: pyonig.o
	gcc -shared $^ -lonig -o $@

clean:
	@rm -rf pyonig.so pyonig.o pyonig.c

re:	clean all
