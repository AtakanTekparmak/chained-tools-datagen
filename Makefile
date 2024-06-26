# Set default target
.DEFAULT_GOAL := help

# Variables

## Python
PYTHON := python3
PIP := pip
VENV_NAME := venv

# .env file
ENV_FILE := .env

# data-genie-agents
DATA_GENIE_AGENTS_REPO_URL := https://github.com/interstellarninja/data-genie-agents
DATA_GENIE_AGENTS_REPO_DIR := data-genie-agents

# Help target
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  1. data_genie_setup  Clone the data-genie-agents repository and install its dependencies (should be run first)"
	@echo "  2. install           Install dependencies and set up the environment (should be run second)"
	@echo "  3. run               Run the main.py script (should be run third)"
	@echo "  4. clean             Remove the virtual environment and its contents"

# Clone the data-genie-agents repository
data_genie_setup: 
	rm -rf $(DATA_GENIE_AGENTS_REPO_DIR) && \
	git clone $(DATA_GENIE_AGENTS_REPO_URL) $(DATA_GENIE_AGENTS_REPO_DIR)

# Copy the .env.example file to .env only if it doesn't exist
copy_env:
	if [ ! -f $(ENV_FILE) ]; then cp .env.example $(ENV_FILE); fi

# Install dependencies and set up the environment
install: copy_env
	$(PYTHON) -m venv $(VENV_NAME)
	. $(VENV_NAME)/bin/activate && \
	$(PIP) install -r requirements.txt \
	$(PIP) install -r $(DATA_GENIE_AGENTS_REPO_DIR)/requirements.txt

# Run the main.py script
run: 
	. $(VENV_NAME)/bin/activate && \
	$(PYTHON) main.py

# Run the data-genie-agents/datagen.py
run_datagen:
	. $(VENV_NAME)/bin/activate && \
	$(PYTHON) $(DATA_GENIE_AGENTS_REPO_DIR)/datagen.py --generation_type function_calling --num_tasks 2 --agent_config chained_groq.json --local_embeddings True

# Clean the virtual environment
clean:
	rm -rf $(VENV_NAME)