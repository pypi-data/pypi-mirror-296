from alembic.autogenerate.api import AutogenContext
from alembic.autogenerate.compare import comparators
from alembic.autogenerate.render import renderers

from sqlalchemy_declarative_extensions.function.compare import (
    CreateFunctionOp,
    DropFunctionOp,
    Operation,
    UpdateFunctionOp,
    compare_functions,
)


@comparators.dispatch_for("schema")
def _compare_functions(autogen_context, upgrade_ops, _):
    metadata = autogen_context.metadata
    functions = metadata.info.get("functions")
    if not functions:
        return

    result = compare_functions(autogen_context.connection, functions, metadata)
    upgrade_ops.ops.extend(result)


@renderers.dispatch_for(CreateFunctionOp)
@renderers.dispatch_for(UpdateFunctionOp)
@renderers.dispatch_for(DropFunctionOp)
def render_create_function(autogen_context: AutogenContext, op: Operation):
    assert autogen_context.connection
    commands = op.to_sql()
    return [f'op.execute("""{command}""")' for command in commands]
