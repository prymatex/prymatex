# Oniguruma Makefile for Python wrapper
#
#

PLATFORM=$(shell python -c "import sys; print(sys.platform)")
H2XML = ctypeslib/scripts/h2xml.py
XML2PY = ctypeslib/scripts/xml2py.py
ONIGOUTPUT=ctypes_output/


oniguruma:
	@#TODO: Hacer compilación segun plataforma
	@echo ${PLATFORM} 
	${H2XML} -D ONIG_NORMAL oniguruma.h -o ${ONIGOUTPUT}ongdefs.xml
	${XML2PY} -c -d -l libonig.so -v -o ${ONIGOUTPUT}onig_${PLATFORM}.py ${ONIGOUTPUT}ongdefs.xml
