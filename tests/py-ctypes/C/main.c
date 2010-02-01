#include <stdio.h>
#include <math.h>
#include <malloc.h>
#include "mydefs.h"

// Esta prueba utiliza la librería mylib.so donde llama
// a la función distancia(Point *p, Point *p)

int main(int argc, char **argv) {

	Point *p1 = (Point*) malloc(sizeof(Point));
	Point *p2 = (Point*) malloc(sizeof(Point));
	p1->x = 2;
	p2->x = 4.3;
	p1->y = 20.17;
	p1->y = 55.89;
	printf("La distancia entre los puntos es %f", distancia(p1, p2));
	//printf("El valor del puntero es: %.8x\n", (unsigned int)p1);

}


