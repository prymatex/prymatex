#include "mydefs.h"
#include <math.h>

float distancia(Point *p1, Point *p2) {
	// Simple pitagoras
	float dx, dy;
	dx = p1->x - p2->x;
	dy = p1->y - p2->y;
	return sqrt( dx * dx + dy * dy);
}
