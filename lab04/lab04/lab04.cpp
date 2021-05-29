#include "pch.h"
#include <iostream>
#include <vector>
#include <valarray>
#include <complex>
#include <string>
#define PI 3.14159265358979323846

typedef std::complex<double> Complex;
typedef std::valarray<Complex> CArray;

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


std::vector<std::pair<double, double>> probkowanie(std::vector<double> x) {
	std::vector<std::pair<double, double>> xy;
	for (auto var : x) {
		xy.push_back(std::pair<double, double>(var, funkcja(var)));
	}
	return xy;
}




double modulacja_a(double x ,double y, double ka, int czestotliwosc) {
	return (ka * y + 1) * cos(2 * PI*czestotliwosc * x);
}

double modulacja_f(double x, double y, double kp, int czestotliwosc) {
	return cos(2 * PI*czestotliwosc*x + kp * y);
}

std::vector<std::pair<double, double>> modulacja(std::vector<std::pair<double, double>> xy, double ka, int czestotliwosc, double (*f)(double, double, double, int)) {
	std::vector<std::pair<double, double>> xy_m;
	for (auto var : xy) {
		xy_m.push_back(std::pair<double, double>(var.first, f(var.first, var.second, ka, czestotliwosc)));
	}
	return xy_m;
}


void write_to_file(std::string filename, std::vector<std::pair<double, double>> xy) {
	FILE *fp;
	fp = fopen(filename.c_str(), "w");
	int i = 0;
	for (auto var : xy) {
		fprintf(fp, "%f;%f\n", var.first, var.second);
		i++;
	}
	fclose(fp);
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

std::vector<std::pair<double, double>> divide(std::vector<std::pair<double, double>> xy, std::vector<double> skala) { //skala częstotliwości i widmo amplitudowe
	std::vector<std::pair<double, double>> new_xy;
	int i = 0;
	for (auto var : xy) {
		new_xy.push_back(std::pair<double, double>(skala.at(i), var.second));
		i++;
		if (i > xy.size() / 2) {
			break;
		}
	}

	return new_xy;
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

std::vector<std::pair<double, double>> widmo_amplitudowe(std::vector<std::complex<double>> fourier, std::vector<std::pair<double, double>> xy) {
	std::vector<std::pair<double, double>> wynik;
	int i = 0;
	for (std::complex<double> var : fourier) {
		wynik.push_back(std::pair<double, double>(xy.at(i).first ,sqrt(pow(var.real(), 2) + pow(var.imag(), 2)) / fourier.size()*2.0));
		i++;
	}
	return wynik;
}

std::vector<double> skala_czestotliwosci(int czestotliwosc, int n) {
	std::vector<double> wynik;
	for (int i = 0; i < n; i++) {
		wynik.push_back((double)i*(czestotliwosc / (double)n));
	}
	return wynik;
}

std::vector<std::pair<double, double>> skala_decybelowa(std::vector<std::pair<double, double>> xy) {
	std::vector<std::pair<double, double>> wynik;
	int i = 0;
	for (auto var : xy) {
		//if(10 * log10(var.second) < )
		wynik.push_back(std::pair<double, double>(xy.at(i).first, 10 * log10(var.second)));
		i++;
	}
	return wynik;
}




//https://rosettacode.org/wiki/Fast_Fourier_transform#C.2B.2B
void fft(CArray& x)
{
	const size_t N = x.size();
	if (N <= 1) return;

	// divide
	CArray even = x[std::slice(0, N / 2, 2)];
	CArray  odd = x[std::slice(1, N / 2, 2)];

	// conquer
	fft(even);
	fft(odd);

	// combine
	for (size_t k = 0; k < N / 2; ++k)
	{
		Complex t = std::polar(1.0, -2 * PI * k / N) * odd[k];
		x[k] = even[k] + t;
		x[k + N / 2] = even[k] - t;
	}
}

std::vector<std::complex<double>> fft(std::vector<std::pair<double, double>> points)
{
	CArray y(points.size());
	for (auto i = 0; i < points.size(); i++)
		y[i] = points[i].second;
	fft(y);
	std::vector<std::complex<double>> results(y.size());
	for (auto i = 0; i < y.size(); i++)
		results[i] = y[i];
	return results;
}

void zadanie(double prog, double ka, double kp, int czestotliwosc_modulacji, int czestotliwosc_probkowania, std::vector<std::pair<double, double>> xy, std::string number) {
	auto xy_oryginalne = xy;
	std::vector<std::pair<double, double>> ma = modulacja(xy, ka, czestotliwosc_modulacji, modulacja_a);
	std::vector<std::complex<double>> fourier = fft(ma);
	std::vector<std::pair<double, double>> widmo = widmo_amplitudowe(fourier, xy);
	write_to_file("modulacja_amplitudowa_" + number + ".csv", ma);
	std::vector<double> skala = skala_czestotliwosci(czestotliwosc_probkowania, xy.size());
	xy = divide(widmo, skala);
	xy = filtr(xy, 25);
	std::vector<std::pair<double, double>> db = skala_decybelowa(xy);
	write_to_file("modulacja_amplitudowa_db_" + number + ".csv", db);
	xy = xy_oryginalne;
	std::vector<std::pair<double, double>> mf = modulacja(xy, kp, czestotliwosc_modulacji, modulacja_f);
	fourier = fft(mf);
	widmo = widmo_amplitudowe(fourier, xy);
	skala = skala_czestotliwosci(czestotliwosc_probkowania, xy.size());
	xy = divide(widmo, skala);
	xy = filtr(xy, 25);
	write_to_file("modulacja_fazowa_" + number + ".csv", mf);
	db = skala_decybelowa(xy);
	write_to_file("modulacja_fazowa_db_" + number + ".csv", db);
}


int main()
{
	double prog = 200;
	int czestotliwosc_probkowania = 4096;
	int czestotliwosc_funkcji_nosnej = 50;
	std::vector<double> x = xx(czestotliwosc_probkowania, 0.0, czestotliwosc_probkowania);
	std::vector<std::pair<double, double>> xy = probkowanie(x);
	write_to_file("probkowanie.csv", xy);
	

	//1 
	// f(min) = 50, f(max) = 50 W = 0 - amplitudowa
	// f(min) = 50, f(max) = 50 W = 0 - fazowa
	double ka = 0.75, kp = 0;
	zadanie(prog, ka, kp, czestotliwosc_funkcji_nosnej, czestotliwosc_probkowania, xy, "1");
	//2
	// f(min) = 46, f(max) = 54 W = 8 - amplitudowa
	// f(min) = 42, f(max) = 58 W = 16 - fazowa
	ka = 8, kp = 2.5;
	zadanie(prog, ka, kp, czestotliwosc_funkcji_nosnej, czestotliwosc_probkowania, xy, "2");
	//3
	// f(min) = 46, f(max) = 54 W = 8 - amplitudowa
	// brak - fazowa
	ka = 100, kp = 150;
	zadanie(prog, ka, kp, czestotliwosc_funkcji_nosnej, czestotliwosc_probkowania, xy, "3");


	
}
