ASM      = nasm
CC       = gcc
ASMFLAGS = -f elf64 -g
LDFLAGS  = -no-pie
TARGET   = average
OBJ      = average.o

all: $(TARGET)

$(OBJ): main.asm
	$(ASM) $(ASMFLAGS) -o $@ $<

$(TARGET): $(OBJ)
	$(CC) $(LDFLAGS) -o $@ $^

run: $(TARGET)
	./$(TARGET) data.txt

.PHONY: all run