-- настроим сжатие данных

ALTER TABLE container_stats
    SET (timescaledb.compress,
	         timescaledb.compress_orderby='time',
		         timescaledb.compress_segmentby = 'container_id');

ALTER TABLE container_detailed_statistics
    SET (timescaledb.compress,
	         timescaledb.compress_orderby='time',
		         timescaledb.compress_segmentby = 'id');

ALTER TABLE container_networks
    SET (timescaledb.compress,
	         timescaledb.compress_orderby='time',
		         timescaledb.compress_segmentby = 'id');
