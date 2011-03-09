
QRC_FILES=$(shell find ./ -iname "*.qrc")

.PHONY: gui


all: resources gui

	${MAKE} -C config
	${MAKE} -C resources/svg
gui: 
	${MAKE} -C gui

resources: res_rc.py

clean_res:
	@rm res_rc.py

re_res: clean_res resources

res_rc.py: res.qrc
	pyrcc4 -py2 $^ -o $@
	@du -hcs $@ | tail -n1


