FROM python:3.10-slim

ENV SHIFT_GAMES='bl4 bl3 blps bl2 bl1' \
    SHIFT_PLATFORMS='epic steam' \
    SHIFT_REDEEM='bl4:steam ttw:epic bl3:epic bl2:epic,steam blps:epic,steam bl1:steam' \
    SHIFT_ARGS='--schedule' \
    TZ='America/Chicago'

COPY . /autoshift/
RUN pip install -r ./autoshift/requirements.txt && \
    mkdir -p ./autoshift/data
CMD if [ -n "${SHIFT_REDEEM}" ]; then \
        python ./autoshift/auto.py --user ${SHIFT_USER} --pass ${SHIFT_PASS} --redeem ${SHIFT_REDEEM} ${SHIFT_ARGS}; \
    else \
        python ./autoshift/auto.py --user ${SHIFT_USER} --pass ${SHIFT_PASS} --games ${SHIFT_GAMES} --platforms ${SHIFT_PLATFORMS} ${SHIFT_ARGS}; \
    fi