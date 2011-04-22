#include "Round_1A_A.h"

int hapCal(int num, int base)
{
	int res = 0;
	while (num != 0)
	{
		res += (num % base) * (num % base);
		num = num / base;
	}
	return res;
}

bool checkHapp(int num, int base)
{
	bool res = true;
	vector<int> calcedNums;

	while (num != 1)
	{
		calcedNums.push_back(num);
		num = hapCal(num,base);
		
		for( int i = 0; i < calcedNums.size(); i++)
			if (num == calcedNums[i])
				return false;
	}

	return res;
}

void multiBase(ifstream& inFile, ofstream& outFile)
{
	int caseNum;
	inFile >> caseNum;
	string   line;  
	getline(inFile,line);

	for (int caseID = 1; caseID <= caseNum; caseID++)
	{
		vector<int> bases;
		bases.clear();
		
		//read all bases
		
		stringstream   ss;   
		getline(inFile,line);
		ss << line;
		int   m;  
        while   (   ss   >>   m   )  
		{  
              bases.push_back(m);
        }  
        ss.str()   =   "";  
        ss.clear(); 
		
		int posNum = 2;

		while (true)
		{
			bool happy = true;

			for (int i = 0; i < bases.size(); i++)
			{
				if(checkHapp(posNum, bases[i]) == false)
					happy = false;
			}			
			
			if (happy)
				break;
			posNum ++;
		}

		cout << "Case #" << caseID<< ": " << posNum << endl;
		outFile << "Case #" << caseID<< ": " << posNum << endl;
	}
}