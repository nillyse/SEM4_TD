#include "pch.h"
#include <iostream>
#include <math.h>
#include <string>


#define PI 3.14159265358979323846

float a = 6.0;
float b = 4.0;
float c = 3.0;
int n[4] = { 2, 4, a * 10 + b };

float wyroznik() {
	return (b *b) - (4 * a*c);
}

void miejsca_zerowe() {
	float t1, t2;
	float delta = wyroznik();
	if (delta > 0) {
		t1 = (-b + sqrt(delta)) / 2 * a;
		t2 = (-b - sqrt(delta)) / 2 * a;
		printf("Miejsca zerowe: %f, %f", t1, t2);

	}
	else if (delta < 0) {
		printf("nie ma miejsca zerowego");
	}
	else {
		t1 = t2 = (-b) / 2*a;
		printf("Miejsce zerowe: %f", t1);
	}
}

void write_to_file(float start, float end, float krok, float (*f)(float), const char* filename) {
	FILE *fp;
	fp = fopen(filename, "w");
	float y;
	while (start <= end) {
		y = f(start);
		fprintf(fp, "%f;%f\n", start, y);
		start += krok;
	}
	fclose(fp);
}


float x(float t) {
	return (a * t * t) + (b*t) + c;
}

float y(float t) {
	return 2 * (x(t) * x(t)) + 12 * cos(t);
}

float z(float t) {
	return sin(2 * PI * 7 * t) * x(t) - 0.2 * log10(abs(y(t) + PI));
}

float u(float t) {
	return sqrt(abs(y(t)*y(t)*z(t))) - 1.8 * sin(0.4*t*z(t) * x(t));
}

float v(float t) {
	if (t < 0.22 && t> 0)
		return (1 - 7 * t) * sin((2 * PI*t * 10) / (t + 0.04));
	else if (t < 0.7 && t >= 0.22)
		return 0.63 * t * sin(125 * t);
	else if (t <= 1 && t >= 0.7)
		return pow(t, -0.662) + 0.77* sin(8 * t);
}

float p1(float t) {
	float wynik = 0;
	for(int i = 1; i<=n[0]; i++)
		wynik += (cos(12 * t*(i * i)) + cos(16 * t * i)) / (i * i);
	return wynik;
}

float p2(float t) {
	float wynik = 0;
	for (int i = 1; i <= n[1]; i++)
		wynik += (cos(12 * t*(i * i)) + cos(16 * t * i)) / (i * i);
	return wynik;
}

float p3(float t) {
	float wynik = 0;
	for (int i = 1; i <= n[2]; i++)
		wynik += (cos(12 * t*(i * i)) + cos(16 * t * i)) / (i * i);
	return wynik;
}



int main()
{
	float t = 1.0/22050;
	write_to_file(-10, 10, t, x, "x.csv");
	write_to_file(0, 1, t, y, "y.csv");
	write_to_file(0, 1, t, z, "z.csv");
	write_to_file(0, 1, t, u, "u.csv");
	write_to_file(0, 1, t, v, "v.csv");
	write_to_file(0, 1, t, p1, "p1.csv");
	write_to_file(0, 1, t, p2, "p2.csv");
	write_to_file(0, 1, t, p3, "p3.csv");


}
