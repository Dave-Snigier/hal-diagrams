# Structurizr Themes Makefile

# Variables
THEMES_DIR := themes
THEMERIZR_DIR := structurizr-themerizr
GRAPHICS_DIR := ../graphics

# Default target
.PHONY: all
all: clean-icon icon clean-logo logo

# Build icon theme
.PHONY: icon
icon:
	@echo "Building icon themes..."
	@if [ -d "$(THEMERIZR_DIR)" ]; then \
		source $(THEMERIZR_DIR)/venv/bin/activate && \
		python $(THEMERIZR_DIR)/themerizr.py $(GRAPHICS_DIR)/custom/icon $(THEMES_DIR)/icon \
			--prefix icon \
			--height 450 \
			--width 450 \
			--name "HAL Icon Theme" \
			--description "Squarish, small icons for diagrams"; \
	else \
		echo "Error: structurizr-themerizr directory not found"; \
		exit 1; \
	fi

# Build logo theme
.PHONY: logo
logo:
	@echo "Building logo themes..."
	@if [ -d "$(THEMERIZR_DIR)" ]; then \
		source $(THEMERIZR_DIR)/venv/bin/activate && \
		python $(THEMERIZR_DIR)/themerizr.py $(GRAPHICS_DIR)/custom/logo $(THEMES_DIR)/logo \
			--prefix logo \
			--height 200 \
			--width 450 \
			--name "HAL Logo Theme" \
			--description "Logos, typically wordmarks for diagrams"; \
	else \
		echo "Error: structurizr-themerizr directory not found"; \
		exit 1; \
	fi

# Build RedHat Networking Icons theme
.PHONY: rh-network
rh-network:
	@echo "Building RedHat Networking Icons theme..."
	@if [ -d "$(THEMERIZR_DIR)" ]; then \
		source $(THEMERIZR_DIR)/venv/bin/activate && \
		python $(THEMERIZR_DIR)/themerizr.py $(GRAPHICS_DIR)/sets/rh-network $(THEMES_DIR)/rh-network \
			--prefix rh-network \
			--height 450 \
			--width 450 \
			--name "RH Network Icons" \
			--description "Selection of networking icons from RedHat Ansible"; \
	else \
		echo "Error: structurizr-themerizr directory not found"; \
		exit 1; \
	fi

.PHONY: clean-logo
clean-logo:
	@echo "Cleaning logo directory..."
	@if [ -d "$(THEMERIZR_DIR)" ]; then \
		source $(THEMERIZR_DIR)/venv/bin/activate && \
		rm $(THEMES_DIR)/logo/*; \
	else \
		echo "Error: structurizr-themerizr directory not found"; \
		exit 1; \
	fi

.PHONY: clean-icon
clean-icon:
	@echo "Cleaning icon directory..."
	@if [ -d "$(THEMERIZR_DIR)" ]; then \
		source $(THEMERIZR_DIR)/venv/bin/activate && \
		rm $(THEMES_DIR)/icon/*; \
	else \
		echo "Error: structurizr-themerizr directory not found"; \
		exit 1; \
	fi

.PHONY: clean-rh-network
clean-rh-network:
	@echo "Cleaning RedHat Networking Icons directory..."
	@if [ -d "$(THEMERIZR_DIR)" ]; then \
		source $(THEMERIZR_DIR)/venv/bin/activate && \
		rm $(THEMES_DIR)/rh-network/*; \
	else \
		echo "Error: structurizr-themerizr directory not found"; \
		exit 1; \
	fi

# Help target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  all           - Default target, builds both icon and logo themes"
	@echo "  icon          - Build icon theme with default settings"
	@echo "  logo          - Build logo theme with default settings"
	@echo "  clean-icon    - Remove all generated icon theme files"
	@echo "  clean-logo    - Remove all generated logo theme files"
	@echo "  help          - Show this help message"
