-- Создаем первичный ключ в основной таблице
ALTER TABLE container_info ADD CONSTRAINT container_id PRIMARY KEY (id);

-- Добавляем внешние ключи на основную таблицу
ALTER TABLE container_detailed_statistics
    ADD CONSTRAINT container_id FOREIGN KEY (id) REFERENCES container_info(id) ON DELETE CASCADE;

ALTER TABLE container_networks
    ADD CONSTRAINT container_id FOREIGN KEY (id) REFERENCES container_info(id) ON DELETE CASCADE;

ALTER TABLE container_stats
    ADD CONSTRAINT container_id FOREIGN KEY (container_id) REFERENCE container_info(id ) ON DELETE CASCADE;
