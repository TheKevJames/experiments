CC_FLAGS=-O2


all: main
	@./runner.sh


main: main.c jaro.o
	@${CC} $(CC_FLAGS) $^ -o $@

jaro.o: jaro.c jaro.h
	@${CC} $(CC_FLAGS) -c $<


clean:
	@rm -rf main
	@rm -rf *.o
