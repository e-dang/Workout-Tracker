#!/bin/bash

echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

if [[ "${TRAVIS_BRANCH}" = "dev" ]]; then
    export TAG="latest-dev"
    export TARGET="dev"
else
    export TAG="latest-feature"
    export TARGET="dev"
fi

docker build -f Dockerfile -t $DOCKER_USER/$DOCKER_REPO:$TAG --target $TARGET .
docker push $DOCKER_USER/$DOCKER_REPO:$TAG