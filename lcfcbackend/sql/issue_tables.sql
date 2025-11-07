-- Issue管理相关表结构SQL脚本

-- Issue主表
CREATE TABLE `issue_main` (
    `issue_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT 'Issue ID',
    `issue_number` VARCHAR(32) NOT NULL COMMENT 'Issue编号(如ISU-2023-1542)',
    `title` VARCHAR(200) NOT NULL COMMENT 'Issue标题',
    `priority` VARCHAR(10) NOT NULL DEFAULT 'low' COMMENT '优先级(high,medium,low)',
    `status` VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '状态(pending待诊断,diagnosing诊断中,completed已完成,cancelled已取消)',
    `issue_type` VARCHAR(50) NOT NULL COMMENT 'Issue类型(BUG,工单,系统日志,测试报告等)',
    `issue_source` VARCHAR(100) DEFAULT NULL COMMENT 'Issue来源',
    `description` TEXT COMMENT '问题描述',
    `solution` TEXT COMMENT '解决方案',
    `expected_resolve_date` DATETIME COMMENT '预期解决日期',
    `create_by` VARCHAR(64) DEFAULT '' COMMENT '创建者',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_by` VARCHAR(64) DEFAULT '' COMMENT '更新者',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `del_flag` VARCHAR(1) DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
    PRIMARY KEY (`issue_id`),
    UNIQUE KEY `uk_issue_number` (`issue_number`),
    KEY `idx_priority` (`priority`),
    KEY `idx_status` (`status`),
    KEY `idx_create_time` (`create_time`),
    KEY `idx_issue_type` (`issue_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Issue主表';

-- Issue系统环境表
CREATE TABLE `issue_system_env` (
    `env_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '环境ID',
    `issue_id` BIGINT NOT NULL COMMENT 'Issue ID',
    `cpu_info` VARCHAR(200) COMMENT 'CPU信息',
    `memory_info` VARCHAR(200) COMMENT '内存信息',
    `gpu_info` VARCHAR(200) COMMENT '显卡信息',
    `os_info` VARCHAR(200) COMMENT '操作系统信息',
    `gpu_driver_version` VARCHAR(100) COMMENT '显卡驱动版本',
    `bios_version` VARCHAR(100) COMMENT 'BIOS版本',
    PRIMARY KEY (`env_id`),
    KEY `idx_issue_id` (`issue_id`),
    CONSTRAINT `fk_system_env_issue` FOREIGN KEY (`issue_id`) REFERENCES `issue_main` (`issue_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Issue系统环境表';

-- Issue诊断记录表
CREATE TABLE `issue_diagnosis_log` (
    `log_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '记录ID',
    `issue_id` BIGINT NOT NULL COMMENT 'Issue ID',
    `step_name` VARCHAR(200) NOT NULL COMMENT '诊断步骤名称',
    `method_description` TEXT COMMENT '具体诊断方法',
    `operator` VARCHAR(64) NOT NULL COMMENT '操作人',
    `operate_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
    PRIMARY KEY (`log_id`),
    KEY `idx_issue_id` (`issue_id`),
    KEY `idx_operate_time` (`operate_time`),
    CONSTRAINT `fk_diagnosis_log_issue` FOREIGN KEY (`issue_id`) REFERENCES `issue_main` (`issue_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Issue诊断记录表';

-- Issue附件表
CREATE TABLE `issue_attachment` (
    `attachment_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '附件ID',
    `issue_id` BIGINT NOT NULL COMMENT 'Issue ID',
    `file_name` VARCHAR(255) NOT NULL COMMENT '文件名',
    `file_path` VARCHAR(500) NOT NULL COMMENT '文件路径',
    `file_size` BIGINT COMMENT '文件大小(字节)',
    `file_type` VARCHAR(50) COMMENT '文件类型',
    `upload_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',
    `upload_by` VARCHAR(64) COMMENT '上传者',
    PRIMARY KEY (`attachment_id`),
    KEY `idx_issue_id` (`issue_id`),
    KEY `idx_upload_time` (`upload_time`),
    CONSTRAINT `fk_attachment_issue` FOREIGN KEY (`issue_id`) REFERENCES `issue_main` (`issue_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Issue附件表';

-- Issue标签表
CREATE TABLE `issue_tag` (
    `tag_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '标签ID',
    `issue_id` BIGINT NOT NULL COMMENT 'Issue ID',
    `tag_name` VARCHAR(50) NOT NULL COMMENT '标签名称',
    PRIMARY KEY (`tag_id`),
    KEY `idx_issue_id` (`issue_id`),
    KEY `idx_tag_name` (`tag_name`),
    CONSTRAINT `fk_tag_issue` FOREIGN KEY (`issue_id`) REFERENCES `issue_main` (`issue_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Issue标签表';

-- 插入一些示例数据（可选）
INSERT INTO `issue_main` (`issue_number`, `title`, `priority`, `status`, `issue_type`, `issue_source`, `description`, `create_by`) VALUES
('ISU-2023-12-21-0001', 'Windows 11蓝屏问题', 'high', 'pending', 'BUG', 'WinDBG', '系统在启动软件时出现蓝屏，错误代码为SYSTEM_SERVICE_EXCEPTION (0x0000003b)', 'admin'),
('ISU-2023-12-21-0002', '系统蓝屏BSOD错误', 'medium', 'diagnosing', '工单', '用户反馈', '发现第三方硬件驱动异与Windows 11系统不兼容，导致系统在使用特定API时发生冲突', 'admin'),
('ISU-2023-12-21-0003', '网络连接异常', 'low', 'completed', '系统日志', '自动检测', '确认网络出现NVIDIA驱动导致系统冲突，在特定条件下会导致系统内存管理错误', 'admin');

-- 插入系统环境示例数据
INSERT INTO `issue_system_env` (`issue_id`, `cpu_info`, `memory_info`, `gpu_info`, `os_info`, `gpu_driver_version`, `bios_version`) VALUES
(1, 'Intel Core i7-11800H @ 2.30GHz', '16GB DDR4', 'NVIDIA GeForce RTX 3060 Laptop GPU', 'Windows 11 专业版 21H2', 'NVIDIA 517.9', 'American Megatrends Inc. 1.07'),
(2, 'Intel Core i7-11800H @ 2.30GHz', '16GB DDR4', 'NVIDIA GeForce RTX 3060 Laptop GPU', 'Windows 11 专业版 21H2', 'NVIDIA 517.9', 'American Megatrends Inc. 1.07'),
(3, 'Intel Core i7-11800H @ 2.30GHz', '16GB DDR4', 'NVIDIA GeForce RTX 3060 Laptop GPU', 'Windows 11 专业版 21H2', 'NVIDIA 517.9', 'American Megatrends Inc. 1.07');

-- 插入诊断记录示例数据
INSERT INTO `issue_diagnosis_log` (`issue_id`, `step_name`, `method_description`, `operator`) VALUES
(1, '蓝屏日志收集', '使用WinDBG分析dump文件，查看点位内存地址ntoskrnl.exe中', 'admin'),
(2, '驱动兼容性检测', '发现第三方硬件驱动异与Windows 11系统不兼容，导致系统在使用特定API时发生冲突', 'admin'),
(3, '网络配置', '确认网络出现NVIDIA驱动导致系统冲突，在特定条件下会导致系统内存管理错误', 'admin');

-- 插入标签示例数据
INSERT INTO `issue_tag` (`issue_id`, `tag_name`) VALUES
(1, 'windows'), (1, '蓝屏'), (1, '网络'),
(2, 'windows'), (2, '蓝屏'), 
(3, 'windows'), (3, '网络');
