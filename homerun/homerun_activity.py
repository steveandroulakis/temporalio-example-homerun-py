import asyncio
import logging
from dataclasses import dataclass
from datetime import timedelta

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker


@dataclass
class ProgressInput:
    progress: int


# express progress as a percentage
@activity.defn
async def progress_percentage(input: ProgressInput) -> str:
    activity.logger.info("Running activity with parameter %s" % input)
    return f"{input.progress * 10}%"


# Basic workflow that logs and invokes an activity
@workflow.defn
class ProgressWorkflow:
    @workflow.run
    async def run(self) -> str:
        workflow.logger.info("Running workflow")

        currentProgress = 0
        count = 0
        progressPercentage = '0%'

        # todo query here

        # todo signal here

        print('The pitcher threw the ball!')

        try:
            for i in range(11):
                count = i
                progressPercentage = await workflow.execute_activity(
                    progress_percentage,
                    ProgressInput(count),
                    start_to_close_timeout=timedelta(minutes=1),
                )
                print(progressPercentage)
                await asyncio.sleep(2)
                currentProgress = currentProgress + 10
            print('Nobody swung at the ball!')
            return
        except asyncio.CancelledError:
            print('Ball was swung at, I wonder if it was hit?')
            raise


async def main():
    # Uncomment the line below to see logging
    # logging.basicConfig(level=logging.INFO)

    # Start client
    client = await Client.connect("localhost:7233")

    # Run a worker for the workflow
    async with Worker(
        client,
        task_queue="homerun",
        workflows=[ProgressWorkflow],
        activities=[progress_percentage],
    ):

        # start the task (ball flying through the air for 20 seconds)
        result = await client.execute_workflow(
            ProgressWorkflow.run,
            id="homerun-activity-workflow-id",
            task_queue="homerun",
        )

        print(f'A pitcher has thrown the ball (worker task started).')
        print(f"Swing (signal) at it when it's 70% of the way to hit a home run!")

        print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
