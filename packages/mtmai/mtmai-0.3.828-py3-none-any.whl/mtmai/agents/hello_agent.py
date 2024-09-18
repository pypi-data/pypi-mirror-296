import chainlit as cl


async def hello_step():
    async with cl.Step(name="Parent step") as parent_step:
        parent_step.input = "Parent step input"

        async with cl.Step(name="Child step") as child_step:
            child_step.input = "Child step input"
            child_step.output = "Child step output"

        parent_step.output = "Parent step output"


@cl.step
async def my_step():
    current_step = cl.context.current_step

    # Override the input of the step
    current_step.input = "My custom input"

    # Override the output of the step
    current_step.output = "My custom output"


@cl.step
async def my_step2():
    current_step = cl.context.current_step

    # Override the input of the step
    current_step.input = "My custom input2"

    # Override the output of the step
    current_step.output = "My custom output2"
