TAG=stable-perl
TEST_NGINX=nginx-test
WEB_NGINX=nginx-web
IMAGE=nginx:${TAG}
podman pull ${IMAGE}
podman run --name ${TEST_NGINX} -p 80:80 -d ${IMAGE}
DOCKER_VOLUMES_DIR='/home/docker-volumes'
NGINX_DOCKER_VOLUMES_DIR=${DOCKER_VOLUMES_DIR}/${WEB_NGINX}
NGINX_OUTER_WWW_DIR="${NGINX_DOCKER_VOLUMES_DIR}/www"
NGINX_OUTER_LOGS_DIR=${NGINX_DOCKER_VOLUMES_DIR}/logs
NGINX_OUTER_CONF_DIR=${NGINX_DOCKER_VOLUMES_DIR}/conf
NGINX_OUTER_CONF_D_DIR=${NGINX_DOCKER_VOLUMES_DIR}/conf.d
NGINX_OUTER_CONF_FILE=${NGINX_OUTER_CONF_DIR}/nginx.conf

rm -rf ${NGINX_OUTER_CONF_DIR}
rm -rf ${NGINX_OUTER_WWW_DIR}
echo this is Dir ${NGINX_OUTER_WWW_DIR}
mkdir -p ${NGINX_OUTER_WWW_DIR}
mkdir -p ${NGINX_OUTER_LOGS_DIR}
mkdir -p ${NGINX_OUTER_CONF_DIR}
mkdir -p ${NGINX_OUTER_CONF_D_DIR}

podman cp ${TEST_NGINX}:/etc/nginx/nginx.conf ${NGINX_OUTER_CONF_DIR}
podman cp ${TEST_NGINX}:/etc/nginx/conf.d/default.conf ${NGINX_OUTER_CONF_D_DIR}/default.conf
podman rm -f ${TEST_NGINX}
podman rm -f ${WEB_NGINX}
podman run -d -p 80:80 -p 443:443 --name ${WEB_NGINX} -v ${NGINX_OUTER_WWW_DIR}:/usr/share/nginx/html -v ${NGINX_OUTER_CONF_FILE}:/etc/nginx/nginx.conf -v ${NGINX_OUTER_CONF_D_DIR}:/etc/nginx/conf.d -v ${NGINX_OUTER_LOGS_DIR}:/var/log/nginx ${IMAGE}
podman start ${WEB_NGINX}

INDEX_FILE=${NGINX_OUTER_WWW_DIR}/index.html
#cp nginx-index.html ${INDEX_FILE}
cp home_page/* ${NGINX_OUTER_WWW_DIR}
cp nginx/conf.d/* ${NGINX_OUTER_CONF_D_DIR}