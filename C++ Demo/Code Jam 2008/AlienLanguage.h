#include<fstream>
#include<string>
#include<vector>
#include<iostream>

using namespace std;

class SuffixTree
{
private:
	char nodeChar;	
	vector<SuffixTree*> subTrees;
public:
	SuffixTree(char ch);
	void AddWord(string word);
	bool ContainWord(string word);
};

class WordTable
{
private:
	SuffixTree* suffixTree;
public:
	WordTable(vector<string> wordList);	
	bool findSubStr(string word);
};

class Matcher
{
private:
	WordTable* _wordTable;
public:
	Matcher(WordTable* wordTable);
	int getMatchNum(string pattern);
};

void AlienLanguage(ifstream& inputFile, ofstream& outputFile);

vector<string> GenPossibleWords(string pattern);