PLATFORM=$(shell python -c "import sys; print(sys.platform)")
H2XML=../tools/ctypeslib/scripts/h2xml.py
XML2PY=../tools/ctypeslib/scripts/xml2py.py
ONIGOUTPUT=
QRC_FILES=$(shell find ./ -iname "*.qrc")




all: oniguruma resources
	
	${MAKE} -C gui
	${MAKE} -C config
	
resources: res_rc.py

res_rc.py: res.qrc
	pyrcc4 -py2 $^ -o $@
	
oniguruma:
	#TODO: Hacer compilación segun plataforma
	@echo ${PLATFORM} 
	${H2XML} oniguruma.h -o ongdefs.xml
	${XML2PY} -c -d -l libonig.so -v -o lib/ctypes/onig_${PLATFORM}.py ongdefs.xml
	