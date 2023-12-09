ifndef $(version)
	API_KEY = SAMPLE_KEY
endif

ifndef $(version)
	ENCRYPTION_KEY = uqwXShUE_rjDk3VAn6v3YUlTR7beGY86wXosq0VaHSo=
endif


run-local:
	uvicorn --reload src.main:app

run:
	docker compose up --build