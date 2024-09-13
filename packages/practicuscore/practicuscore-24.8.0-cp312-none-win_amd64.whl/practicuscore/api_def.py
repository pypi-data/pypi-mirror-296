from enum import Enum

# DO NOT REMOVE the below import
from practicuscore.api_base import *  # pylint:disable=wildcard-import,unused-wildcard-import


class CreateProcessRequest(PRTRequest):
    pass


class CreateProcessResponse(PRTResponse):
    process_id: int = -1
    os_pid: int = -1


class StartExtSvcRequest(PRTRequest):
    svc_name: str = ""
    port: Optional[int] = None
    dark_mode: bool = True
    auto_start_after_failure: bool = False
    singleton_service_per_node: bool = True
    options: Optional[dict] = None


class StartExtSvcResponse(PRTResponse):
    port: int = -1
    options: Optional[dict] = None


class RestartNodeSvcRequest(PRTRequest):
    restart_reason_to_log: Optional[str] = None


class KillProcessRequest(PRTRequest):
    process_id: int = -1
    process_uuid: Optional[str] = None


class KillProcessesRequest(PRTRequest):
    process_id_list: Optional[List[int]] = None


class PingRequest(PRTRequest):
    pass


class HeartBeatRequest(PRTRequest):
    payload: Optional[dict] = None


class HeartBeatResponse(PRTResponse):
    payload: Optional[dict] = None


class CloneLogsRequest(PRTRequest):
    pass


class LoadRequest(PRTDataRequest):
    pass
    # response is csv, no class needed


class ExportDataRequest(PRTDataRequest):
    # conn_conf in base class is a mandatory field and is the destination of save
    source_conn_conf: Optional[Union[
        dict,
        ConnConf,
        WorkerFileConnConf,
        SqLiteConnConf,
        S3ConnConf,
        MYSQLConnConf,
        PostgreSQLConnConf,
        RedshiftConnConf,
        SnowflakeConnConf,
        MSSQLConnConf,
        OracleConnConf,
        HiveConnConf,
        AthenaConnConf,
        TrinoConnConf,
        DremioConnConf,
        HanaConnConf,
        TeradataConnConf,
        Db2ConnConf,
        DynamoDBConnConf,
        CockroachDBConnConf,
        ClouderaConnConf,
        CustomDBConnConf,
    ]] = None
    step_dict_list: Optional[List[dict]] = None
    # response is op_result


class GetDFRequest(PRTRequest):
    sampling_method: Optional[str] = None
    sample_size_app: Optional[int] = None


class WSStateKeys:
    DF_FULL_TYPE_NAME = "DF_FULL_TYPE_NAME"
    DF_LOADED_ROWS_COUNT = "DF_LOADED_ROWS_COUNT"


class GetWSStateRequest(PRTRequest):
    wait_for_free_sec: float = 600.0
    generic_attributes_keys: Optional[List[str]] = None


class GetWSStateResponse(PRTResponse):
    busy: bool = False
    step_dict_list: Optional[List[dict]] = None
    async_op_issues_json_list: Optional[List[str]] = None
    generic_attributes_dict: Optional[dict] = None


class RunStepsRequest(PRTRequest):
    # used to run for "Node only" steps. Using dict, since Step is not a Pydantic model
    step_dict_list: Optional[List[dict]] = None
    reset_steps: bool = False


class GetObjectStorageMetaRequest(PRTDataRequest):
    prefix: Optional[str] = None
    max_size: Optional[int] = None
    starting_token: Optional[str] = None
    element_uuid: Optional[str] = None


class StorageMetaChildrenLoadStatus(str, Enum):
    NOT_LOADED = "NOT_LOADED"
    LOADED = "LOADED"
    WONT_LOAD = "WONT_LOAD"


class ObjectStorageMeta(PrtBaseModel):
    key: Optional[str] = None
    name: Optional[str] = None
    prefix: Optional[str] = None
    is_folder: Optional[bool] = None
    size: Optional[int] = None
    last_modified: Optional[datetime] = None
    level: int = 0
    children: Optional[List['ObjectStorageMeta']] = None
    children_loaded: StorageMetaChildrenLoadStatus = StorageMetaChildrenLoadStatus.NOT_LOADED

    @property
    def is_file(self) -> bool:
        return not self.is_folder


class GetObjectStorageMetaResponse(PRTResponse):
    meta_list: Optional[List[ObjectStorageMeta]] = None


class ConnSelectionStats(PrtBaseModel):
    # statistics about a selected key or keys
    size_per_row: Optional[int] = None
    sample_size_in_bytes: Optional[int] = None
    sample_rows: Optional[int] = None
    total_size_in_bytes: Optional[int] = None
    total_rows: Optional[int] = None


class PreviewRequest(PRTDataRequest):
    pass


class PreviewResponse(PRTResponse):
    selection_stats: Optional[ConnSelectionStats] = None
    csv_str: Optional[str] = None
    preview_text: Optional[str] = None


class TestConnectionRequest(PRTDataRequest):
    pass


class GetFileStatusRequest(PRTRequest):
    node_path_list: Optional[List[str]] = None
    recursive: bool = False


class FileStatus(PrtBaseModel):
    file_path: str
    file_size: int
    file_epoch: float


class GetFileStatusResponse(PRTResponse):
    file_status_list: Optional[List[FileStatus]] = None


class UploadFilesRequest(PRTRequest):
    # opens a multipart app to Worker communication channel. files/file parts are communicated chunk by chunk
    pass


class UploadFilesToCloudRequest(PRTRequest):
    conn_conf: Optional[Union[
        S3ConnConf
    ]] = None


class UploadWorkerFilesRequest(PRTRequest):
    conn_conf: Optional[Union[
        S3ConnConf
    ]] = None
    source_path_list: Optional[List[str]] = None
    target_dir_path: Optional[str] = None
    source_path_to_cut: Optional[str] = None


class DownloadFilesRequest(PRTRequest):
    node_path_list: Optional[List[str]] = None
    recursive: bool = False


class CopyFilesRequest(PRTRequest):
    source_path_list: Optional[List[str]] = None
    target_dir_path: Optional[str] = None
    source_path_to_cut: Optional[str] = None


class ProfileWSRequest(PRTRequest):
    profile_uuid: Optional[str] = None
    title: Optional[str] = None
    compare_to_original: Optional[bool] = None


class ProfileWSResponse(PRTResponse):
    started_profiling: Optional[bool] = None


class ViewLogsRequest(PRTRequest):
    view_practicus_log: bool = True
    log_size_mb: int = 10


class ViewLogsResponse(PRTResponse):
    practicus_log: Optional[str] = None


class TestGenericRequest(PRTRequest):
    some_str: Optional[str] = None


class TestGenericResponse(PRTResponse):
    some_result: Optional[str] = None


class RunScriptRequest(PRTRequest):
    script_path: Optional[str] = None
    run_as_sudo: bool = False
    timeout_secs: int = 120
    wait_for_end: bool = True


class RunScriptResponse(PRTResponse):
    std_out: str = ""
    std_err: str = ""


class FlushLogsRequest(PRTRequest):
    pass


class XLImportRequest(PRTRequest):
    file_name: str = ""


class XLImportResponse(PRTResponse):
    dp_content: str = ""
    dp_err_warning: str = ""


class TestCodeRequest(PRTRequest):
    sampling_method: Optional[str] = "ALL"
    sample_size: Optional[int] = 1000
    code_block_encoded: Optional[str] = None
    is_sql: Optional[bool] = None
    sql_table_name: Optional[str] = None


class TestCodeResponse(PRTResponse):
    test_result_csv_b: Optional[str] = None


class GenerateCodeRequest(PRTRequest):
    worksheets_dict: Optional[dict] = None
    template: Optional[str] = None
    app_user_name: Optional[str] = None
    export_name: Optional[str] = None
    dag_flow: Optional[str] = None
    schedule_start_date_ts: Optional[float] = None
    schedule_interval: Optional[str] = None
    save_cloud_credentials: bool = False
    params: Optional[dict] = None  # Worker + auth details (if requested by user)


class GenerateCodeResponse(PRTResponse):
    generated_file_paths: Optional[List[str]] = None


class CreateFolderRequest(PRTDataRequest):
    full_path: Optional[str] = None


class ModelAPIHeaderMeta(PrtBaseModel):
    # x-prt-... Http headers of a model api
    model_id: int | None = None
    model_version: str | None = None
    model_deployment_key: str | None = None
    pod_name: str | None = None
    model_prefix: str | None = None
    model_name: str | None = None
    traffic_weight: int | None = None
    auth_detail: str | None = None
    extra_config: str | None = None


class ModelConfig(PrtBaseModel):
    state: Optional[str] = None
    percent_complete: Optional[int] = None
    model_name: Optional[str] = None
    model_desc: Optional[str] = None
    target: Optional[str] = None
    re_sample_size: Optional[int] = None
    model_dir: Optional[str] = None
    short_model_name: Optional[str] = None
    version_name: Optional[str] = None
    problem_type: Optional[str] = None
    limit_to_models: Optional[str] = None
    use_gpu: Optional[bool] = None
    explain: Optional[bool] = None
    sensitive_features: Optional[str] = None
    user_name: Optional[str] = None
    node_name: Optional[str] = None
    node_instance_id: Optional[str] = None
    setup_params: Optional[dict] = None
    tune_params: Optional[dict] = None
    model_signature_json: Optional[str] = None
    # Feature selection
    feature_selection_percent: Optional[int] = None
    features_ignored: Optional[str] = None
    # Time Series
    time_feature: Optional[str] = None
    time_frequency: Optional[str] = None
    # Clustering
    num_clusters: Optional[int] = None
    # Engines etc. versions
    py_version: Optional[str] = None
    auto_ml_engine: Optional[str] = None
    auto_ml_version: Optional[str] = None
    # Experiment logging
    log_exp_name: Optional[str] = None
    log_experiment_service_key: Optional[str] = None
    log_experiment_service_name: Optional[str] = None
    log_exp_id: Optional[str] = None
    log_exp_full_parent_run_id: Optional[str] = None
    log_exp_full_final_run_id: Optional[str] = None
    final_model: Optional[str] = None
    score: Optional[float] = None
    errors: Optional[str] = None
    summary: Optional[str] = None

    @property
    def input_columns(self) -> List[str]:
        input_cols = []
        try:
            if self.model_signature_json is not None:
                import json
                signature_json = json.loads(self.model_signature_json)
                if "inputs" in signature_json:
                    inputs_dict_list = json.loads(signature_json["inputs"])
                    for input_dict in inputs_dict_list:
                        input_cols.append(input_dict["name"])
        except:
            from practicuscore.log_manager import get_logger, Log
            logger = get_logger(Log.CORE)
            logger.error(
                f"Unable to extract input columns from model_signature_json: {self.model_signature_json}.",
                exc_info=True)
        finally:
            return input_cols

    def save(self, json_path: str):
        with open(json_path, "wt") as f:
            f.write(self.model_dump_json())

    def __str__(self):
        return self.model_dump_json(indent=4)

    @staticmethod
    def load(model_conf: str | dict) -> Optional['ModelConfig']:
        """
        Model configuration Json or dictionary
        :param model_conf:
        :return:
        """
        if isinstance(model_conf, str):
            import json
            model_conf = json.loads(model_conf)

        if isinstance(model_conf, dict):
            return ModelConfig.model_validate(model_conf)

        return None


class CreateModelRequest(PRTRequest):
    model_conf: Optional[ModelConfig] = None
    status_check: bool = False
    last_reported_log_byte: int = 0


class CreateModelResponse(PRTResponse):
    model_conf: Optional[ModelConfig] = None
    current_log: Optional[str] = None
    last_reported_log_byte: int = 0


class RegisterModelRequest(PRTRequest):
    model_dir: Optional[str] = None


class ModelSearchResult(PrtBaseModel):
    model_name: Optional[str] = None
    latest_v: Optional[int] = None
    latest_v_timestamp: Optional[int] = None
    latest_staging_v: Optional[int] = None
    latest_staging_timestamp: Optional[int] = None
    latest_prod_v: Optional[int] = None
    latest_prod_timestamp: Optional[int] = None


class ModelSearchResults(PrtBaseModel):
    results: Optional[List[ModelSearchResult]] = None


class SearchModelsRequest(PRTRequest):
    filter_string_b64: Optional[str] = None
    max_results: int = 100


class SearchModelsResponse(PRTResponse):
    model_search_results: Optional[ModelSearchResults] = None


class GetModelMetaRequest(PRTRequest):
    model_uri: Optional[str] = None
    model_json_path: Optional[str] = None


class GetModelMetaResponse(PRTResponse):
    model_conf_json: Optional[str] = None
    prepare_ws_b64: Optional[str] = None


class GetSystemStatRequest(PRTRequest):
    pass


class GetSystemStatResponse(PRTResponse):
    system_stat: Optional[dict] = None
    node_version: Optional[str] = None


class DeleteKeysRequest(PRTDataRequest):
    keys: Optional[List[str]] = None
    delete_sub_keys: bool = False


class ListBucketsRequest(PRTDataRequest):
    pass


class ListBucketsResponse(PRTResponse):
    buckets: Optional[List[str]] = None


class ReplicateNodeRequest(PRTRequest):
    source_node_name: Optional[str] = None
    source_node_dns: Optional[str] = None
    source_node_pem_data: Optional[str] = None
    timeout_secs: int = 30 * 60  # 30 minutes


class UploadModelFilesRequest(PRTRequest):
    model_dir: Optional[str] = None
    region_url: Optional[str] = None
    deployment_key: Optional[str] = None
    token: Optional[str] = None
    prefix: Optional[str] = None
    model_id: Optional[int] = None
    model_name: Optional[str] = None
    version: Optional[str] = None


class UploadModelFilesResponse(PRTResponse):
    model_url: Optional[str] = None


class DeployWorkflowRequest(PRTRequest):
    workflow_service_key: Optional[str] = None
    destination_dir_path: Optional[str] = None
    files_dir_path: Optional[str] = None


class CreatePlotRequest(PRTRequest):
    dark_mode: bool = False


class CreatePlotResponse(PRTResponse):
    plot_token: Optional[str] = None


class UpdateWsNameRequest(PRTRequest):
    ws_name: Optional[str] = None


class RunTaskRequest(PRTRequest):
    task_uuid: Optional[str] = None
    task_file_path: Optional[str] = None


class CheckTaskStateRequest(PRTRequest):
    task_uuid: Optional[str] = None


class TaskState(str, Enum):
    UNKNOWN = "UNKNOWN"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

    @classmethod
    def from_value(cls, value: Union[str, Enum]) -> 'TaskState':
        str_val = str(value.value if hasattr(value, "value") else value).upper()
        for i, enum_val in enumerate(cls):
            # noinspection PyUnresolvedReferences
            if str(enum_val.value).upper() == str_val:
                return cls(enum_val)

        raise ValueError(f'{value} is not a valid {cls}')


class CheckTaskStateResponse(PRTResponse):
    task_state: TaskState = TaskState.UNKNOWN
