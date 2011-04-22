#include "AlienLanguage.h"

WordTable::WordTable(vector<string> wordList)
{	
	suffixTree = new SuffixTree('@');

	for (int i = 0; i < wordList.size(); i++)
		suffixTree->AddWord(wordList[i]);
}

bool WordTable::findSubStr(string word)
{
	bool res = false;

	res = suffixTree->ContainWord(word);

	return res;
}


Matcher::Matcher(WordTable* wordTable)
{
	_wordTable = wordTable;
}

int Matcher::getMatchNum(string pattern)
{
	int matchNum = 0;
	int index = 0;
	vector<string> wordsList;
	vector<string> newWordsList;

	wordsList.push_back("");

	while (index  < pattern.size())
	{
		newWordsList.clear();

		if (pattern[index] != '(')
		{
			for (int i = 0; i < wordsList.size(); i++)
				if (this->_wordTable->findSubStr(wordsList[i] + pattern[index]))
					newWordsList.push_back(wordsList[i] + pattern[index]);
		}
		else
		{
			index ++;
			while (pattern[index] != ')')
			{
				for (int i = 0; i < wordsList.size(); i++)
					if (this->_wordTable->findSubStr(wordsList[i] + pattern[index]))
						newWordsList.push_back(wordsList[i] + pattern[index]);
				index ++;
			}
		}

		wordsList = newWordsList;
		index ++;
	}
	
	matchNum = wordsList.size();
	return matchNum;
}


SuffixTree::SuffixTree(char ch)
{
	this->nodeChar = ch;
	this->subTrees.clear();
}

void SuffixTree::AddWord(string word)
{
	SuffixTree* curNode = this;

	for (int i = 0; i < word.size(); i++)
	{
		bool find = false;
		for (int j = 0; j < curNode->subTrees.size(); j++)
			if (curNode->subTrees[j]->nodeChar == word[i])
			{
				find = true;
				curNode  = this->subTrees[j];
				break;
			}

		if (find == false)
		{
			SuffixTree* newNode = new SuffixTree(word[i]);
			curNode->subTrees.push_back(newNode);
			curNode = newNode;
		}
	}	
}

bool SuffixTree::ContainWord(string word)
{
	if (word == "")
		return true;

	for (int i = 0; i < this->subTrees.size(); i++)
		if (word[0] == subTrees[i]->nodeChar)
			return subTrees[i]->ContainWord(word.substr(1));

	return false;
}

void AlienLanguage(ifstream& inFile, ofstream& outFile)
{
	int L,D,N;
	vector<string> wordsList;
	WordTable* wordTable;

	// read data
	inFile >> L >> D >> N;
	
	for (int i = 0; i < D; i++)
	{
		string word;
		inFile >> word;
		wordsList.push_back(word);
	}

	wordTable = new WordTable(wordsList);
	Matcher matcher(wordTable);

	// matching words
	for (int i = 0; i < N; i++)
	{
		string pattern;
		inFile >> pattern;
		int matchNum = 0;
		
		matchNum = matcher.getMatchNum(pattern);
		outFile << "Case #" << i + 1 << ": " << matchNum << endl;	
		cout <<"Case #" << i + 1 << ": " << matchNum << endl;	
	}
}