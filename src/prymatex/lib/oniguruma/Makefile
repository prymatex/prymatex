# Oniguruma Makefile for Python wrapper
#
#

PLATFORM=$(shell python -c "import sys; print(sys.platform)")

.PHONY:  pyrex re clean onig_pxd

all: cython


cython: pyonig.so

#%.c: %.pyx %.pxd
#	cython $^
#
pyonig.c: pyonig.pyx pyonig.pxd
	cython pyonig.pyx

#onig_pxd: pyonig.pxd

pyonig_defs.pxd: includes/oniguruma.h
	./h2pxd.py -o $@ $^

%.o: %.c
	gcc -c -fPIC -I/usr/include/python2.6 $^ -o $@

pyonig.so: pyonig.o
	gcc -shared $^ -lonig -o $@

clean:
	@rm -rf pyonig.so pyonig.o pyonig.c pyonig.pxd

re:	clean all

pxd_clean:
	-rm *.pxd

pxd_re: pxd_clean pyonig.pxd

