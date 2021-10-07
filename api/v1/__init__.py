from flask import Blueprint

api_v1 = Blueprint('api_v1',__name__)

from . import anna_data_vms
from . import anna_data_divas
from . import anna_data_vurixdms
from . import anna_data_aruba
from . import anna_data_videotransfer
from . import anna_data_download