.PHONY: build-image push-image helm kustomize native

SERVER  =
COMMIT  =${shell git rev-parse --short HEAD}
VERSION ?=${COMMIT}
TYPE    ?=minikube
REPO_NAME=imilabremodeling/ilatc


build-image:
	docker build --tag ${REPO_NAME}:${VERSION} .
	docker image tag ${REPO_NAME}:${VERSION} ${REPO_NAME}:latest    

push-image: build-image
	docker push ${REPO_NAME}:${VERSION}
	docker push ${REPO_NAME}:latest
docker-lint:
	@echo "---------docker lint----------"
	docker run --rm -i hadolint/hadolint < Dockerfile;

shellcheck:
	@echo "---------shell check----------"
	shellcheck run.sh

test: shellcheck docker-lint

native:
	@echo "---------kubectl yaml check -----------"
	kubectl --dry-run=server apply -f yamls/

helm:
	@echo "---------helm yaml check -----------"
	helm install --dry-run --debug test predict_n1_chart
kustomize:
	@echo "---------kustomize yaml check -----------"
	@echo "--------- base -----------"
	kubectl --dry-run=server apply -k kustomize/base/
	@echo "--------- production -----------"
	kubectl --dry-run=server apply -k kustomize/overlays/production/
	@echo "--------- staging -----------"
	kubectl --dry-run=server apply -k kustomize/overlays/staging/

k8s-yaml: native helm kustomize

bats:
	@echo "---------bats check-----------"
	sudo TYPE=${TYPE} bats -t tests/test.bats

k8s-test: k8s-yaml bats
                     
