# Anna(DMS-BI) SQL

# Target > TABLE
# CONT   > CHECK EXISTS TABLE
#############################################################################
q_is_table = '''
    SELECT *
    FROM INFORMATION_SCHEMA.tables WITH(NOLOCK)
    WHERE TABLE_SCHEMA = '{schema}'
    AND TABLE_NAME = '{table}'
'''

# Target > TABLE
# CONT   > DROP TABLE
#############################################################################
q_drop_table = '''
    DROP TABLE IF EXISTS {schema}.{table}
'''

# Target > VURIXDMS > yeongcheon01
# CREATE TABLE -> dms_plpr_data_part
#############################################################################
q_dms_plpr_data_part = '''
    CREATE TABLE {schema}.{table}(
        day_hour_part               date                NOT NULL,
        cctv_id                     varchar(50)         NOT NULL,
        cctv_name                   nvarchar(255)       NULL,
        longitude                   varchar(32)         NULL,
        latitude                    varchar(32)         NULL,
        hjd_name                    nvarchar(32)        NOT NULL,
        arrear_type                 nvarchar(40)        NOT NULL,
        cnt                         int                 NULL,
        arrear_count_sum            bigint              NULL,
        arrear_sum                  bigint              NULL,
        arrear_min                  bigint              NULL,
        arrear_max                  bigint              NULL,
        --direction                   nvarchar(12)        NULL,
        db_update_time              datetime            NOT NULL,
        PRIMARY KEY CLUSTERED 
        (
            day_hour_part       ASC,
            cctv_id             ASC,
            arrear_type         ASC        )
    ) ;
'''



# Target > VURIXDMS > miryang01
# CREATE TABLE -> dms_lpr_data_part
#############################################################################
q_dms_lpr_data_part_miryang = '''
    CREATE TABLE {schema}.{table}(
        day_hour_part		 		date		 		NOT NULL,
        cnt		 				    bigint 		        NULL,
        vhcty_asort_nm              nvarchar(50)        NOT NULL    DEFAULT '',
        vims_prpos_se_nm		 	nvarchar(50) 		NOT NULL    DEFAULT '',
        use_strnghld_area1          nvarchar(50)        NOT NULL    DEFAULT '',
        use_strnghld_area2          nvarchar(50)        NOT NULL    DEFAULT '',
        use_strnghld_area3          nvarchar(100)       NOT NULL    DEFAULT '',
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

# Target > VURIXDMS > yeoncheon01
# CREATE TABLE -> dms_lpr_data_part
#############################################################################
q_dms_lpr_data_part_yeoncheon = '''
    CREATE TABLE {schema}.{table}(
        cctv_id                     varchar(50)         NOT NULL, 
        day_hour_part		 		date		 		NOT NULL,
        cnt		 				    bigint 		        NULL,
        vhcty_asort_nm              nvarchar(50)        NOT NULL    DEFAULT '',
        vims_prpos_se_nm		 	nvarchar(50) 		NOT NULL    DEFAULT '',
        use_strnghld_area1          nvarchar(50)        NOT NULL    DEFAULT '',
        use_strnghld_area2          nvarchar(50)        NOT NULL    DEFAULT '',
        use_strnghld_area3          nvarchar(100)       NOT NULL    DEFAULT '',
        use_strnghld_area4          nvarchar(100)       NOT NULL    DEFAULT '',
        db_update_time				datetime			NOT NULL,
        PRIMARY KEY CLUSTERED 
        (
            cctv_id             ASC,
            day_hour_part		ASC,
            vhcty_asort_nm 		ASC,
            vims_prpos_se_nm    ASC,
            use_strnghld_area1  ASC,
            use_strnghld_area2  ASC,
            use_strnghld_area3  ASC,
            use_strnghld_area4  ASC
        )
    ) ;
'''

# Target > VMS
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


# Target > VMS
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

# Target > VMS
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

# Target > VMS
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

# Target > VMS
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

# Target > VMS
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

# Target > VMS
# CREATE TABLE -> vms_vfs_fail_history
#############################################################################
q_vms_vfs_fail_history = '''
    DROP TABLE IF EXISTS  {schema}.{table};
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

# Target > VMS
# CREATE TABLE -> vms_vfs_history
#############################################################################
q_vms_vfs_history = '''
    DROP TABLE IF EXISTS {schema}.{table};
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

# Target > VMS
# CREATE TABLE -> vms_user_log
#############################################################################
q_vms_user_log = '''
    DROP TABLE IF EXISTS {schema}.{table};
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
        ins_time                                    DATETIME         NOT NULL,
        db_update_time                              DATETIME         NOT NULL,
        PRIMARY KEY CLUSTERED
        (
            log_id ASC,
            ins_time ASC
        )
    );
'''

class VmsUserLog():
    __table_name__ = ''
    
# Target > VMS
# CREATE TABLE -> vms_server_status
#############################################################################
q_vms_server_status = '''
    DROP TABLE IF EXISTS {schema}.{table};
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

# Target > DIVAS
# CREATE TABLE -> divas_water_flow
#############################################################################
q_divas_water_flow = '''
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

# Target > ARUBA
# CREATE TABLE -> aruba_count_daily
#############################################################################
q_aruba_count_daily = '''
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
            dt DESC
        )
    );
'''

# Target > ARUBA
# CREATE TABLE -> aruba_count_hourly
#############################################################################
q_aruba_count_hourly = '''
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

# Target > ARUBA
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

# Target > VIDEOTRANSFER
# CREATE TABLE -> videotransfer_csafer
#############################################################################
q_videotransfer_csafer = '''
    DROP TABLE IF EXISTS {schema}.{table};
    CREATE TABLE {schema}.{table} (
		request_id			 	nvarchar(20) 		NOT NULL,
		child_request_id		nvarchar(20) 		NULL,
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
		longitude			 	nvarchar(20) 		NULL,
		latitude			 	nvarchar(20) 		NULL,
		db_update_time 			datetime			NULL,

        PRIMARY KEY CLUSTERED
        (
			request_id 		ASC,
			request_date 	ASC
        )
    ) 
'''
