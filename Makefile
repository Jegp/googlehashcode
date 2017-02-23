.PHONY: run

NAME=googlehashcode

run:
	docker run -it --rm --name $(NAME) \
		-v `pwd`:/src \
		-w /src \
		python:3.5 \
		bash
