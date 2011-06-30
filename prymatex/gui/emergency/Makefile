# Basados en el manual de GNU Make 
# http://www.gnu.org/software/make/manual/make.html#Wildcard-Examples

# pyuic es el compilador de UI (Qt XML) a Python 
PYUIC=pyuic4
PYUIC_FLAGS=-x --from-imports
UI_BASE=ui_files
UI_FILES=$(notdir $(shell ls ${UI_BASE}/*.ui))
PY_FILES=$(patsubst %.ui,ui_%.py,${UI_FILES})

all: ${PY_FILES} 
	
ui_%.py: ui_files/%.ui
	${PYUIC} ${PYUIC_FLAGS} $^ -o $@
	
clean:
	-rm ${PY_FILES}

re: clean all

help:
	@echo "${MAKE} all | clean | re"
	@echo "Compila los archivos de ui_files/*.ui en ui_NOMBREARCHIVO.py" 
