-- ========================================
-- Issue附件表结构调整 - 支持临时附件
-- ========================================
-- 说明：
-- 1. 将issue_id改为可空，支持上传临时附件
-- 2. 添加status字段标记附件状态（临时/已关联）
-- 3. 移除issue_id的外键约束，重新添加可空的外键约束
-- ========================================

-- 1. 删除原有的外键约束
ALTER TABLE `issue_attachment` DROP FOREIGN KEY `fk_attachment_issue`;

-- 2. 修改issue_id字段为可空
ALTER TABLE `issue_attachment` 
MODIFY COLUMN `issue_id` BIGINT NULL COMMENT 'Issue ID';

-- 3. 添加status字段
ALTER TABLE `issue_attachment` 
ADD COLUMN `status` VARCHAR(20) NOT NULL DEFAULT 'temporary' 
COMMENT '附件状态(temporary临时,linked已关联)' 
AFTER `upload_by`;

-- 4. 重新添加外键约束（允许NULL）
ALTER TABLE `issue_attachment` 
ADD CONSTRAINT `fk_attachment_issue` 
FOREIGN KEY (`issue_id`) 
REFERENCES `issue_main` (`issue_id`) 
ON DELETE CASCADE;

-- 5. 为已存在的附件数据设置状态为已关联
UPDATE `issue_attachment` 
SET `status` = 'linked' 
WHERE `issue_id` IS NOT NULL;

-- 6. 添加索引以提高查询性能
CREATE INDEX `idx_attachment_status` ON `issue_attachment` (`status`);
CREATE INDEX `idx_attachment_upload_time_status` ON `issue_attachment` (`upload_time`, `status`);

-- ========================================
-- 定时任务配置（可选）
-- ========================================
-- 添加清理临时附件的定时任务（每天凌晨2点执行）
-- 注意：需要根据实际情况调整任务ID，避免冲突

INSERT INTO `sys_job` (
    `job_id`,
    `job_name`,
    `job_group`,
    `job_executor`,
    `invoke_target`,
    `job_args`,
    `job_kwargs`,
    `cron_expression`,
    `misfire_policy`,
    `concurrent`,
    `status`,
    `create_by`,
    `create_time`,
    `remark`
) VALUES (
    100,
    '清理临时附件',
    'default',
    'default',
    'module_task.clean_temporary_attachments.clean_temporary_attachments',
    NULL,
    NULL,
    '0 0 2 * * ?',  -- 每天凌晨2点执行
    '3',  -- 计划执行错误策略：放弃执行
    '1',  -- 禁止并发执行
    '1',  -- 状态：暂停（需要手动启用）
    'admin',
    NOW(),
    '自动清理超过24小时未关联的临时附件'
);

-- ========================================
-- 回滚脚本（如果需要回退）
-- ========================================
/*
-- 删除定时任务
DELETE FROM `sys_job` WHERE `job_id` = 100;

-- 删除索引
DROP INDEX `idx_attachment_status` ON `issue_attachment`;
DROP INDEX `idx_attachment_upload_time_status` ON `issue_attachment`;

-- 删除status字段
ALTER TABLE `issue_attachment` DROP COLUMN `status`;

-- 删除外键约束
ALTER TABLE `issue_attachment` DROP FOREIGN KEY `fk_attachment_issue`;

-- 恢复issue_id为非空
UPDATE `issue_attachment` SET `issue_id` = 0 WHERE `issue_id` IS NULL;
ALTER TABLE `issue_attachment` 
MODIFY COLUMN `issue_id` BIGINT NOT NULL COMMENT 'Issue ID';

-- 重新添加外键约束
ALTER TABLE `issue_attachment` 
ADD CONSTRAINT `fk_attachment_issue` 
FOREIGN KEY (`issue_id`) 
REFERENCES `issue_main` (`issue_id`) 
ON DELETE CASCADE;
*/

