#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>



// ;; vlakna co obsluhuje prichozi spojeni
void *prijem(void *arg){
	int client_sock_In = 0;
	char cbuf[256]; //null

	//pretypujem parametr z netypoveho ukazate na ukazatel na int
	client_sock_In = *(int *) arg; /* vytazeni klientske adresy, socketu */
	while(1){
		recv(client_sock_In, &cbuf, 256*sizeof(char), 0);
		cbuf[strlen(cbuf)] = '\0';
		printf("(Vlakno_In-%d:) Dostal jsem %s\n", client_sock_In, cbuf);
		
		bzero(cbuf, 256);
	}
	close(client_sock_In);

	// uvolnujeme pamet
	free(arg);
	return 0;
}


void *odesli(void *arg){
	int client_sock_Out = 0;
	char cbuf[256]; //null

	//pretypujem parametr z netypoveho ukazate na ukazatel na int
	client_sock_Out = *(int *) arg; /* vytazeni klientske adresy, socketu */
	while(1){
		fgets(cbuf,256, stdin); // nactu ze standartniho vstupu(konzole)
		cbuf[strlen(cbuf)] = '\0';
		send(client_sock_Out, &cbuf, strlen(cbuf), 0);
		printf("(Vlakno_Out-%d:) Odeslal jsem %s\n", client_sock_Out, cbuf);

		bzero(cbuf, 256);
	}
	// uvolnujeme pamet
	free(arg);
	return 0;
}


int main (void){

	int server_socket;
	int client_socket;
	int return_value;
	char cbuf[256];
	int len_addr;
	struct sockaddr_in my_addr, peer_addr;

	int *th_socket_In;
	int *th_socket_Out;
	pthread_t thread_id_In; /* kladaji se identifikatory vlakna */
	pthread_t thread_id_Out;

	server_socket = socket(AF_INET, SOCK_STREAM, 0);

	memset(&my_addr, 0, sizeof(struct sockaddr_in)); // nulovani pameti

	my_addr.sin_family = AF_INET;
	my_addr.sin_port = htons(10000);
	my_addr.sin_addr.s_addr = INADDR_ANY;

	return_value = bind(server_socket, (struct sockaddr *) &my_addr, \
			sizeof(struct sockaddr_in));

	if (return_value == 0) 
		printf("Bind - OK\n");
	else {
		printf("Bind - ERR\n");
		return -1;
	}

	return_value = listen(server_socket, 5);

	if (return_value == 0) 
		printf("Listen - OK\n");
	else {
		printf("Listen - ERR\n");
		return -1;
	}

	for (;;){
		client_socket = accept(server_socket, (struct sockaddr *) &peer_addr, &len_addr);
		if (client_socket>0) {
			printf("Hura nove spojeni\n");


			th_socket_In= (int *) malloc(sizeof(int));	// vyhrazuju si pamet na clientsky socket
			*th_socket_In=client_socket;
			th_socket_Out=(int *) malloc(sizeof(int));	
			*th_socket_Out=client_socket;

			pthread_create(&thread_id_In, NULL, (void *)&prijem, (void *)th_socket_In); /* vytvoreni vlakna a prevod na netypove ukazatele */
			pthread_create(&thread_id_Out, NULL,(void *)&odesli, (void *)th_socket_Out); /* vytvoreni vlakna a prevod na netypove ukazatele */


		}
		else {
			printf ("Brutal Fatal ERROR\n");
			return -1;
		}
	}

	return 0;
}










