
QRC_FILES=$(shell find ./ -iname "*.qrc")

.PHONY: gui


all: oniguruma resources gui

	${MAKE} -C config
gui: 
	${MAKE} -C gui

resources: res_rc.py

clean_res:
	@rm res_rc.py

re_res: clean_res resources

res_rc.py: res.qrc
	pyrcc4 -py2 $^ -o $@
	@du -hcs $@ | tail -n1

oniguruma:
	$(MAKE) -C lib/oniguruma



