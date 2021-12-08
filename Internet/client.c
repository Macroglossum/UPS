#pragma comment(lib, "Ws2_32.lib");

#include "WinSock2.h"
#include "windows.h"
#include <iostream>

using namespace std;

SOCKADDR_IN addr;

SOCKET sConnect;

struct Buffer
{
	int ID;
	char Message[256];
};

int ClientThread()
{
	Buffer sbuffer;

	char buffer[sizeof(sbuffer)] = {0};

	for(;; Sleep(10))
	{	
		if(recv(sConnect, buffer, sizeof(sbuffer), NULL))
		{
			memcpy(&sbuffer, buffer, sizeof(sbuffer));
			cout << "<Client " << sbuffer.ID << ":> " << sbuffer.Message << endl;
		}
	}
	return 0;
}

int main()
{
	system("cls");

	int RetVal = 0;
	WSAData wsaData;
	WORD DLLVersion = MAKEWORD(2,1);
	RetVal = WSAStartup(DLLVersion, &wsaData);
	
	if(RetVal != 0)
	{
		MessageBoxA(NULL, "ERROR: Connection can´t be opened!", "ERROR", MB_OK | MB_ICONERROR);
		exit(1);
	}
	
	sConnect = socket(AF_INET, SOCK_STREAM, NULL);

	addr.sin_addr.s_addr = inet_addr("127.0.0.1");
	addr.sin_family = AF_INET;
	addr.sin_port = htons(1234);
	
	cout << "Connect to the server ? [ENTER]" << endl;
	getchar();
	RetVal = connect(sConnect, (SOCKADDR*)&addr, sizeof(addr));

	if(RetVal != 0)
	{
		MessageBoxA(NULL, "Server Connection ERROR!", "ERROR", MB_OK | MB_ICONERROR);
		main();
	}
	else
	{
		int ID;
		char* cID = new char[256];
		ZeroMemory(cID, 256);

		recv(sConnect, cID, 256, NULL);
		ID = atoi(cID);

		cout << "Successfuly Connected!" << endl;
		cout << "You are Client NO: " << ID << endl;

		CreateThread(NULL, NULL, (LPTHREAD_START_ROUTINE) ClientThread, NULL, NULL, NULL);

		for(;; Sleep(10))
		{
			char* buffer = new char[256];
			ZeroMemory(buffer, 256);
			cin >> buffer;
			getchar();

			send(sConnect, buffer, 256, NULL);
		}
	}
	return 0;
}
