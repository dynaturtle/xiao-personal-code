#include "Round_1A_C.h"

using namespace std;

int main()
{	
	char* inputFileName = "c.in";
	char* outputFileName = "c.out";

	ifstream inFile(inputFileName, ios::in);
	ofstream outFile(outputFileName, ios::out);

	CollectingCards(inFile, outFile);	
	return 0;
}