#include "pch.h"
#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <time.h>
using namespace ::std;
int** G; //матрица смежности
int** Chr; //массив хромосом
int** Chr_buff; //копия массива хромосом
//Целевая функция
int Objective_function(int chr[], int n)
{
	int f = 0;
	for (int i = 0; i < n; i++)
	{
		if (chr[i] == 0)
			for (int j = 0; j < n; j++)
			{
				if (chr[j] == 1) f += G[i][j];
			}
	}
	return f;
}
//Оператор репродукции
void OR(int n)
{
	int i_best = 0;
	int i_worst = 0;
	for (int i = 0; i < 4; i++)
	{
		if (Objective_function(Chr[i], n) < Objective_function(Chr[i_best], n)) i_best = i;
		else if (Objective_function(Chr[i], n) > Objective_function(Chr[i_worst], n)) i_worst = i;
	}
	int i1 = 2;
	for (int i = 0; i < 4; i++)
	{
		if (i != i_worst)
		{
			if (i == i_best)
				for (int j = 0; j < n; j++)
				{
					Chr[0][j] = Chr_buff[i][j];
					Chr[1][j] = Chr_buff[i][j];
				}
			else
			{
				for (int j = 0; j < n; j++)
				{
					Chr[i1][j] = Chr_buff[i][j];
				}
				i1++;
			}
		}
	}
}
//Оператор мутации
void OM(int n, int n1, int n2)
{
	for (int i = 1; i < 4; i++)
	{
		int* l1 = new int[n1];
		int* l2 = new int[n2];
		int j1 = 0;
		int j2 = 0;
		for (int j = 0; j < n; j++)
		{
			if (Chr[i][j] == 1)
			{
				l1[j1] = j;
				j1++;
			}
			else if (Chr[i][j] == 0)
			{
				l2[j2] = j;
				j2++;
			}
		}
		Chr[i][l1[rand() % n1]] = 0;
		Chr[i][l2[rand() % n2]] = 1;
		delete[] l1;
		delete[] l2;
	}
}
int main()
{
	srand(time(NULL));
	setlocale(LC_ALL, "Russian");
	string name = "file.txt";
	ifstream file;
	int n = 0; //число вершин
	int n1 = 0;
	int n2 = 0;
	int m; //число частей
	//Подсчёт числа вершин
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
	//Запись матрицы смежности из файла в массив
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
	//Ввод данных
	cout << "На сколько частей требуется разрезать граф: ";
	cin >> m;
	int* n_m = new int[m];// массив числа вершин в частях
	for (int i = 0; i < m; i++)
	{
		cout << "Введите число вершин в части " << i << ": ";
		cin >> n_m[i];
	}
	//Создание масиива хромосом
	Chr = new int*[4];
	Chr_buff = new int*[4];
	for (int i = 0; i < 4; i++)
	{
		Chr[i] = new int[n];
		Chr_buff[i] = new int[n];
		for (int j = 0; j < n; j++)
		{
			Chr[i][j] = 0;
		}
	}
	//Основной процесс
	int m1 = 1; //число частей, на которые разрезан граф в данный момент
	int* Chr_best = new int[n]; // лучшая хромосома
	while (m1 < m)
	{
		int k = 0;
		//Формирование начальной популяции
		n1 = n_m[m1 - 1];
		n2 = 0;
		for (int i = m1; i < m; i++)
		{
			n2 += n_m[i];
		}
		for (int i = 0; i < 4; i++)
		{
			int ran = 0;
			for (int j = 0; j < n1; j++)
			{
				while (Chr[i][ran] != 0)
				{
					ran = rand() % n;
				}
				Chr[i][ran] = 1;
			}
		}
		//Разрезание текущей части на 2 части
		while (k < n*2)
		{
			for (int i = 0; i < 4; i++)
			{
				for (int j = 0; j < n; j++)
				{
					Chr_buff[i][j] = Chr[i][j];
				}
			}
			OR(n);
			OM(n, n1, n2);
			for (int j = 0; j < n; j++)
			{
				if (Chr_best[j] != Chr[0][j]) k = 0;
				Chr_best[j] = Chr[0][j];
			}
			k++;
		}
		m1++;
		for (int i = 0; i < 4; i++)
		{
			for (int j = 0; j < n; j++)
			{
				Chr[i][j] = Chr_best[j];
				if (Chr[i][j] == 1) Chr[i][j] = m1;
			}
		}
	}
	//Вывод решения
	for (int i = 0; i < m; i++)
	{
		cout << "Вершины в части " << i << ": ";
		for (int j = 0; j < n; j++)
		{
			if (Chr_best[j] == i) cout << j << '\t';
		}
		cout << endl;
	}
	//Удаление массивов
	for (int i = 0; i < n; i++)
	{
		delete[] G[i];
	}
	delete[] G;
	for (int i = 0; i < 4; i++)
	{
		delete[] Chr[i];
	}
	delete[] Chr;
	for (int i = 0; i < 4; i++)
	{
		delete[] Chr_buff[i];
	}
	delete[] Chr_buff;
	delete[] Chr_best;
	delete[] n_m;
	system("pause");
	return 0;
}
