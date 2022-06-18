.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: format
format:  ## 🔧 코드를 포매팅합니다.
	pycln .
	black .
	isort .

.PHONY: lint
lint:  ## 💯 코드를 린팅합니다.
	mypy .

.PHONY: test
test:  ## 🧪 테스트 코드를 실행합니다.
	pytest tests/
