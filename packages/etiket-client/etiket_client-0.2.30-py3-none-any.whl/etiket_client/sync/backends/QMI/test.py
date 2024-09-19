import pathlib
import dataclasses

from lark import logger

@dataclasses.dataclass
class FileSyncExampleConfig:
    data_storage_location: pathlib.Path
    set_up: str
    sample_name : str
    
from etiket_client.sync.base.sync_source_abstract import SyncSourceFileBase
from etiket_client.sync.base.sync_utilities import file_info, sync_utilities,\
    dataset_info, sync_item, FileType
    
import pathlib, os, json, datetime, xarray, logging

logger = logging.getLogger(__name__)

class MySyncAgentSync(SyncSourceFileBase):
    SyncAgentName = "SimpleFileSync"
    ConfigDataClass = FileSyncExampleConfig
    MapToASingleScope = True
    LiveSyncImplemented = False
    level = 2
    
    @staticmethod
    def rootPath(configData: FileSyncExampleConfig) -> pathlib.Path:
        return configData.data_storage_location

    @staticmethod
    def checkLiveDataset(configData: FileSyncExampleConfig, syncIdentifier: sync_item, isNewest: bool) -> bool:
        # to keep things simple, we assume here files are only written when they are completed (i.e. at the end of a measurement)
        return False
    
    @staticmethod
    def syncDatasetNormal(configData: FileSyncExampleConfig, syncIdentifier: sync_item):
        create_dataset(configData, syncIdentifier)
        
        # if metadata.json is present, we upload it as a file
        metadata_path = os.path.join(configData.data_storage_location, syncIdentifier.dataIdentifier, "metadata.json")
        upload_file_if_exists(pathlib.Path(metadata_path), "metadata", FileType.JSON, syncIdentifier)
        
        # if measurement.csv is present, we upload it as a file and convert it to an xarray dataset
        measurement_path = os.path.join(configData.data_storage_location, syncIdentifier.dataIdentifier, "measurement.csv")
        if os.path.exists(measurement_path):
            # filetype is currently set to TEXT (CSV not yet supported)
            upload_file_if_exists(pathlib.Path(measurement_path), "measurement", FileType.TEXT, syncIdentifier)
            
            # Convert the csv file to an xarray dataset
            try:
                with measurement_path.open("r") as f:
                    first_line = f.readline().strip()
                    if first_line.startswith('#'):
                        first_line = first_line[1:].strip()
                    variables = first_line.split(",")

                    data = [list(map(float, line.strip().split(" "))) for line in f]
                    data = list(zip(*data))

                    x_axis_name, x_axis_unit = split_axis_and_unit(variables[0])
                    y_axis_name, y_axis_unit = split_axis_and_unit(variables[1])

                    ds = xarray.Dataset(
                        {
                            y_axis_name: ([x_axis_name,], list(data[1]), {"units": y_axis_unit}),
                        },
                        coords={
                            x_axis_name: (x_axis_name, list(data[0]), {"units": x_axis_unit})
                        },
                    )
                    sync_utilities.upload_xarray(ds, syncIdentifier, "measurement")
            except Exception:
                logger.exception(f"Error converting {measurement_path} to xarray dataset.")

    @staticmethod
    def syncDatasetLive(configData: FileSyncExampleConfig, syncIdentifier: sync_item):
        raise NotImplementedError


def upload_file_if_exists(file_path: pathlib.Path, file_name : str, file_type : FileType, syncIdentifier : sync_item):
    if file_path.exists():
        f_info = file_info(
            name=file_name,
            fileName=file_path.name,
            created=datetime.datetime.fromtimestamp(file_path.stat().st_mtime),
            fileType=file_type,
            file_generator="SimpleFileSync"
        )
        sync_utilities.upload_file(str(file_path), syncIdentifier, f_info)

def split_axis_and_unit(input_string : str):
    open_paren_index = input_string.find('(')
    close_paren_index = input_string.find(')')
    
    if open_paren_index == -1 or close_paren_index == -1:
        axis_name = input_string.strip()
        unit = None
    else:
        axis_name = input_string[:open_paren_index].strip()
        unit = input_string[open_paren_index + 1:close_paren_index].strip()
        
        if unit == "a.u.":
            unit = None
    
    return axis_name, unit     

def create_dataset(configData: FileSyncExampleConfig, syncIdentifier: sync_item):
    dataset_path = pathlib.Path(os.path.join(configData.data_storage_location, syncIdentifier.dataIdentifier))
    dataset_name = "Dataset"
    keywords = []
    attributes = {"set_up": configData.set_up, "sample_name": configData.sample_name}
    
    # find dataset name (if file exists and key is present)
    try:
        with open(os.path.join(dataset_path, "metadata.json"), "r") as f:
            metadata = json.load(f)
            dataset_name = metadata["exp_name"]
            # additional attributes could be added here
    except:
        pass
    
    # try to add the variable names to the keywords, as they will allow for searching on these.
    try:
        with open(os.path.join(dataset_path, "measurement.csv"), "r") as f:
            line = f.readline()
            keywords = line.split(",")
    except:
        pass
    
    # when the folder was created, we take as the creation time of the dataset
    created = datetime.datetime.fromtimestamp(pathlib.Path(dataset_path).stat().st_mtime)
    
    ds_info = dataset_info(name = dataset_name, datasetUUID = syncIdentifier.datasetUUID,
            alt_uid = syncIdentifier.dataIdentifier, scopeUUID = syncIdentifier.scopeUUID,
            created = created, keywords = list(keywords), 
            attributes = attributes)
    sync_utilities.create_ds(False, syncIdentifier, ds_info)