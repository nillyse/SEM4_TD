#include "pch.h"
#include <iostream>
#include <vector>
#define PI 3.14159265358979323846

float A = 6.0;
float B = 4.0;
float C = 3.0;


float funkcja(float t) {
	float a = 1.0;
	float fi = C * PI;
	float f = B;
	return a * sin(2 * PI * f*t + fi);

}

std::vector<float> probkowanie(int czestotliwosc, float start, float end) {
	float krok = 1.0 / czestotliwosc;
	std::vector<float> tab;
	for (float i = start; i < end; i += krok) {
		tab.push_back(funkcja(i));
	}
	return tab;

}


std::vector<int> kwantyzacja(int czestotliwosc, std::vector<float> tab, int q) {
	int podzial = pow(2, q);
	std::vector<int> tablica;
	for (float kwa : tab){
		tablica.push_back(round((kwa * (podzial - 1) + podzial) / 2.0));
	}
	return tablica;
}


void write_to_file(float start, float end, int czestotliwosc, const char* filename, std::vector<float> tab) {
	FILE *fp;
	fp = fopen(filename, "w");
	float krok = 1.0 / czestotliwosc;
	int i = 0;
	while (start <= end) {
		fprintf(fp, "%f;%f\n", start, tab.at(i));
		start += krok;
		i++;
	}
	fclose(fp);
}


void write_to_file(float start, float end, int czestotliwosc, const char* filename, std::vector<int> tab) {
	FILE *fp;
	fp = fopen(filename, "w");
	float krok = 1.0 / czestotliwosc;
	int i = 0;
	while (start <= end) {
		fprintf(fp, "%f;%d\n", start, tab.at(i));
		start += krok;
		i++;
	}
	fclose(fp);
}
// wartość x, liczba skwantyzowana i wartość liczb skwantyzowanych

int main(){
	float start = 0;
	float end = A;
	int q = 16;
	int czestotliwosc = 600;
	std::vector<float> tab = probkowanie(czestotliwosc, start, end);
	std::vector<int> tablica = kwantyzacja(czestotliwosc, tab, q);
	write_to_file(start, end, czestotliwosc, "probkowanie.csv", tab);
	write_to_file(start, end, czestotliwosc, "kwantyzacja.csv", tablica);
	q = 8;
	czestotliwosc /= 2;
	tab = probkowanie(czestotliwosc, start, end);
	tablica = kwantyzacja(czestotliwosc, tab, q);
	write_to_file(start, end, czestotliwosc, "kwantyzacja2.csv", tablica);

}
