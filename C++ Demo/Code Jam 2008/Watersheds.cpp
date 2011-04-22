#include "Watersheds.h"

ElevationMap::ElevationMap(int* streamData,int width, int height)
{
	this->_height = height;
	this->_width = width;
	this->_data = new int*[height];
	for (int i = 0; i < height; i++)
	{
		this->_data[i] = new int[width];
		for (int j = 0; j < width; j++)
			this->_data[i][j] = streamData[i * width + j];
	}
}

int ElevationMap::getAltitude(int i, int j)
{
	if ((i < 0) || (j < 0) || (j >= _width) || (i >= _height))
		return 100000;	
	return this->_data[i][j];
}

void ElevationMap::floodMap(int y, int x, char label)
{
	int pos = y * this->_width + x;
	visitMap[pos] = true;
	this->basinMap[pos] = label;

	//check left
	if (x - 1 >= 0)
	{
		int index = y * this->_width + x - 1;
		if ((!visitMap[index]) && ((directMap[index] == 'r') || (directMap[pos] == 'l')))
			floodMap(y, x - 1, label);
	}

	// check right
	if ( x+1 < this->_width)
	{
		int index = y * this->_width + x + 1;
		if ((!visitMap[index]) && ((directMap[index] == 'l') || (directMap[pos] == 'r')))
			floodMap(y, x + 1, label);
	}

	// check top
	if ( y - 1 >= 0)
	{
		int index = (y - 1)* this->_width + x;
		if ((!visitMap[index]) && ((directMap[index] == 'b') || (directMap[pos] == 't')))
			floodMap(y - 1, x, label);
	}

	// check bottom
	if ( y + 1 < this->_height)
	{
		int index = (y + 1)* this->_width + x;
		if ((!visitMap[index]) && ((directMap[index] == 't') || (directMap[pos] == 'b')))
			floodMap(y + 1, x, label);
	}
}

char* ElevationMap::getBasinMap()
{	
	basinMap = new char[this->_height * this->_width];
	directMap = new char[this->_height * this->_width];
	visitMap = new bool[this->_height * this->_width];

	// calc direction map
	for (int i = 0; i < this->_height; i++)
		for (int j = 0; j < this->_width; j++)
		{
			// pos direct: s(sink), l(left), r(right), t(top), b(bottom)
			char direct = 's';
			int max = 0;
			int center = this->getAltitude(i,j);
			int left = this->getAltitude(i, j - 1);
			int right = this->getAltitude(i, j + 1);
			int top = this->getAltitude(i - 1, j);
			int bottom = this->getAltitude(i + 1,j);

			if ((center - top) > max)
			{
				direct = 't';
				max = center - top;
			}
			if ((center - left) > max)
			{
				direct = 'l';
				max = center - left;
			}
			if ((center - right) > max)
			{
				direct = 'r';
				max = center - right;
			}
			if ((center -bottom) > max)
			{
				direct = 'b';
				max = center - bottom;
			}

			directMap[i * this->_width + j] = direct;
		}/*end of calc direct map*/

	// calc of basin map
	for (int i = 0; i < this->_height * this->_width; i++)
	{
		visitMap[i] = false;
	}

	char label = 'a';
	for (int i = 0; i < this->_height; i++)
		for (int j = 0; j < this->_width; j++)
		{
			if (visitMap[i * this->_width + j])
				continue;
			floodMap(i,j,label);
			label ++;
		}

	delete[] directMap;
	delete[] visitMap;
	return basinMap;
}

void Watersheds(ifstream& inFile, ofstream& outFile)
{
	int caseNum;
	int height, width;
	int* streamData = 0;

	inFile >> caseNum;
	
	for (int caseID = 0; caseID < caseNum; caseID ++)
	{
		inFile >> height >> width;		
		streamData = new int[height * width];
		for (int i = 0; i < height * width; i++)
			inFile >> streamData[i];
		ElevationMap* elevationMap;
		elevationMap = new ElevationMap(streamData,width,height);
		char* res = elevationMap->getBasinMap();
		outFile << "Case #" << caseID + 1 << ":" << endl;
		for (int i = 0; i < height; i ++)
		{
			outFile << res[i * width];
			for (int j = 1; j < width; j++)
				outFile << " " << res[i * width + j];
			outFile << endl;
		}
	}	
}