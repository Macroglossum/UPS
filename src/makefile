BIN = graph.exe
OBJ = main.o  nodes_ht.o
CC = gcc
CCFLAGS = -Wall -Wextra -pedantic -ansi -lm

$(BIN): $(OBJ)
	gcc $(OBJ) -o $(BIN) $(CCFLAGS)

main.o: main.c
	$(CC) -c main.c $(CCFLAGS)

nodes_ht.o: nodes_ht.c nodes_ht.h
	$(CC) -c nodes_ht.c $(CCFLAGS)

clean:
	del *.o
	del *.exe 
