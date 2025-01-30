. `dirname $0`/env.sh

wget "${LWS_SOURCE_URL}" -O libwebsockets.tar.gz
wget "${LIBUNWIND_SOURCE_URL}" -O libunwind.tar.gz
tar -zxf libwebsockets.tar.gz --one-top-level="${LWS_DIR}"       --strip-components 1
tar -zxf libunwind.tar.gz     --one-top-level="${LIBUNWIND_DIR}" --strip-components 1

wget "${PROTON_SOURCE_URL}" -O qpid-proton.tar.gz
wget "${ROUTER_SOURCE_URL}" -O skupper-router.tar.gz

sudo apt -y install gcc make cmake \
    libsasl2-dev libssl-dev uuid-dev \
    python3-dev python3-pip python3-wheel \
    libnghttp2-dev \
    wget tar patch findutils git \
    libtool;
