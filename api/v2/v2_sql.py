# from sqlalchemy.types import *

# vms_device = {
#     "dev_serial":BIGINT(),

# }

# Anna(DMS-BI) SQL

# CONT -> CHECK EXISTS TABLE
#############################################################################
q_is_table = '''
    SELECT *
    FROM INFORMATION_SCHEMA.tables WITH(NOLOCK)
    WHERE TABLE_SCHEMA = '{schema}'
    AND TABLE_NAME = '{table}'
'''


# CONT -> DROP TABLE
#############################################################################
q_drop_table = '''
    DROP TABLE IF EXISTS {schema}.{table}
'''


# CREATE TABLE -> dms_layer_cctv
# For hadong
q_dms_layer_cctv_2nd = '''
    DROP TABLE IF EXISTS {schema}.{table};
    CREATE TABLE {schema}.{table}(
            cctv_id                                 nvarchar(128)   NULL,
            area                                    nvarchar(20)    NOT NULL,
            name                                    nvarchar(128)   NOT NULL,
            hjd_bjcd                                nvarchar(32)    NULL,
            hjd_name                                nvarchar(32)    NULL,
            emd_bjcd                                nvarchar(32)    NULL,
            emd_name                                nvarchar(32)    NULL,
            asset_type                              nvarchar(20)    NOT NULL,
            latitude                                nvarchar(36)    NOT NULL,
            longitude                               nvarchar(36)    NOT NULL,
            sublayer_id                             nvarchar(50)    NOT NULL,
            install_date                            nvarchar(50)    NULL,
            address                                 nvarchar(256)   NULL,
            model                                   nvarchar(128)   NULL,
            state                                   nvarchar(20)    NULL,
            vms_type                                nvarchar(20)    NULL,
            reg_date                                datetime        NULL,
            upd_date                                datetime        NULL,
            db_update_time                          datetime        NULL,
            PRIMARY KEY CLUSTERED
            (
                name ASC
            )
        );
'''

# CREATE TABLE -> dms_layer_cctv
q_dms_layer_cctv = '''
    DROP TABLE IF EXISTS {schema}.{table};
    CREATE TABLE {schema}.{table}(
            cctv_id                                 nvarchar(128)   NULL,
            area                                    nvarchar(20)    NOT NULL,
            name                                    nvarchar(128)   NOT NULL,
            hjd_bjcd                                nvarchar(32)    NULL,
            hjd_name                                nvarchar(32)    NULL,
            emd_bjcd                                nvarchar(32)    NULL,
            emd_name                                nvarchar(32)    NULL,
            asset_type                              nvarchar(20)    NOT NULL,
            latitude                                nvarchar(36)    NOT NULL,
            longitude                               nvarchar(36)    NOT NULL,
            sublayer_id                             nvarchar(50)    NOT NULL,
            install_date                            nvarchar(50)    NULL,
            asset_id                                nvarchar(128)   NULL,
            address                                 nvarchar(256)   NULL,
            model                                   nvarchar(128)   NULL,
            state                                   nvarchar(20)    NULL,
            vms_type                                nvarchar(20)    NULL,
            ptz                                     bit             NULL,
            direction                               float           NULL,
            distance                                float           NULL,
            poll_num                                nvarchar(128)   NULL,
            pixel                                   varchar(50)     NULL,
            storage_server                          nvarchar(128)   NULL,
            stream                                  nvarchar(128)   NULL,
            frame                                   nvarchar(128)   NULL,
            reg_date                                datetime        NULL,
            upd_date                                datetime        NULL,
            bjcd                                    nvarchar(10)    NULL,
            db_update_time                          datetime        NULL,
            PRIMARY KEY CLUSTERED
            (
                name ASC
            )
        );
'''


# CREATE TABLE -> vms_device
#############################################################################
q_vms_device = '''
    DROP TABLE IF EXISTS {schema}.{table};
    CREATE TABLE {schema}.{table}(
        dev_serial                                  BIGINT          NOT NULL,
        dev_name                                    NVARCHAR(255)   NULL,
        model_id                                    BIGINT          NULL,
        vms_id                                      BIGINT          NULL,
        dev_type                                    BIGINT          NULL,
        dev_stat                                    BIGINT          NULL,
        ins_time                                    DATETIME        NULL,
        mod_time                                    DATETIME        NULL,
        locationed                                  NVARCHAR(255)   NULL,
        db_update_time                              DATETIME        NULL,
        PRIMARY KEY CLUSTERED
        (
            dev_serial ASC
        )
    );
'''

# CREATE TABLE -> vms_device_channel
#############################################################################
q_vms_device_channel = '''
    DROP TABLE IF EXISTS {schema}.{table};
    CREATE TABLE {schema}.{table}(
        dch_id                                      INT             NOT NULL,
        srv_serial                                  INT             NULL,
        dev_serial                                  INT             NULL,
        vms_id                                      INT             NULL,
        dch_ch                                      INT             NULL,
        dch_type                                    INT             NULL,
        dch_media                                   INT             NULL,
        dch_defstrm                                 INT             NULL,
        dch_defrec                                  INT             NULL,
        ins_time                                    DATETIME        NULL,
        mod_time                                    DATETIME        DEFAULT NULL NULL,
        db_update_time                              DATETIME        NULL,
        PRIMARY KEY CLUSTERED
        (
            dch_id ASC
        )
    );
'''


# CREATE TABLE -> vms_device_media
#############################################################################
q_vms_device_media = '''
    DROP TABLE IF EXISTS {schema}.{table};
    CREATE TABLE {schema}.{table}(
        dchm_id                                     INT              NOT NULL,
        vms_id                                      INT              NOT NULL,
        dev_serial                                  INT              NOT NULL,
        dch_ch                                      INT              NOT NULL,
        dchm_serial                                 INT              NOT NULL,
        media_type                                  INT              NOT NULL,
        dchm_stat                                   INT              NOT NULL,
        dchm_url                                    NVARCHAR(1024)   NOT NULL,
        dchm_port                                   INT              NOT NULL,
        dchm_codec                                  NVARCHAR(128)    NULL,
        dchm_width                                  INT              NOT NULL,
        dchm_height                                 INT              NOT NULL,
        dchm_desc                                   NVARCHAR(64)     NULL,
        dchm_property                               NVARCHAR(1024)   NULL,
        ins_time                                    DATETIME         NOT NULL,
        mod_time                                    DATETIME         NULL,
        db_update_time                              DATETIME         NULL,
        PRIMARY KEY CLUSTERED
        (
            dchm_id ASC
        )
    );
'''


# CREATE TABLE -> vms_device_model
#############################################################################
q_vms_device_model = '''
    DROP TABLE IF EXISTS {schema}.{table};
    CREATE TABLE {schema}.{table}(
        model_id                                    INT              NOT NULL,
        model_name                                  NVARCHAR(45)     NOT NULL,
        company                                     NVARCHAR(45)     NULL,
        model_driver                                NVARCHAR(45)     NULL,
        ins_time                                    DATETIME         NOT NULL,
        mod_time                                    DATETIME         DEFAULT NULL NULL,
        db_update_time                              DATETIME         NULL,
        PRIMARY KEY CLUSTERED
        (
            model_id ASC
        )
    );
'''


# CREATE TABLE -> vms_servers
#############################################################################
q_vms_servers = '''
    DROP TABLE IF EXISTS {schema}.{table};
    CREATE TABLE {schema}.{table}(
        srv_serial                                  INT               NOT NULL,
        srv_id                                      BIGINT            NULL,
        srv_name                                    NVARCHAR(45)      NOT NULL,
        srv_stat                                    NVARCHAR(45)      NOT NULL,
        srv_type                                    NVARCHAR(45)      NOT NULL,
        vms_id                                      INT               NOT NULL,
        ins_time                                    DATETIME          NOT NULL,
        mod_time                                    DATETIME          NULL,
        db_update_time                              DATETIME          NULL,
        PRIMARY KEY CLUSTERED
        (
            srv_serial ASC
        )
    );
'''


# CREATE TABLE -> dms_layer_ap
#############################################################################
q_dms_layer_ap = '''
    DROP TABLE IF EXISTS {schema}.{table};
    CREATE TABLE {schema}.{table} (
        hjd_name 			nvarchar(100)   	NULL,
        hjd_bjcd 			varchar(20)   		NULL,
        emd_name 			nvarchar(100)   	NULL,
        emd_bjcd 			varchar(10)   		NULL,
        area 				nvarchar(20)   		NULL,
        name 				nvarchar(100)   	NOT NULL,
        asset_type 			nvarchar(100)   	NULL,
        install_date 		varchar(50)   		NULL,
        asset_id 			nvarchar(100)   	NULL,
        address 			nvarchar(250)   	NULL,
        model 				nvarchar(100)   	NULL,
        state 				varchar(6)   		NULL,
        sublayer_id 		nvarchar(64)   		NULL,
        ap_mac 				varchar(20)   		NULL,
        ap_serial 			varchar(50)   		NULL,
        company 			nvarchar(50)   		NULL,
        ip 					varchar(20)   		NULL,
        dept 				nvarchar(50)   		NULL,
        reg_date 			datetime 			NULL,
        upd_date 			datetime 			NULL,
        db_update_time 		datetime 			NULL,
        x 					varchar(32)   		NULL,
        y 					varchar(32)   		NULL,
        PRIMARY KEY (name)
    );
'''


# CREATE TABLE -> vms_user_log
#############################################################################
q_vms_user_log = '''
    IF NOT EXISTS
        (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME='{table}')
    CREATE TABLE {schema}.{table}
    (
        uuid                                        NVARCHAR(100)    NOT NULL,
        log_id                                      INT              NOT NULL,
        user_id                                     NVARCHAR(45)     NULL,
        log_type                                    INT              NULL,
        log_sub_type                                INT              NULL,
        log_info                                    NVARCHAR(2048)   NULL,
        target_type                                 INT              NULL,
        target_serial                               INT              NULL,
        target_name                                 NVARCHAR(1024)   NULL,
        log_time                                    DATETIME         NULL,
        ins_time                                    DATETIME         NOT NULL,
        db_update_time                              DATETIME         NOT NULL,
        PRIMARY KEY CLUSTERED
        (
            log_id ASC,
            ins_time ASC
        )
    );
'''


# CREATE TABLE -> vms_vfs_history
#############################################################################
q_vms_vfs_history = '''
    IF NOT EXISTS
        (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME='{table}')
    CREATE TABLE {schema}.{table}(
        history_serial                              NVARCHAR(60)     NOT NULL,
        srv_serial                                  INT              NULL,
        dev_serial                                  INT              NULL,
        dch_ch                                      INT              NULL,
        rec_time                                    DATETIME         NULL,
        rec_size                                    BIGINT           NULL,
        db_update_time                              DATETIME         NULL,
        PRIMARY KEY CLUSTERED
        (
            history_serial ASC
        )
    );
'''


# CREATE TABLE -> vms_vfs_fail_history
#############################################################################
q_vms_vfs_fail_history = '''
    IF NOT EXISTS
        (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME='{table}')
    CREATE TABLE {schema}.{table}(
        dev_serial                                  INT              NOT NULL,
        dch_ch                                      INT              NOT NULL,
        srv_serial                                  INT              NOT NULL,
        rec_min                                     DATETIME         NOT NULL,
        rec_size                                    BIGINT           NULL,
        frame_index                                 NVARCHAR(128)    NULL,
        out_time                                    INT              NULL,
        db_update_time                              DATETIME         NULL,
        PRIMARY KEY CLUSTERED
        (
            dev_serial      ASC,
            dch_ch          ASC,
            srv_serial      ASC,
            rec_min         ASC
        )
    );
'''


# CREATE TABLE -> vms_server_status
#############################################################################
q_vms_server_status = '''
    IF NOT EXISTS
        (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME='{table}')
    CREATE TABLE {schema}.{table}(
        history_serial                              NVARCHAR(100)    NOT NULL,
        srv_name                                    NVARCHAR(255)    NOT NULL,
        srv_serial                                  INT              NOT NULL,
        groups_id                                   INT              NOT NULL,
        item_id                                     INT              NOT NULL,
        item_param                                  NVARCHAR(255)    NOT NULL,
        recv_count                                  INT              NULL,
        item_min_time                               DATETIME         NULL,
        item_max_time                               DATETIME         NULL,
        item_value                                  INT              NULL,
        item_value_str                              NVARCHAR(255)    NULL,
        db_update_time                              DATETIME         NOT NULL,
        PRIMARY KEY CLUSTERED
        (
            srv_name ASC,
            srv_serial ASC,
            groups_id ASC,
            item_id ASC,
            item_param ASC,
            db_update_time ASC
        )
    );
'''


# CREATE TABLE -> videotransfer_csafer
#############################################################################
q_videotransfer_csafer = '''
    DROP TABLE IF EXISTS {schema}.{table};
    CREATE TABLE {schema}.{table} (
		request_id			 	nvarchar(20) 		NOT NULL,
		child_request_id		nvarchar(20) 		NOT NULL,
		dev_serial				varchar(32)			NULL,
		requestor			 	nvarchar(50) 		NULL,
		relationship			nvarchar(50) 		NULL,
		reason			 		nvarchar(255)		NULL,
		detailed_reason			nvarchar(255)		NULL,
		cctv			 		nvarchar(255)		NULL,
		camera_addr			 	nvarchar(408)		NULL,
		request_date			datetime			NOT NULL,
		update_date				nvarchar(255)		NULL,
		request_start			nvarchar(255)		NULL,
		request_end			 	nvarchar(255)		NULL,
		status			 		nvarchar(255)		NULL,
		result			 		nvarchar(255)		NULL,
		detailed_result			nvarchar(255)		NULL,
		longitude			 	nvarchar(32) 		NULL,
		latitude			 	nvarchar(32) 		NULL,
		db_update_time 			datetime			NULL,

        PRIMARY KEY CLUSTERED
        (
			request_id 		    ASC,
            child_request_id    ASC,
			request_date 	    ASC
        )
    ) 
'''

q_dms_lpr_data_part_yeongcheon01 = '''
    IF NOT EXISTS
        (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME='{table}')
    CREATE TABLE {schema}.{table}(
        cctv_id                     varchar(50)         NOT NULL, 
        day_hour_part		 		date		 		NOT NULL,
        cnt		 				    bigint 		        NULL,
        vhcty_asort_nm              nvarchar(50)        NOT NULL    DEFAULT '',
        vims_prpos_se_nm		 	nvarchar(50) 		NOT NULL    DEFAULT '',
        use_strnghld_area1          nvarchar(50)        NOT NULL    DEFAULT '',
        use_strnghld_area2          nvarchar(50)        NOT NULL    DEFAULT '',
        db_update_time				datetime			NOT NULL,
        PRIMARY KEY CLUSTERED 
        (
            cctv_id             ASC,
            day_hour_part		ASC,
            vhcty_asort_nm 		ASC,
            vims_prpos_se_nm    ASC,
            use_strnghld_area1  ASC,
            use_strnghld_area2  ASC
        )
    ) ;
'''


q_dms_lpr_data_part_miryang01 = '''
    IF NOT EXISTS
        (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME='{table}')
    CREATE TABLE {schema}.{table}(
        day_hour_part		 		date		 		NOT NULL,
        cnt		 				    bigint 		        NULL,
        vhcty_asort_nm              nvarchar(50)        NOT NULL    DEFAULT '',
        vims_prpos_se_nm		 	nvarchar(50) 		NOT NULL    DEFAULT '',
        use_strnghld_area1          nvarchar(50)        NOT NULL    DEFAULT '',
        use_strnghld_area2          nvarchar(50)        NOT NULL    DEFAULT '',
        db_update_time				datetime			NOT NULL,
        PRIMARY KEY CLUSTERED 
        (
            day_hour_part		ASC,
            vhcty_asort_nm 		ASC,
            vims_prpos_se_nm    ASC,
            use_strnghld_area1  ASC,
            use_strnghld_area2  ASC
        )
    ) ;
'''


# CREATE TABLE -> dms_plpr_data_part
#############################################################################
q_dms_plpr_data_part = '''
    IF NOT EXISTS
        (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME='{table}')
    CREATE TABLE {schema}.{table} (
        day_hour_part               date                NOT NULL,
        cctv_id                     varchar(50)         NOT NULL,
        cctv_name                   nvarchar(255)       NULL,
        longitude                   varchar(32)         NULL,
        latitude                    varchar(32)         NULL,
        hjd_name                    nvarchar(32)        NULL,
        arrear_type                 nvarchar(40)        NOT NULL,
        cnt                         int                 NULL,
        arrear_count_sum            bigint              NULL,
        arrear_sum                  bigint              NULL,
        arrear_min                  bigint              NULL,
        arrear_max                  bigint              NULL,
        db_update_time              datetime            NULL,
        PRIMARY KEY CLUSTERED
        (
            day_hour_part       ASC,
            cctv_id             ASC,
            arrear_type         ASC        
        )
    );
'''


# CREATE TABLE -> divas_water_flow
#############################################################################
q_divas_water_flow = '''
    IF NOT EXISTS
        (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME='{table}')
    CREATE TABLE {schema}.{table}(
        code        		 		VARCHAR(10)		NOT NULL,
        flow_date		 			DATETIME 		    NOT NULL,
        equipment_id        		BIGINT         		NOT NULL    DEFAULT 0,
        equipment_name              NVARCHAR(50)        NOT NULL    DEFAULT '',
        type                        VARCHAR(100)        NOT NULL    DEFAULT '',
        last_time                   DATETIME            NULL,
        value                       BIGINT              NULL        DEFAULT 0,
        realtime_flow_value         BIGINT              NULL,
        level1                      INT                 NULL,
        level2                      INT                 NULL,
        level3                      INT                 NULL,
        level4                      INT                 NULL,    
        address                     NVARCHAR(256)       NULL,                 
        db_update_time				datetime			NOT NULL,
        PRIMARY KEY CLUSTERED 
        (
            code		      ASC,
            flow_date 		  ASC
        )
    );
'''


# CREATE TABLE -> aruba_count_hourly
#############################################################################
q_aruba_count_hourly = '''
    IF NOT EXISTS
        (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME='{table}')
    CREATE TABLE {schema}.{table}(
        loc                                 varchar(50)   NOT NULL,
        cnt                                 int           NULL,
        dt_hour                             datetime      NOT NULL,
        db_update_time                      datetime      NULL,
        PRIMARY KEY CLUSTERED
        (
            loc ASC,
            dt_hour ASC
        )
    );
'''


# CREATE TABLE -> aruba_count_daily
#############################################################################
q_aruba_count_daily = '''
    IF NOT EXISTS
        (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME='{table}')
    CREATE TABLE {schema}.{table}(
        sublayer_id                         nvarchar(100) NOT NULL,
        id                                  varchar(52)   NOT NULL,
        cnt                                 int           NULL,
        start_time                          datetime      NULL,
        end_time                            datetime      NULL,
        avg_signal                          int           NULL,
        stay_time                           int           NULL,
        avg_interval_time                   int           NULL,
        stay_rate                           float         NULL,
        dt                                  varchar(10)   NOT NULL,
        db_update_time                      datetime      NULL,
        PRIMARY KEY CLUSTERED
        (
            sublayer_id ASC,
            id ASC,
            dt ASC
        )
    );
'''


# CREATE TABLE -> weather_atmo
q_weather_atmo = '''
    IF NOT EXISTS
        (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME='{table}')
    CREATE TABLE {schema}.{table}(
        slocal_code             varchar(10)     NOT NULL,
        atmo_date_kst           datetime        NOT NULL,
        btype                   varchar(1)      NULL,
        lavr                    int             NULL,
        lmin                    int             NULL,
        lmax                    int             NULL,
        brtu_state              varchar(1)      NULL,
        db_update_time_utc      datetime        NULL,
        PRIMARY KEY CLUSTERED
        (
            slocal_code ASC,
            atmo_date_kst DESC
        )
    );
'''


# CREATE TABLE -> weather_humi
q_weather_humi = '''
    IF NOT EXISTS
        (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME='{table}')
    CREATE TABLE {schema}.{table}(
        slocal_code             varchar(10)     NOT NULL,
        humi_date_kst           datetime        NOT NULL,
        btype                   varchar(1)      NULL,
        lavr                    int             NULL,
        lmin                    int             NULL,
        lmax                    int             NULL,
        brtu_state              varchar(1)      NULL,
        db_update_time_utc      datetime        NULL,
        PRIMARY KEY CLUSTERED
        (
            slocal_code ASC,
            humi_date_kst DESC
        )
    );
'''


# CREATE TABLE -> weather_rain
q_weather_rain = '''
    IF NOT EXISTS
        (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME='{table}')
    CREATE TABLE {schema}.{table}(
        slocal_code             varchar(10)     NOT NULL,
        rain_date_kst           datetime        NOT NULL,
        btype                   varchar(1)      NULL,
        lvalue                  int             NULL,
        bsensing                int             NULL,
        db_update_time_utc      datetime        NULL,
        PRIMARY KEY CLUSTERED
        (
            slocal_code ASC,
            rain_date_kst DESC
        )
    );
'''


# CREATE TABLE -> weather_rain
q_weather_temp = '''
    IF NOT EXISTS
        (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME='{table}')
    CREATE TABLE {schema}.{table}(
        slocal_code             varchar(10)     NOT NULL,
        temp_date_kst           datetime        NOT NULL,
        btype                   varchar(1)      NULL,
        lavr                    int             NULL,
        lmin                    int             NULL,
        lmax                    int             NULL,
        min_time                int             NULL,
        max_time                int             NULL,
        brtu_state              varchar(1)      NULL,
        db_update_time_utc      datetime        NULL,
        PRIMARY KEY CLUSTERED
        (
            slocal_code ASC,
            temp_date_kst DESC
        )
    );
'''

# CREATE TABLE -> weather_rain
q_weather_wind = '''
    IF NOT EXISTS
        (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME='{table}')
    CREATE TABLE {schema}.{table}(
        slocal_code             varchar(10)     NOT NULL,
        wind_date_kst           datetime        NOT NULL,
        btype                   varchar(1)      NULL,
        lavr_deg1               int             NULL,
        lavr_vel1               int             NULL,
        lavr_deg2               int             NULL,
        lavr_vel2               int             NULL,
        lmax_deg                int             NULL,
        lmax_vel                int             NULL,        
        max_vel_time            datetime        NULL,
        brtu_state              varchar(1)      NULL,
        db_update_time_utc      datetime        NULL,
        PRIMARY KEY CLUSTERED
        (
            slocal_code ASC,
            wind_date_kst DESC
        )
    );
'''


# CREATE TABLE -> weather_localinfo
#############################################################################
q_weather_localinfo = '''
    DROP TABLE IF EXISTS {schema}.{table};
    CREATE TABLE {schema}.{table}(
        slocal_code             varchar(10)     NOT NULL,
        slocal_name             nvarchar(12)    NULL,
        lsensor_type            int             NULL,
        lmodel_type             int             NULL,
        lline_type              int             NULL,
        bavr_type               int             NULL,
        gath_turm               int             NULL,   
        last_call_time_kst      datetime        NULL,
        db_update_time_utc      datetime        NULL,
        PRIMARY KEY CLUSTERED
        (
            slocal_code ASC
        )
    );
'''

# CREATE TABLE -> forest_sensor_list
#############################################################################
q_forest_sensor_list = '''
    DROP TABLE IF EXISTS {schema}.{table};
    CREATE TABLE {schema}.{table} (
        no 					int   				NOT NULL,
        device_type			varchar(1)			NULL,
        status				varchar(1)			NULL,
        longitude			varchar(20)			NULL,
        latitude			varchar(20)			NULL,
        voltage				int      			NULL,
        last_recp_time      datetime            NULL,
        db_update_time_utc  datetime            NULL,
        PRIMARY KEY (
            no
        )
    );
'''

# CREATE TABLE -> forest_tree_list
#############################################################################
q_forest_tree_list = '''
    DROP TABLE IF EXISTS {schema}.{table};
    CREATE TABLE {schema}.{table} (
        no 					int   				NOT NULL,
        status				varchar(1)			NULL,
        longitude			varchar(20)			NULL,
        latitude			varchar(20)			NULL,
        db_update_time_utc  datetime            NULL,
        PRIMARY KEY (
            no
        )
    );
'''

# CREATE TABLE -> forest_tree
#############################################################################
q_forest_tree = '''
    IF NOT EXISTS
        (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME='{table}')
    CREATE TABLE {schema}.{table} (
        no 					int   				NOT NULL,
        date 				date 				NOT NULL,
        hour 				int  				NOT NULL,
        temperature         float				NULL,
        humidity 			float  				NULL,
        [top] 				float  				NULL,
        middle              float  				NULL,
        bottom				float  				NULL,
        soil 				float  				NULL,
        voltage 			float  				NULL,
        db_update_time_utc  datetime            NULL,
        PRIMARY KEY (
            no ASC,
            date DESC,
            hour DESC
        )
    );
'''

# CREATE TABLE -> forest_sensor
#############################################################################
q_forest_sensor = '''
    IF NOT EXISTS
        (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME='{table}')
    CREATE TABLE {schema}.{table} (
        no 					int   				NOT NULL,
        date 				date 				NOT NULL,
        hour 				int  				NOT NULL,
        temperature         float				NULL,
        humidity 			float  				NULL,
        [top] 				float  				NULL,
        middle              float  				NULL,
        bottom				float  				NULL,
        soil 				float  				NULL,
        voltage 			float  				NULL,
        db_update_time_utc  datetime            NULL,
        PRIMARY KEY (
            no ASC,
            date DESC,
            hour DESC
        )
    );
'''
