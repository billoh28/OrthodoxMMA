PKG := "."
# PKG_LIST := $(shell go list ${PKG}/... | grep -v /vendor/)
##GO_FILES := $(shell find . -name '*.go' | grep -v /vendor/ | grep -v _test.go)

.PHONY: test help

# all: build

# lint: ## Lint the files
# 	@golint -set_exit_status ${PKG_LIST}

build_py:
	pip3 install --upgrade pip
	apt-get update
	apt-get install -y libgl1-mesa-dev


testApp:
	@echo ''
	cd src/Flask_App && pytest
	@echo ''

testAdHoc:
	@echo ''
	cd src/Pose_Estimation/test && pytest
	@echo ''

installs:
	pip3 install opencv-python-headless
	pip3 install -r requirements.txt
	pip3 install pytest
	pip3 install joblib
	pip3 install matplotlib
	pip3 install numpy
	pip3 install scikit-learn
	pip3 install mediapipe

# msan: dep ## Run memory sanitizer
# 	@go test -msan -short ${PKG_LIST}

# build: ## Build the binary file
# 	@echo 'Getting dependencies'
# 	@go build -i -v ./...

# clean: ## Remove previous build
# 	@rm -f $(PROJECT_NAME)

# dep: ## Get the dependencies
# 	@go get -v -d ./...

help:
	@echo 'Usage: make <OPTION>'
	@echo ''
	@echo 'Available targets are:'
	@echo ''
	@echo 'help 					Show this help screen.'
	@echo 'lint 					Run golint.'
	@echo 'test 					Run unit tests.'
	@echo 'msan 					Memory sanitizer'
	@echo 'build					Build project for current platform'
	@echo 'clean					Removes previous builds'
	@echo ''
