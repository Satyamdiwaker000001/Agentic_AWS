FROM public.ecr.aws/lambda/python:3.11

# Copy requirements and install
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
# Also install mangum for lambda handler
RUN pip install mangum --target "${LAMBDA_TASK_ROOT}"

# Copy the backend code
COPY SRS_Compliance_Analyzer/ ${LAMBDA_TASK_ROOT}/

# Set the CMD to the handler
CMD [ "main.handler" ]
