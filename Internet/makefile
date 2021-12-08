CC=gcc

all:	clean client server

client:	client.cpp
	${CC} -o client client.cpp

server: server.cpp
	${CC} -o server server.cpp

clean: 
	rm -f client
	rm -f server
