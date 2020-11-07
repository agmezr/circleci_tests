# Circle CI

Test with Circle CI like docker, parallelism, etc


### Stuff learned

To cache image to speed up time of spin up

```yaml
version 2
jobs:
  build:
    docker:
      - image: circleci/python:3.6.2
    steps:
      - checkout
      - setup_remote_docker:
          docker_layer_caching: true
      - run: docker build . 
```