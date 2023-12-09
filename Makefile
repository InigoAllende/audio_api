ifndef $(version)
	version = development
endif

ifndef $(API_KEY)
	API_KEY = SAMPLE_KEY
endif

ifndef $(ENCRYPTION_KEY)
	ENCRYPTION_KEY = uqwXShUE_rjDk3VAn6v3YUlTR7beGY86wXosq0VaHSo=
endif

build:
	docker build -t audio_api:${version} .
 
run-local:
	uvicorn --reload src.main:app

run:
	docker compose up --build

.PHONY: tests
tests: 
	pytest tests