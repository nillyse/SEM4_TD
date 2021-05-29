#include "pch.h"
#include <iostream>
#include <vector>
#include <complex>
#include <fstream>
#include <string>
#include <stdio.h>
#include <utility>
#define PI 3.14159265358979323846

double A = 6.0;
double B = 4.0;
double C = 3.0;

double funkcja(double t) {
	double a = 1.0;
	double fi = C * PI;
	double f = B;
	return a * sin(2 * PI * f*t + fi);

}

std::vector<double> xx(int czestotliwosc, double start, double ilosc_probek) {
	double krok = 1.0 / czestotliwosc;
	std::vector<double> tab;
	for (double i = 0; i < ilosc_probek; i++) {
		tab.push_back(start);
		start += krok;
	}
	return tab;
}

std::vector<double> probkowanie(std::vector<double> x) {
	std::vector<double> tab;
	for (double var : x) {
		tab.push_back(funkcja(var));
	}
	return tab;
}

std::vector<std::complex<double>> fourier(std::vector<double> x) {
	std::vector<std::complex<double>> wynik;
	std::complex<double> wartosc(0.0);
	for (int i = 0; i < x.size(); i++) {
		wartosc.real(0);
		wartosc.imag(0);
		for (int j = 0; j < x.size(); j++) {
			wartosc.real(wartosc.real() + cos((-PI * 2.0 * i * j) / (double)x.size()) * x[j]);
			wartosc.imag(wartosc.imag()+ sin((-PI * 2.0 * i * j) / (double)x.size()) * x[j]);
		}
		wynik.push_back(wartosc);
	}
	return wynik;
}


std::vector<double> reverse_fourier(std::vector<std::complex<double>> x) {
	std::vector<double> wynik;
	std::complex<double> wartosc(0.0);
	double w = 0;
	for (int i = 0; i < x.size(); i++) {
		wartosc.real(0);
		wartosc.imag(0);
		for (int j = 0; j < x.size(); j++) {
			wartosc.real(wartosc.real() + cos((-PI * 2.0 * i * j) / x.size()) * x[j].real());
			wartosc.imag(wartosc.imag() + sin((-PI * 2.0 * i * j) / x.size()) * x[j].imag());
			}
		w = (wartosc.real() + wartosc.imag())/x.size();
		wynik.push_back(w);
	}
	return wynik;
}

std::vector<double> widmo_amplitudowe(std::vector<std::complex<double>> x) {
	std::vector<double> wynik;
	for (std::complex<double> var : x) {
		wynik.push_back(sqrt(pow(var.real(), 2) + pow(var.imag(), 2))/x.size()*2.0);
	}
	return wynik;
}

std::vector<double> skala_czestotliwosci(int czestotliwosc, int n) {
	std::vector<double> wynik;
	for (int i = 0; i < n; i++) {
		wynik.push_back((double)i*(czestotliwosc/(double)n));
	}
	return wynik;
}

std::vector<std::pair<double, double>> skala_decybelowa(std::vector<std::pair<double, double>> xy) {
	std::vector<std::pair<double, double>> wynik;
	int i = 0;
	for (auto var : xy) {
		wynik.push_back(std::pair<double, double>(xy.at(i).first,10* log10(var.second)));
		i++;
	}
	return wynik;
}

void write_to_file(const char* filename, std::vector<double> x, std::vector<double> y) {
	FILE *fp;
	fp = fopen(filename, "w");
	int i = 0;
	for(double var : x) {
		fprintf(fp, "%f;%f\n", var, y.at(i));
		i++;
	}
	fclose(fp);
}

void write_to_file(std::string filename, std::vector<double> x, std::vector<std::pair<double, double>> xy) {
	FILE *fp;
	fp = fopen(filename.c_str(), "w");
	int i = 0;
	for (auto var : xy) {
		fprintf(fp, "%f;%f\n", var.first, var.second);
		i++;
	}
	fclose(fp);
}



std::vector<std::pair<double, double>>wczytaj_xy(std::string filename, double ilosc_probek) {
	//FILE *fp;
	//fp = fopen(filename, "r");

	std::ifstream myfile(std::string(filename)+".csv");
	if (!myfile)
	{
		printf("aaa");
		perror("File error: ");
		system("pause");
		exit(EXIT_FAILURE);
	}
	double x = 0, y = 0;
	char srednik;
	std::vector<std::pair<double, double>> xy;

	while (myfile >> x >> srednik >> y)
	{
		xy.push_back(std::pair<double, double>(x, y));
	}
	int n = floor(xy.size() / ilosc_probek);
	std::vector<std::pair<double, double>> xy_final;
	for (int i = 0, j = 0; i < ilosc_probek; i++, j+=n) {
		xy_final.push_back(xy.at(j));
	}
	return xy_final;	
}

std::vector<std::pair<double, double>> divide(std::vector<double> y, std::vector<double> x) {
	std::vector<double> new_x;
	std::vector<double> new_y;
	for (int i = 0; i < (x.size() / 2); i++) {
		new_x.push_back(x.at(i));
		new_y.push_back(y.at(i));
	}
	std::vector<std::pair<double, double>> xy;
	int i = 0;
	for (auto var : new_y) {
		xy.push_back(std::pair<double, double>(x.at(i), var));
		i++;
	}

	return xy;
}

double find_max(std::vector<std::pair<double, double>> xy) {
	double max = xy.at(0).second;
	for (auto var : xy) {
		if (var.second > max) {
			max = var.second;
		}
	}
	return max;
}


std::vector<std::pair<double, double>> filtr(std::vector<std::pair<double, double>> xy, double prog) {
	std::vector<std::pair<double, double>> new_xy;
	double cut = find_max(xy) / prog;
	for (auto var : xy) {
		if (abs(var.second) < cut) {
			continue;
		}
		new_xy.push_back(var);
	}
	return new_xy;
}


void zadanie(std::string filename, double prog) {
	double start = 0.0;
	double ilosc_probek = 100 * A + 10 * B + C;
	int czestotliwosc = 22050;
	std::vector<std::pair<double, double>> xy = wczytaj_xy("wynik\\"+filename, ilosc_probek);
	std::vector<double> x, y;
	for (auto xyvar : xy)
	{
		x.push_back(std::move(xyvar.first));
		y.push_back(std::move(xyvar.second));
	}
	std::vector<std::complex<double>> wynik = fourier(y);
	std::vector<double> widmo = widmo_amplitudowe(wynik);
	std::vector<double> skala = skala_czestotliwosci(czestotliwosc, ilosc_probek);
	xy = divide(widmo, skala);
	xy = filtr(xy, prog);
	std::vector<std::pair<double, double>> db = skala_decybelowa(xy);
	write_to_file("wynik\\widmo_"+filename+".csv", skala, xy);
	write_to_file("wynik\\skala_decybelowa_" + filename + ".csv", skala, db);
}


int main()
{
	double start = 0.0;
	double ilosc_probek = 100 * A + 10 * B + C;
	int czestotliwosc = 800;
	std::vector<double> x = xx(czestotliwosc, start, ilosc_probek);
	std::vector<double> y = probkowanie(x);
	write_to_file("probkowanie.csv", x, y);

	std::vector<std::complex<double>> wynik = fourier(y);
	std::vector<double> widmo = widmo_amplitudowe(wynik);


	std::vector<double> skala = skala_czestotliwosci(czestotliwosc, ilosc_probek);
	std::vector<std::pair<double, double>> xy = divide(widmo, skala);
	xy = filtr(xy, 100);
	std::vector<std::pair<double, double>> db = skala_decybelowa(xy);
	write_to_file("wynik\\widmo.csv", skala, xy);
	write_to_file("wynik\\skala_decybelowa.csv", skala, db);
	zadanie("p1", 50);
	zadanie("p2", 50);
	zadanie("p3", 50);
	zadanie("u", 100);
	zadanie("v", 100);
	zadanie("x", 100);
	zadanie("y", 100);
	zadanie("z", 100);
	y = reverse_fourier(wynik);
	write_to_file("wynik\\odwrocenie.csv", x, y);

}

