import prefect
from prefect.client.client import Client

cli = Client()

cli.create_flow_run(
    flow_id="786bc84d-10e0-4b60-919f-27c41ce9b33b",
    run_name="xxx",
    parameters=dict(
        
    )
)