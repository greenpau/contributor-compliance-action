.PHONY: info release linter test
PKG_NAME="contributor-compliance-action"
PKG_VERSION:=$(shell cat VERSION | head -1)
GIT_COMMIT:=$(shell git describe --dirty --always)
GIT_BRANCH:=$(shell git rev-parse --abbrev-ref HEAD -- | head -1)
LATEST_GIT_COMMIT:=$(shell git log --format="%H" -n 1 | head -1)
BUILD_USER:=$(shell whoami)
BUILD_DATE:=$(shell date +"%Y-%m-%d")
BUILD_DIR:=$(shell pwd)

all: info
	@echo "DEBUG: completed $@"

info:
	@echo "DEBUG: Version: $(PKG_VERSION), Branch: $(GIT_BRANCH), Revision: $(GIT_COMMIT)"
	@echo "DEBUG: Build on $(BUILD_DATE) by $(BUILD_USER)"

test: linter
	@echo "DEBUG: completed $@"

linter:
	@pylint inspect.py
	@echo "DEBUG: completed $@"

release:
	@echo "Making release"
	@if [ $(GIT_BRANCH) != "main" ]; then echo "cannot release to non-main branch $(GIT_BRANCH)" && false; fi
	@git diff-index --quiet HEAD -- || ( echo "git directory is dirty, commit changes first" && false )
	@versioned -patch
	@echo "Patched version"
	@git add VERSION
	@git commit -m "released v`cat VERSION | head -1`"
	@git tag -a v`cat VERSION | head -1` -m "v`cat VERSION | head -1`"
	@git push
	@git push --tags
	@@echo "If necessary, run the following commands:"
	@echo "  git push --delete origin v$(PKG_VERSION)"
	@echo "  git tag --delete v$(PKG_VERSION)"
	@echo "DEBUG: completed $@"
