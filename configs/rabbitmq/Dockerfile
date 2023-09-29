FROM rabbitmq:3.11.7-management-alpine

ENV CONFIG_PATH configs/rabbitmq

ARG RABBITMQ_ADMIN_USER
ARG RABBITMQ_ADMIN_PASSWORD
ARG RABBITMQ_GUEST_USER
ARG RABBITMQ_GUEST_PASSWORD

COPY ${CONFIG_PATH}/conf/rabbitmq.conf ${CONFIG_PATH}/conf/definitions.json ${CONFIG_PATH}/scripts/init.sh /etc/rabbitmq/

# hashing passwords from env vars and replacing them in the config file
RUN chmod +x /etc/rabbitmq/init.sh && ./etc/rabbitmq/init.sh
