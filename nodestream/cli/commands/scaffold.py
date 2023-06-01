from ..operations import (
    AddPipelineToProject,
    GeneratePipelineScaffold,
    InitializeProject,
    CommitProjectToDisk,
)
from .nodestream_command import NodestreamCommand
from .shared_options import (
    DATABASE_NAME_OPTION,
    PROJECT_FILE_OPTION,
    SCOPE_NAME_OPTION,
    PIPELINE_ARGUMENT,
)


class Scaffold(NodestreamCommand):
    name = "scaffold"
    description = "Generate a New Nodestream Pipeline"
    arguments = [PIPELINE_ARGUMENT]
    options = [DATABASE_NAME_OPTION, SCOPE_NAME_OPTION, PROJECT_FILE_OPTION]

    async def handle_async(self):
        pipeline_name = self.argument("pipeline")
        desired_scope = self.option("scope")
        database_name = self.option("database")
        project = await self.run_operation(InitializeProject())
        generated_pipelines = await self.run_operation(
            GeneratePipelineScaffold(
                project_root=self.get_project_path().parent,
                database_name=database_name,
                pipeline_file_name=pipeline_name + ".yaml",
            )
        )
        for generated_pipeline in generated_pipelines:
            await self.run_operation(
                AddPipelineToProject(project, generated_pipeline, desired_scope)
            )

        await self.run_operation(CommitProjectToDisk(project, self.get_project_path()))
