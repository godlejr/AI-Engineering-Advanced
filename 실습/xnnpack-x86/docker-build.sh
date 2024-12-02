#/bin/sh

'''docker buildx build . -t executorch:xnnpack \
        -o type=docker '''


docker  build -t djkim:xnnpack .\
