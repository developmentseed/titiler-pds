FROM public.ecr.aws/lambda/python:3.9

COPY setup.py ${LAMBDA_TASK_ROOT}
COPY titiler_pds/ ${LAMBDA_TASK_ROOT}/titiler_pds/

# Install dependencies
RUN pip3 install titiler_pds/rio_tiler_pds-0.7.0-py3-none-any.whl -t ${LAMBDA_TASK_ROOT} && \
    pip3 install . rasterio==1.3a2 -t ${LAMBDA_TASK_ROOT} && \
    \
    echo "Leave module precompiles for faster Lambda startup" && \
    cd ${LAMBDA_TASK_ROOT} && find . -type f -name '*.pyc' | \
    while read f; do n=$(echo $f | sed 's/__pycache__\///' | sed 's/.cpython-[2-3][0-9]//'); cp $f $n; done && \
    \
    cd ${LAMBDA_TASK_ROOT} && find . -type d -a -name '__pycache__' -print0 | xargs -0 rm -rf && \
    cd ${LAMBDA_TASK_ROOT} && find . -type f -a -name '*.py' -print0 | grep -v handler.py | xargs -0 rm -f && \
    cd ${LAMBDA_TASK_ROOT} && find . -type d -a -name 'tests' -print0 | xargs -0 rm -rf && \
    rm -rdf ${LAMBDA_TASK_ROOT}/numpy/doc/ && \
    rm -rdf ${LAMBDA_TASK_ROOT}/stack

CMD [ "titiler_pds.handler.handler" ]
