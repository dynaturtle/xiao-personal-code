#include "Round_1A_C.h"

double posAtM(int m, int c)
{
	double res = 0;
	res += 1.0 / c;
	
	double rate =(c - 2.0) / (c - 1.0);
	double delta = 1;

	for (int i = 0; i < m; i++)
		delta *= rate;

	res += delta * (c - 1.0) / c;

	return res;
}
double posWhole(int wholeNum, int setNum)
{
	double res = 0;
	double lastPos = 0;
	double previousPos = 0;
	int times = wholeNum / setNum;
	if (wholeNum % setNum != 0)
		times ++;
	
	while (true)
	{		
		double thisPos;
		thisPos = 0;
		int minCardNum = (times - 1) * setNum + 1 > wholeNum ? (times - 1) * setNum + 1: wholeNum;
		int maxCardNum = times * setNum;

		for (int i = minCardNum; i <= maxCardNum; i++)
		{			
			double curPos;
			curPos = posAtM(i,wholeNum);
			thisPos += (1 - previousPos) * curPos;
			previousPos += thisPos;
		}

		if (abs(thisPos) < 1e-7)
			break;		
		res += times * thisPos;	

		times ++;
	}

	return res;
}

void CollectingCards(ifstream& inFile, ofstream& outFile)
{
	int caseNum;
	inFile >> caseNum;

	for (int caseID = 1; caseID <= caseNum; caseID++)
	{
		double p;
		int N,C;
		inFile >> C >> N;

		//calc possibility
		p = posWhole(C,N);
		outFile << "Case #" << caseID<< ": " << p<< endl;
	}
}