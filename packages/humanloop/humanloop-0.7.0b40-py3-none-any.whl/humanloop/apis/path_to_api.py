import typing_extensions

from humanloop.paths import PathValues
from humanloop.apis.paths.chat import Chat
from humanloop.apis.paths.chat_deployed import ChatDeployed
from humanloop.apis.paths.chat_model_config import ChatModelConfig
from humanloop.apis.paths.completion import Completion
from humanloop.apis.paths.completion_deployed import CompletionDeployed
from humanloop.apis.paths.completion_model_config import CompletionModelConfig
from humanloop.apis.paths.datapoints_id import DatapointsId
from humanloop.apis.paths.datapoints import Datapoints
from humanloop.apis.paths.projects_project_id_datasets import ProjectsProjectIdDatasets
from humanloop.apis.paths.datasets import Datasets
from humanloop.apis.paths.datasets_id import DatasetsId
from humanloop.apis.paths.datasets_dataset_id_datapoints import DatasetsDatasetIdDatapoints
from humanloop.apis.paths.evaluations_id import EvaluationsId
from humanloop.apis.paths.evaluations_id_datapoints import EvaluationsIdDatapoints
from humanloop.apis.paths.projects_project_id_evaluations import ProjectsProjectIdEvaluations
from humanloop.apis.paths.evaluations_evaluation_id_log import EvaluationsEvaluationIdLog
from humanloop.apis.paths.evaluations_evaluation_id_result import EvaluationsEvaluationIdResult
from humanloop.apis.paths.evaluations_id_status import EvaluationsIdStatus
from humanloop.apis.paths.evaluations_id_evaluators import EvaluationsIdEvaluators
from humanloop.apis.paths.evaluations import Evaluations
from humanloop.apis.paths.evaluators import Evaluators
from humanloop.apis.paths.evaluators_id import EvaluatorsId
from humanloop.apis.paths.feedback import Feedback
from humanloop.apis.paths.logs import Logs
from humanloop.apis.paths.logs_id import LogsId
from humanloop.apis.paths.model_configs import ModelConfigs
from humanloop.apis.paths.model_configs_id import ModelConfigsId
from humanloop.apis.paths.model_configs_id_export import ModelConfigsIdExport
from humanloop.apis.paths.model_configs_serialize import ModelConfigsSerialize
from humanloop.apis.paths.model_configs_deserialize import ModelConfigsDeserialize
from humanloop.apis.paths.projects import Projects
from humanloop.apis.paths.projects_id import ProjectsId
from humanloop.apis.paths.projects_id_configs import ProjectsIdConfigs
from humanloop.apis.paths.projects_id_active_config import ProjectsIdActiveConfig
from humanloop.apis.paths.projects_id_feedback_types import ProjectsIdFeedbackTypes
from humanloop.apis.paths.projects_id_export import ProjectsIdExport
from humanloop.apis.paths.projects_id_deployed_configs import ProjectsIdDeployedConfigs
from humanloop.apis.paths.projects_project_id_deploy_config import ProjectsProjectIdDeployConfig
from humanloop.apis.paths.projects_project_id_deployed_config_environment_id import ProjectsProjectIdDeployedConfigEnvironmentId
from humanloop.apis.paths.sessions import Sessions
from humanloop.apis.paths.sessions_id import SessionsId

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.CHAT: Chat,
        PathValues.CHATDEPLOYED: ChatDeployed,
        PathValues.CHATMODELCONFIG: ChatModelConfig,
        PathValues.COMPLETION: Completion,
        PathValues.COMPLETIONDEPLOYED: CompletionDeployed,
        PathValues.COMPLETIONMODELCONFIG: CompletionModelConfig,
        PathValues.DATAPOINTS_ID: DatapointsId,
        PathValues.DATAPOINTS: Datapoints,
        PathValues.PROJECTS_PROJECT_ID_DATASETS: ProjectsProjectIdDatasets,
        PathValues.DATASETS: Datasets,
        PathValues.DATASETS_ID: DatasetsId,
        PathValues.DATASETS_DATASET_ID_DATAPOINTS: DatasetsDatasetIdDatapoints,
        PathValues.EVALUATIONS_ID: EvaluationsId,
        PathValues.EVALUATIONS_ID_DATAPOINTS: EvaluationsIdDatapoints,
        PathValues.PROJECTS_PROJECT_ID_EVALUATIONS: ProjectsProjectIdEvaluations,
        PathValues.EVALUATIONS_EVALUATION_ID_LOG: EvaluationsEvaluationIdLog,
        PathValues.EVALUATIONS_EVALUATION_ID_RESULT: EvaluationsEvaluationIdResult,
        PathValues.EVALUATIONS_ID_STATUS: EvaluationsIdStatus,
        PathValues.EVALUATIONS_ID_EVALUATORS: EvaluationsIdEvaluators,
        PathValues.EVALUATIONS: Evaluations,
        PathValues.EVALUATORS: Evaluators,
        PathValues.EVALUATORS_ID: EvaluatorsId,
        PathValues.FEEDBACK: Feedback,
        PathValues.LOGS: Logs,
        PathValues.LOGS_ID: LogsId,
        PathValues.MODELCONFIGS: ModelConfigs,
        PathValues.MODELCONFIGS_ID: ModelConfigsId,
        PathValues.MODELCONFIGS_ID_EXPORT: ModelConfigsIdExport,
        PathValues.MODELCONFIGS_SERIALIZE: ModelConfigsSerialize,
        PathValues.MODELCONFIGS_DESERIALIZE: ModelConfigsDeserialize,
        PathValues.PROJECTS: Projects,
        PathValues.PROJECTS_ID: ProjectsId,
        PathValues.PROJECTS_ID_CONFIGS: ProjectsIdConfigs,
        PathValues.PROJECTS_ID_ACTIVECONFIG: ProjectsIdActiveConfig,
        PathValues.PROJECTS_ID_FEEDBACKTYPES: ProjectsIdFeedbackTypes,
        PathValues.PROJECTS_ID_EXPORT: ProjectsIdExport,
        PathValues.PROJECTS_ID_DEPLOYEDCONFIGS: ProjectsIdDeployedConfigs,
        PathValues.PROJECTS_PROJECT_ID_DEPLOYCONFIG: ProjectsProjectIdDeployConfig,
        PathValues.PROJECTS_PROJECT_ID_DEPLOYEDCONFIG_ENVIRONMENT_ID: ProjectsProjectIdDeployedConfigEnvironmentId,
        PathValues.SESSIONS: Sessions,
        PathValues.SESSIONS_ID: SessionsId,
    }
)

path_to_api = PathToApi(
    {
        PathValues.CHAT: Chat,
        PathValues.CHATDEPLOYED: ChatDeployed,
        PathValues.CHATMODELCONFIG: ChatModelConfig,
        PathValues.COMPLETION: Completion,
        PathValues.COMPLETIONDEPLOYED: CompletionDeployed,
        PathValues.COMPLETIONMODELCONFIG: CompletionModelConfig,
        PathValues.DATAPOINTS_ID: DatapointsId,
        PathValues.DATAPOINTS: Datapoints,
        PathValues.PROJECTS_PROJECT_ID_DATASETS: ProjectsProjectIdDatasets,
        PathValues.DATASETS: Datasets,
        PathValues.DATASETS_ID: DatasetsId,
        PathValues.DATASETS_DATASET_ID_DATAPOINTS: DatasetsDatasetIdDatapoints,
        PathValues.EVALUATIONS_ID: EvaluationsId,
        PathValues.EVALUATIONS_ID_DATAPOINTS: EvaluationsIdDatapoints,
        PathValues.PROJECTS_PROJECT_ID_EVALUATIONS: ProjectsProjectIdEvaluations,
        PathValues.EVALUATIONS_EVALUATION_ID_LOG: EvaluationsEvaluationIdLog,
        PathValues.EVALUATIONS_EVALUATION_ID_RESULT: EvaluationsEvaluationIdResult,
        PathValues.EVALUATIONS_ID_STATUS: EvaluationsIdStatus,
        PathValues.EVALUATIONS_ID_EVALUATORS: EvaluationsIdEvaluators,
        PathValues.EVALUATIONS: Evaluations,
        PathValues.EVALUATORS: Evaluators,
        PathValues.EVALUATORS_ID: EvaluatorsId,
        PathValues.FEEDBACK: Feedback,
        PathValues.LOGS: Logs,
        PathValues.LOGS_ID: LogsId,
        PathValues.MODELCONFIGS: ModelConfigs,
        PathValues.MODELCONFIGS_ID: ModelConfigsId,
        PathValues.MODELCONFIGS_ID_EXPORT: ModelConfigsIdExport,
        PathValues.MODELCONFIGS_SERIALIZE: ModelConfigsSerialize,
        PathValues.MODELCONFIGS_DESERIALIZE: ModelConfigsDeserialize,
        PathValues.PROJECTS: Projects,
        PathValues.PROJECTS_ID: ProjectsId,
        PathValues.PROJECTS_ID_CONFIGS: ProjectsIdConfigs,
        PathValues.PROJECTS_ID_ACTIVECONFIG: ProjectsIdActiveConfig,
        PathValues.PROJECTS_ID_FEEDBACKTYPES: ProjectsIdFeedbackTypes,
        PathValues.PROJECTS_ID_EXPORT: ProjectsIdExport,
        PathValues.PROJECTS_ID_DEPLOYEDCONFIGS: ProjectsIdDeployedConfigs,
        PathValues.PROJECTS_PROJECT_ID_DEPLOYCONFIG: ProjectsProjectIdDeployConfig,
        PathValues.PROJECTS_PROJECT_ID_DEPLOYEDCONFIG_ENVIRONMENT_ID: ProjectsProjectIdDeployedConfigEnvironmentId,
        PathValues.SESSIONS: Sessions,
        PathValues.SESSIONS_ID: SessionsId,
    }
)
