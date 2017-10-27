all: main
	@erl -noshell -s main run_tests -s init stop


main: main.beam similarity_jw.beam

%.beam: %.erl
	@erlc $^ >/dev/null


clean:
	@rm -rf *.beam
