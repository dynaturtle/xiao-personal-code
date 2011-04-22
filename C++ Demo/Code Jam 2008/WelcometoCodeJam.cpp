#include "WelcometoCodeJam.h"
string toString(int num)
{
	string res = "";
	
	while (num != 0)
	{
		res = (char)(num % 10 + '0') + res;
		num = num / 10;
	}

	while (res.size() != 4)
	{
		res = '0' + res;
	}
	return res;
}

void WelcometoCodeJam(ifstream& inFile, ofstream& outFile)
{
	int caseNum;
	inFile >> caseNum;
	string tempS;
	getline(inFile, tempS);	

	for (int caseID = 1; caseID <= caseNum; caseID ++)
	{
		string paragraph;
		string codeJam = "welcome to code jam";
		int** computeTable;
			
		getline(inFile, paragraph);	
		computeTable = new int*[paragraph.size() + 1];
		for (int i = 0; i <= paragraph.size(); i++)
		{
			computeTable[i] = new int[codeJam.size() + 1];
			for (int j = 0; j < codeJam.size(); j++)
				computeTable[i][j] = 0;
			computeTable[i] [codeJam.size()] = 1;
		}

		// compute nums
		for (int i = paragraph.size() - 1; i >= 0; i --)
			for (int j = codeJam.size() - 1; j >=max((int)0,(int)(i - paragraph.size() + codeJam.size())) ; j --)
				for (int k = i; k < min(paragraph.size() - codeJam.size() + j, paragraph.size()); k++)
				{
					if (paragraph[k] ==  codeJam[j])
						computeTable[i][j] += computeTable[k+1][ j+1] % 10000;
				}

		outFile << "Case #" << caseID <<": " << toString(computeTable[0][0]) << endl;
	}
}