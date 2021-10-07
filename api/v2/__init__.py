from flask import Blueprint

api_v2 = Blueprint('api_v2',__name__)

from . import v2_pre_vms
from . import v2_pre_videotransfer
from . import v2_pre_vurixdms
from . import v2_pre_divas
from . import v2_pre_aruba
from . import v2_pre_common
from . import v2_pre_weather
from . import v2_pre_forest