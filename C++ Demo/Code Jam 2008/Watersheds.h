#include<fstream>
#include<string>
#include<vector>

using namespace std;

class ElevationMap
{
private:
	int _width;
	int _height;
	int** _data;
	char* directMap;
	bool* visitMap;
	char* basinMap;
	void floodMap(int x, int y, char label);
public:
	ElevationMap(int* streamData, int width, int height);
	int getAltitude(int x, int y);
	char* getBasinMap();
};

void Watersheds(ifstream& inputFile, ofstream& outputFile);