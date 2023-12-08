ifndef $(version)
	version = development
endif

ifndef $(version)
	API_KEY = SAMPLE_KEY
endif


run-local:
	uvicorn --reload src.main:app

build:
	docker build -t audio_api:$(version) .

run: build
	docker compose up