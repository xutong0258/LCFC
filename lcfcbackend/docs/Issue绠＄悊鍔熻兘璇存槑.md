# Issue 管理功能实现说明

## 功能概述

Issue 管理系统是一个完整的问题跟踪和诊断管理模块，支持 Issue 的全生命周期管理，包括创建、编辑、删除、状态跟踪、诊断记录、附件上传等功能。

## 技术架构

采用经典的三层架构模式：

```
Controller层 -> Service层 -> DAO层 -> 数据库
```

## 数据库设计

### 主要表结构

1. **issue_main**: Issue 主表，存储 Issue 基本信息
2. **issue_system_env**: 系统环境信息表
3. **issue_diagnosis_log**: 诊断记录表
4. **issue_attachment**: 附件表
5. **issue_tag**: 标签表

### 关键设计要点

- 使用`del_flag`字段实现软删除(`'0'`存在，`'2'`删除)
- 遵循项目统一的字段命名和类型规范
- 外键约束确保数据一致性
- 合理的索引设计优化查询性能

## API 接口

### 统计接口

- `GET /system/issue/statistics` - 获取 Issue 统计数据

### 基础 CRUD

- `GET /system/issue/list` - 获取 Issue 列表（分页）
- `POST /system/issue/list` - 获取 Issue 列表（POST 方式）
- `GET /system/issue/{issue_id}` - 获取 Issue 详情
- `POST /system/issue` - 新增 Issue
- `PUT /system/issue` - 编辑 Issue
- `DELETE /system/issue/{issue_ids}` - 删除 Issue

### 扩展功能

- `POST /system/issue/diagnosis/log` - 新增诊断记录
- `POST /system/issue/attachment/upload` - 上传附件
- `DELETE /system/issue/attachment/{attachment_id}` - 删除附件
- `PATCH /system/issue/{issue_id}/status` - 更新 Issue 状态

### 辅助接口

- `GET /system/issue/options/types` - 获取 Issue 类型选项
- `GET /system/issue/options/priorities` - 获取优先级选项
- `GET /system/issue/options/status` - 获取状态选项
- `GET /system/issue/export` - 导出 Issue 列表

## 主要功能特性

### 1. Issue 生命周期管理

- **待诊断** -> **诊断中** -> **已完成** / **已取消**
- 支持状态自动更新（添加诊断记录时自动从"待诊断"变为"诊断中"）

### 2. 系统环境信息管理

- CPU、内存、显卡信息记录
- 操作系统、驱动版本、BIOS 版本记录

### 3. 诊断记录跟踪

- 支持多步骤诊断记录
- 记录操作人、操作时间、具体方法

### 4. 附件管理

- 支持多种文件格式（.jpg、.pdf、.zip、.dmp、.log 等）
- 文件大小限制 100MB
- 安全的文件上传机制

### 5. 标签系统

- 支持多标签分类
- 便于 Issue 分类和检索

### 6. 统计功能

- Issue 总数统计
- 本月新增 Issue 数量
- 待处理 Issue 数量
- 诊断次数统计
- 高优先级 Issue 数量
- 已完成 Issue 数量

## 权限控制

所有接口都需要登录认证，并通过`CheckUserInterfaceAuth`装饰器进行权限控制：

- `system:issue:list` - 查看 Issue 列表权限
- `system:issue:query` - 查看 Issue 详情权限
- `system:issue:add` - 新增 Issue 权限
- `system:issue:edit` - 编辑 Issue 权限
- `system:issue:remove` - 删除 Issue 权限
- `system:issue:export` - 导出 Issue 权限

## 日志记录

使用`@Log`装饰器记录关键操作：

- 新增 Issue: `BusinessType.INSERT`
- 编辑 Issue: `BusinessType.UPDATE`
- 删除 Issue: `BusinessType.DELETE`

## 文件结构

```
module_admin/
├── entity/
│   ├── do/
│   │   └── issue_do.py          # 数据库实体类
│   └── vo/
│       └── issue_vo.py          # Pydantic模型类
├── dao/
│   └── issue_dao.py             # 数据访问层
├── service/
│   └── issue_service.py         # 业务逻辑层
└── controller/
    └── issue_controller.py      # 控制器层

sql/
└── issue_tables.sql             # 数据库表结构SQL

docs/
└── Issue管理功能说明.md         # 本文档
```

## 使用说明

### 1. 数据库初始化

执行`sql/issue_tables.sql`中的 SQL 语句创建相关表结构。

### 2. 启动服务

确保在`server.py`中已注册 Issue 模块路由：

```python
app.include_router(router=issue_controller.issueController, tags=["Issue管理模块"])
```

### 3. 接口调用

所有接口都需要在请求头中包含有效的认证 token。

### 4. 文件上传配置

确保`config/env.py`中配置了正确的上传路径：

```python
issue_path = 'vf_admin/upload_path/issues'
```

## 扩展建议

1. **通知机制**: 可以添加 Issue 状态变更通知
2. **工作流**: 可以扩展更复杂的状态流转规则
3. **报表功能**: 可以增加更丰富的统计报表
4. **API 集成**: 可以与外部系统集成，自动创建 Issue
5. **搜索优化**: 可以添加全文搜索功能
6. **版本控制**: 可以添加 Issue 变更历史记录

## 注意事项

1. 文件上传时需要进行安全校验
2. Issue 编号采用日期+序号的方式自动生成
3. 删除操作为软删除，不会真正删除数据
4. 所有操作都有事务支持，确保数据一致性
5. 需要定期清理无效的附件文件
