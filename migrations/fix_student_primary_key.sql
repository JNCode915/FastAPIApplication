-- SQLAlchemy's create_all() does not modify an existing table.
-- Run this once if Student.id was created without AUTO_INCREMENT.
ALTER TABLE `Student`
    MODIFY COLUMN `id` INT NOT NULL AUTO_INCREMENT;
