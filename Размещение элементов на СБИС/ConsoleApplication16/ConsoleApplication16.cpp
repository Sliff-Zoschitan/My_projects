#include <iostream>
#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <time.h>
using namespace ::std;
int** G;
float ffmin;
float kmin;
float Objective_function(int** P, int np, int mp, int r)
{
	float f = 0;
	int k = 0;
	for (int x1 = 0; x1 < np; x1++)
	{
		for (int y1 = 0; y1 < mp; y1++)
		{
			if (P[x1][y1] > -1)
				for (int x2 = 0; x2 < np; x2++)
				{
					for (int y2 = 0; y2 < mp; y2++)
					{
						if (G[P[x1][y1]][P[x2][y2]] > 0)
						{
							f += pow(abs(x1 - x2)*abs(x1 - x2)*r*r + abs(y1 - y2)*abs(y1 - y2)*r*r, 0.5);
							for (int x3 = 0; x3 < np; x3++)
							{
								for (int y3 = 0; y3 < mp; y3++)
								{
									if (P[x3][y3] > -1)
										for (int x4 = 0; x4 < np; x4++)
										{
											for (int y4 = 0; y4 < mp; y4++)
											{
												if (G[P[x3][y3]][P[x4][y4]] > 0)
												{
													float v1 = (x4 - x3)*(y1 - y3) - (y4 - y3)*(x1 - x3);
													float v2 = (x4 - x3)*(y2 - y3) - (y4 - y3)*(x2 - x3);
													float v3 = (x2 - x1)*(y3 - y1) - (y2 - y1)*(x3 - x1);
													float v4 = (x2 - x1)*(y4 - y1) - (y2 - y1)*(x4 - x1);
													if ((v1*v2 < 0) && (v3*v4 < 0)) k++;
												}
												
											}
										}
								}
							}
						}
					}
				}
		}
	}
	k /=4;
	f /= 2;
	kmin = k;
	ffmin = f;
	f*=k;
	return f;
}
void readFile(string name)
{
	ifstream file;
	file.open(name);
	if (file.is_open())
	{
		int i = 0;
		int j = 0;
		char ch;
		string weight_str;
		while (file.get(ch))
		{
			if (ch != ' ' && ch != '\n')
			{
				weight_str += ch;
			}
			else
			{
				G[i][j] = stoi(weight_str);
				weight_str = "";
				if (ch == ' ') j++;
				if (ch == '\n')
				{
					j = 0;
					i++;
				}
			}
		}
		G[i][j] = stoi(weight_str);
		file.close();
	}
}
void input(int* np, int* mp, int* r)
{
	cout << "Колличество посадочных мест по вертикали = ";
	cin >> *np;
	cout << "Колличество посадочных мест по горизонтали = ";
	cin >> *mp;
	cout << "Расстояние между соседними элементами = ";
	cin >> *r;
}
void output(int** Pmin, int np, int mp, int r)
{
	for (int i = 0; i < np; i++)
	{
		for (int j = 0; j < mp; j++)
		{
			cout << Pmin[i][j] << '\t';
		}
		cout << endl;
	}
	Objective_function(Pmin, np, mp, r);
	cout << "сумма расстояний между элементами = " << ffmin << endl;
	cout << "число пересечений соединений = " << kmin << endl;
}

int main()
{
	srand(time(NULL));
	setlocale(LC_ALL, "Russian");
	string name = "file.txt";
	ifstream file;
	int n = 0;
	file.open(name);
	if (file.is_open())
	{
		char ch;
		while (file.get(ch))
		{
			if (ch == '\n') n++;
		}
		n++;
		file.close();
	}
	G = new int*[n];
	for (int i = 0; i < n; i++)
	{
		G[i] = new int[n];
	}
	readFile(name);
	int np = 0;
	int mp = 0;
	int r = 2;
	input(&np, &mp, &r);
	int** P = new int*[n];
	for (int i = 0; i < n; i++)
	{
		P[i] = new int[n];
	}
	for (int i = 0; i < n; i++)
	{
		for (int j = 0; j < n; j++)
		{
			P[i][j] = -1;
		}
	}

	int** Pmin = new int*[n];
	for (int i = 0; i < n; i++)
	{
		Pmin[i] = new int[n];
	}
	for (int i = 0; i < n; i++)
	{
		for (int j = 0; j < n; j++)
		{
			Pmin[i][j] = -1;
		}
	}

	int nit = 100*np*mp;
	for (int it = 0; it < nit; it++)
	{
		for (int i = 0; i < n; i++)
		{
			int i1 = rand() % np;
			int j1 = rand() % mp;
			while (P[i1][j1] > -1)
			{
				i1 = rand() % np;
				j1 = rand() % mp;
			}
			P[i1][j1] = i;
		}
		
		if (it == 0)
			for (int i1 = 0; i1 < np; i1++)
			{
				for (int j1 = 0; j1 < mp; j1++)
				{
					Pmin[i1][j1] = P[i1][j1];
				}
			}
		if (Objective_function(Pmin, np, mp, r) > Objective_function(P, np, mp, r) && it > 0)
			for (int i1 = 0; i1 < np; i1++)
			{
				for (int j1 = 0; j1 < mp; j1++)
				{
					Pmin[i1][j1] = P[i1][j1];
				}
			}
		for (int i = 0; i < n; i++)
		{
			for (int j = 0; j < n; j++)
			{
				P[i][j] = -1;
			}
		}
	}

	output(Pmin, np, mp, r);
	system("pause");
}

