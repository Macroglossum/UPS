#pragma comment(lib, "Ws2_32.lib");

#include "WinSock2.h"
#include "windows.h"
#include <iostream>

using namespace std;

SOCKADDR_IN addr;

SOCKET sListen;
SOCKET sConnect;
SOCKET* Connections;

int addrlen = sizeof(addr);
int ConCounter = 1;

struct Buffer
{
	int ID;
	char Message[256];
};

int ServerThread(int ID)
{
	Buffer sbuffer;

	char* Recv = new char[256];
	ZeroMemory(Recv, sizeof(Recv));

	char* Send = new char[sizeof(Buffer)];
	ZeroMemory(Send, sizeof(Buffer));

	for(;; Sleep(10))
	{
		if(recv(Connections[ID], Recv, 256, NULL))
		{
			sbuffer.ID = ID;
			memcpy(sbuffer.Message, Recv, 256);
			memcpy(Send, &sbuffer, sizeof(Buffer));

			cout << "<Client " << sbuffer.ID << ":> " << sbuffer.Message << endl;
			for(int a = 0; a != ConCounter; a++)
			{
				if(Connections[a] == Connections[ID])
				{

				}
				else
				{
					send(Connections[a], Send, sizeof(Buffer), NULL);
				}
			}
			ZeroMemory(Recv, sizeof(Recv));
		}
	}
	return 0;
}

int InitWinSock()
{
	int RetVal;
	WSAData wsaData;
	WORD DLLVersion = MAKEWORD(2,1);
	RetVal = WSAStartup(DLLVersion, &wsaData);

	return RetVal;
}
int main()
{
	int RetVal = 0;
	RetVal = InitWinSock();

	if(RetVal != 0)
	{
		MessageBoxA(NULL, "WinSock Connection ERROR!", "ERROR", MB_OK | MB_ICONERROR);
		exit(1);
	}

	Connections = (SOCKET*)calloc(256, sizeof(SOCKET));

	sListen = socket(AF_INET, SOCK_STREAM, NULL);
	sConnect = socket(AF_INET, SOCK_STREAM, NULL);

	addr.sin_addr.s_addr = inet_addr("127.0.0.1");
	addr.sin_family = AF_INET;
	addr.sin_port = htons(1234);

	bind(sListen, (SOCKADDR*)&addr, sizeof(addr));
	listen(sListen, 256);

	cout << "Server Started Successfuly!" << endl;

	for(;; Sleep(50))
	{
		if(sConnect = accept(sListen, (SOCKADDR*)&addr, &addrlen)){
			Connections[ConCounter] = sConnect;
			cout << "New Client Connected!" << endl;

			char* ID = new char[256];
			ZeroMemory(ID, sizeof(ID));

			itoa(ConCounter, ID, 10);
			send(Connections[ConCounter], ID, sizeof(ID), NULL);

			ConCounter = ConCounter + 1;
			CreateThread(NULL, NULL, (LPTHREAD_START_ROUTINE) ServerThread, (LPVOID)(ConCounter -1), NULL, NULL);
		}
	}
	return 0;
}
