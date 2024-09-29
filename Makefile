# Variables
APP_NAME=app.py
VENV_NAME=.venv

# Default target
.DEFAULT_GOAL := run

# Create virtual environment
venv:
	python -m venv $(VENV_NAME)

# Install dependencies
install: venv
	$(VENV_NAME)/bin/pip install -r requirements.txt
	$(VENV_NAME)/bin/pip install black flake8

# Remove venv
remove:
	rm -rf $(VENV_NAME)

# Run the Streamlit app
run:
	$(VENV_NAME)/bin/streamlit run $(APP_NAME)

# Format the code using black
format:
	$(VENV_NAME)/bin/black .

# Lint the code using flake8
lint:
	$(VENV_NAME)/bin/flake8 -v --exclude=$(VENV_NAME),__pycache__ .

# Clean up cache
clean:
	rm -rf __pycache__



# Help
help:
	@echo "Usage:"
	@echo "  make venv               Create a virtual environment"
	@echo "  make install            Install dependencies"
	@echo "  make run                Run the Streamlit app"
	@echo "  make format             Format code with black"
	@echo "  make lint               Lint code with flake8"
	@echo "  make clean              Clean up the python cache"
	@echo "  make help               Display this help message"

