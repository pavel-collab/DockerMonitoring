-- настроим автоматическую аггрегацию данных с помощью расширения timescaledb
ALTER TABLE container_statistics  
    SET (timescaledb.compress, 
         timescaledb.compress_orderby='time', 
         timescaledb.compress_segmentby = 'id');