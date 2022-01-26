/*
    C socket server example, handles multiple clients using threads
    Compile
    gcc server.c -lpthread -o server
*/
 
#include<stdio.h>
#include<string.h>    //strlen
#include<stdlib.h>    //strlen
#include<netdb.h> 
#include<sys/socket.h>
#include<arpa/inet.h> //inet_addr
#include<unistd.h>    //write
#include<pthread.h> //for threading , link with lpthread
#include<time.h>
#define CLIENT_MSG_SIZE 100


//the thread function
void *connection_handler(void *);
void fill_deck(int deck[28][2]);
void shuffle_deck();
void first_card();
void players_first_cards(int player);
int add_to_board(token1, token2, player);

typedef struct {
    int game_id;
    struct dominoes *doms;
} game;

char card_to_send[CLIENT_MSG_SIZE];
char card_to_other1[CLIENT_MSG_SIZE];
char card_to_other2[CLIENT_MSG_SIZE];
int pruchod = 0;
int players_in_lobby = 0;
int game_id = 0;
game *every_game;
int client = 0;
int full_deck[28][2] = {{0, 0}, {0, 1}, {0, 2}, {0, 3}, {0, 4}, {0, 5}, {0, 6}, 
                      {1, 1}, {1, 2}, {1, 3}, {1, 4}, {1, 5}, {1, 6}, 
                      {2, 2}, {2, 3}, {2, 4}, {2, 5}, {2, 6}, 
                      {3, 3}, {3, 4}, {3, 5}, {3, 6}, 
                      {4, 4}, {4, 5}, {4, 6},
                      {5, 5}, {5, 6}, 
                      {6, 6}};
int cards_in_deck = 28;
int new_deck[28][2] = {{-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, 
                      {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1},
                      {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1},
                      {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1},
                      {-1, -1}, {-1, -1}, {-1, -1},
                      {-1, -1}, {-1, -1},
                      {-1, -1}};
int board_deck_left[28][2] = {{-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, 
                      {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1},
                      {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1},
                      {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1},
                      {-1, -1}, {-1, -1}, {-1, -1},
                      {-1, -1}, {-1, -1},
                      {-1, -1}};
int on_board_left = 1;
int on_board_right = 1;
int board_deck_right[28][2] = {{-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, 
                      {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1},
                      {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1},
                      {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1},
                      {-1, -1}, {-1, -1}, {-1, -1},
                      {-1, -1}, {-1, -1},
                      {-1, -1}};
int player1[12][2] = {{-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, 
                     {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}};
int player2[12][2] = {{-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, 
                     {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}, {-1, -1}};
int player1_hand = 0;
int player2_hand = 0;

int main(int argc , char *argv[])
{
    int socket_desc , client_sock , c;
    struct sockaddr_in server , client;
     
    //Create socket
    socket_desc = socket(AF_INET , SOCK_STREAM , 0);

    if (socket_desc == -1)
    {
        printf("Could not create socket");
    }
    puts("Socket created");
    
    //Prepare the sockaddr_in structure
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons( 10035 );
    
    //Reusing of port in case of server disconnect while clients are running
    //serverfault.com/questions/329845
    int flag = 1;
    if (-1 == setsockopt(socket_desc, SOL_SOCKET, SO_REUSEPORT, &flag, sizeof(flag)))
    {
        perror("setsockopt failed. Error");
    }
    
    //Bind
    if( bind(socket_desc,(struct sockaddr *)&server , sizeof(server)) < 0)
    {
        //print the error message
        perror("bind failed. Error");
        return 1;
    }
    puts("bind done");
    
    //Listen
    listen(socket_desc , 3);
     
    //Accept and incoming connection
    puts("Waiting for incoming connections...");
    c = sizeof(struct sockaddr_in);
	pthread_t thread_id;
	
    while( (client_sock = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c)) )
    {
        puts("Connection accepted");
        
        if( pthread_create( &thread_id , NULL ,  connection_handler , (void*) &client_sock) < 0)
        {
            perror("could not create thread");
            //return 1; (ukoncuje server, kdzy se pokazi klient)
        }
        //Now join the thread , so that we dont terminate before the thread
        //pthread_join( thread_id , NULL);
        puts("Handler assigned");
    }
     
    if (client_sock < 0)
    {
        perror("accept failed");
        return 1;
    }
     
    return 0;
}
 
/*
 * This will handle connection for each client
 * */
void *connection_handler(void *socket_desc)
{
    //Get the socket descriptor
    int sock = *(int*)socket_desc;
    int read_size;
    char *message , client_message[CLIENT_MSG_SIZE];
     
    //Send some messages to the client
    message = ";;connected;;";
    write(sock , message , strlen(message));
    
    char tok[50];

    //Receive a message from client
    while( (read_size = recv(sock, client_message, CLIENT_MSG_SIZE, 0)) > 0 ) {
        pruchod = 0;
        //end of string marker 
        client_message[read_size] = '\0';
        printf("%s\n", client_message);	
        if (strncmp(client_message, "play", 4) == 0) {
            printf("Player clicked on play\n");
            players_in_lobby++;
            client++;
            int round = 0;
            while (players_in_lobby == 1) {
                if (round == 0) {
                    write(sock , ";;lobby;;" , strlen(";;lobby;;"));
                    round++;
                    game_id++;
                }
            }
            write(sock , ";;game;;" , strlen(";;game;;"));
            players_in_lobby = 0;
            if (pruchod == 0) {
                shuffle_deck();
                write(sock, ";;yourturn;;", strlen(";;yourturn;;"));
                players_first_cards(0);
                write(sock, card_to_send, strlen(card_to_send));
                //printf("%s\n jednicka", client_message);
            }
            if (pruchod == 1) {
                write(sock, ";;waiting;;", strlen(";;waiting;;"));
                players_first_cards(1);
                write(sock, card_to_send, strlen(card_to_send));
            }
            first_card();
            write(sock, card_to_send, strlen(card_to_send));
            //printf("%d\n", pruchod);
        }	
        /**get position of players card and its destination */
        char *ret1 = strstr(client_message, ";;position_card:");
        if (ret1 && pruchod % 2 == 0) {
            char *token1 = strtok(client_message, ":");
            token1 = strtok(NULL, ";;");
            char *comp = "13"; 
            if (strcmp(token1, comp) != 0) {
                strcat(tok, token1);
            }
            else {
                add_to_board(token1, "", 1);
                printf(card_to_send);
                write(sock, card_to_send, strlen(card_to_send));
                strcat(card_to_other1, card_to_send);
                break;
            } 
        } 
        char *ret2 = strstr(client_message, ";;destination_card:");
        if (ret2 && pruchod % 2 == 0) { 
            char *token2 = strtok(client_message, ":");
            token2 = strtok(NULL, ";;");
            add_to_board(tok, token2, 0);
            printf(card_to_send);
            write(sock, card_to_send, strlen(card_to_send));
            strcat(card_to_other2, card_to_send);
            printf("%s", card_to_other2);
            break; 
        }
        if (strncmp(client_message, ";;done?;;", 10) == 0) {
            write(sock , card_to_other1, strlen(card_to_other1));
            write(sock , card_to_other2, strlen(card_to_other2));
            memset(card_to_other1, 0, CLIENT_MSG_SIZE);
            memset(card_to_other2, 0, CLIENT_MSG_SIZE);
            write(sock , ";;change;;", strlen(";;change;;"));
        }
	//clear the message buffer
    pruchod++;
	memset(client_message, 0, CLIENT_MSG_SIZE);
    }
     
    if(read_size == 0)
    {
        puts("Client disconnected");
        fflush(stdout);
    }
    else if(read_size == -1)
    {
        perror("recv failed");
    }
         
    return 0;
} 

//Dominoes game functions----------------------------------------------------------------------------------------
/* 
    Add card to board of possible or ask client for different choice
    return valid cards to display on board or error statement if addition is not possible 
    token1...postition of card in hand (0 - 11, 12 = deck)
    token2...destination of card (left ... -1, right ... -2)
*/
int add_to_board(char *token1, char *token2, int player) {
    int x, y;
    char temp[CLIENT_MSG_SIZE];
    memset(card_to_send, 0, CLIENT_MSG_SIZE);

    //char msg[CLIENT_MSG_SIZE];
    x = atoi(token1); //position of card in hand
    y = atoi(token2); //destination of card in hand
    //card from deck (not adding to board at all)
    if (x == 13) {
        if (cards_in_deck > 0) {
            int i = new_deck[28-cards_in_deck][0];
            int j = new_deck[28-cards_in_deck][1];
            for (int k = 0; k < 12; k++) {
                if (player1[k][0] == -1) { 
                    player1[j][0] = new_deck[28-cards_in_deck][0];
                    player1[j][1] = new_deck[28-cards_in_deck][1];
                    new_deck[28-cards_in_deck][0] = -1;
                    new_deck[28-cards_in_deck][1] = -1;
                    cards_in_deck--;
                    sprintf(temp, "%d", k);
                    break;
                }
            }
            char str1[CLIENT_MSG_SIZE], str2[CLIENT_MSG_SIZE];
            sprintf(str1, "%d", i);
            sprintf(str2, "%d", j);
            strcat(card_to_send, ";;addtohand:");
            strcat(card_to_send, str1);
            strcat(card_to_send, "_");
            strcat(card_to_send, str2);
            strcat(card_to_send, ">");
            strcat(card_to_send, temp); //position in hand
            strcat(card_to_send, ";;");
            printf(card_to_send);
        }
    }
    else {
        if (y == -1) { //left side
            char str1[CLIENT_MSG_SIZE], str2[CLIENT_MSG_SIZE];
            if (player1[x][0] == board_deck_left[on_board_left-1][0]) {
                player1[on_board_left][0] = player1[x][1];
                player1[on_board_left][1] = player1[x][0];
                sprintf(str2, "%d", player1[x][0]);
                sprintf(str1, "%d", player1[x][1]);  
            }
            else if(player1[x][1] == board_deck_left[on_board_left-1][0]) {
                player1[on_board_left][0] = player1[x][0];
                player1[on_board_left][1] = player1[x][1];
                sprintf(str1, "%d", player1[x][0]);
                sprintf(str2, "%d", player1[x][1]);  
            }
            else {
                return -1;
            }
            on_board_left++;
            player1_hand--;
            player1[x][0] = -1;
            player1[x][1] = -1;
            strcat(card_to_send, ";;addtoboard:");
            strcat(card_to_send, str1);
            strcat(card_to_send, "_");
            strcat(card_to_send, str2);
            strcat(card_to_send, ">");
            strcat(card_to_send, "-1"); //position on board
            strcat(card_to_send, "<");
            strcat(card_to_send, token1);
            strcat(card_to_send, ";;");
            printf(card_to_send);
        }
        if (y == -2) { //right side
            printf("%d\n", player1[x][0]);
            printf("%d\n", player1[x][1]);
            printf("%d\n", board_deck_left[on_board_left-1][0]);
            printf("%d_%d\n", board_deck_left[0][0], board_deck_left[0][1]);
            printf("count: %d\n", on_board_left);
            char str1[CLIENT_MSG_SIZE], str2[CLIENT_MSG_SIZE];
            if (player1[x][0] == board_deck_left[on_board_left-1][1]) {
                player1[on_board_right][0] = player1[x][0];
                player1[on_board_right][1] = player1[x][1];
                sprintf(str1, "%d", player1[x][0]);
                sprintf(str2, "%d", player1[x][1]);
            }
            else if(player1[x][1] == board_deck_left[on_board_left-1][1]) {
                player1[on_board_right][0] = player1[x][1];
                player1[on_board_right][1] = player1[x][0];
                sprintf(str2, "%d", player1[x][0]);
                sprintf(str1, "%d", player1[x][1]);    
            }
            else {
                return -1;
            }
            on_board_left++;
            player1_hand--;
            player1[x][0] = -1;
            player1[x][1] = -1;
            strcat(card_to_send, ";;addtoboard:");
            strcat(card_to_send, str1);
            strcat(card_to_send, "_");
            strcat(card_to_send, str2);
            strcat(card_to_send, ">");
            strcat(card_to_send, "-2"); //position on board
            strcat(card_to_send, "<");
            strcat(card_to_send, token1);
            strcat(card_to_send, ";;");
            printf(card_to_send);
        }

    }
    return 0;
}

/* shuffle deck and add first cards: one to table, 6 to each player */
void shuffle_deck() {
    srand(time(NULL));
    int number = rand() % (27);
    //printf("rand: %d\n", number);
    for (int i = 0; i < 28; i++) {
        while (full_deck[number][0] == -1) {
            number = rand() % (28);
            //printf("rand: %d\n", number);//04
        }
        new_deck[i][0] = full_deck[number][0];
        new_deck[i][1] = full_deck[number][1];
        full_deck[number][0] = -1;
        full_deck[number][1] = -1;
    }
    for (int i = 0; i < 28; i++) {
        //printf("%d_%d\n", new_deck[i][0], new_deck[i][1]);
    } //first card in game
    board_deck_left[0][0] = new_deck[0][0];
    board_deck_left[0][1] = new_deck[0][1];
    board_deck_right[0][0] = new_deck[0][0];
    board_deck_right[0][1] = new_deck[0][1];
    new_deck[0][0] = -1;
    new_deck[0][1] = -1;
    printf("\n\n%d_%d\n", board_deck_left[0][0], board_deck_left[0][1]);
    printf("%d_%d\n", board_deck_right[0][0], board_deck_right[0][1]);
    //player1 starting cards
    for(int i = 1, j = 0; i < 7; i++, j++) {
        player1[j][0] = new_deck[i][0];
        player1[j][1] = new_deck[i][1];
        new_deck[i][0] = -1;
        new_deck[i][1] = -1;
        //printf("%d_%d\n", player1[j][0], player1[j][1]);
    }
    //player2 starting cards
    for(int i = 7, j = 0; i < 13; i++, j++) {
        player2[j][0] = new_deck[i][0];
        player2[j][1] = new_deck[i][1];
        new_deck[i][0] = -1;
        new_deck[i][1] = -1;
        //printf("%d_%d\n", player2[j][0], player2[j][1]);
    } 
    //how many left in deck
    cards_in_deck -= 13;
}
void first_card() {
    char str1[CLIENT_MSG_SIZE], str2[CLIENT_MSG_SIZE];
    memset(card_to_send, 0, CLIENT_MSG_SIZE);

    strcat(card_to_send, ";;first_card:");
    sprintf(str1, "%d", board_deck_left[0][0]);
    sprintf(str2, "%d", board_deck_left[0][1]);
    strcat(card_to_send, str1);
    //strcat(card_to_send, "_");
    strcat(card_to_send, str2);
    strcat(card_to_send, ";;");
    printf(card_to_send);
}
void players_first_cards(int player) {
    char str1[CLIENT_MSG_SIZE], str2[CLIENT_MSG_SIZE];
    memset(card_to_send, 0, CLIENT_MSG_SIZE);

    for (int i = 0; i < 6; i++) {
        strcat(card_to_send, ";;card");
        sprintf(str1, "%d", i);
        strcat(card_to_send, str1);
        strcat(card_to_send, ":");
        if (player == 0) {
            sprintf(str1, "%d", player1[i][0]);
            sprintf(str2, "%d", player1[i][1]);
            player1_hand++;
        }
        else {
            sprintf(str1, "%d", player2[i][0]);
            sprintf(str2, "%d", player2[i][1]);
            player2_hand++;
        }
        strcat(card_to_send, str1);
        strcat(card_to_send, "_");
        strcat(card_to_send, str2);
        strcat(card_to_send, ";;");
    }
}
