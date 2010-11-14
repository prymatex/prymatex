
QRC_FILES=$(shell find ./ -iname "*.qrc")




all: oniguruma resources
	
	${MAKE} -C gui
	${MAKE} -C config
	
resources: res_rc.py

res_rc.py: res.qrc
	pyrcc4 -py2 $^ -o $@
	
oniguruma:
	$(MAKE) -C lib/oniguruma