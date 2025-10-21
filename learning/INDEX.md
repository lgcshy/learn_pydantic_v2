# 📑 学习资源索引

## 🎯 根据需求快速定位

### 我是新手，从哪里开始？
→ **[00_START_HERE.md](00_START_HERE.md)** - 5分钟快速上手

### 我想系统学习
→ **[README_LEARNING.md](README_LEARNING.md)** - 完整学习指南（8.5小时）

### 我需要快速查询语法
→ **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - 速查表

### 我想看项目概览
→ **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - 项目总结

### 我想知道某个功能怎么用
→ 查看下方的功能索引

---

## 🔍 按功能查找

### 基础操作

| 功能 | 文件 | 位置 |
|------|------|------|
| 创建模型 | `01_basics.py` | 第1节 |
| 从字典创建 | `01_basics.py` | 第2.1节 |
| 从JSON创建 | `01_basics.py` | 第2.2节 |
| 转为字典 | `01_basics.py` | 第2.3节 |
| 转为JSON | `01_basics.py` | 第2.4节 |
| 复制模型 | `01_basics.py` | 第2.6节 |

### Field 约束

| 功能 | 文件 | 位置 |
|------|------|------|
| 数值约束 | `02_field_constraints.py` | 第1节 |
| 字符串约束 | `02_field_constraints.py` | 第2节 |
| 正则表达式 | `02_field_constraints.py` | 第2节 |
| 邮箱验证 | `02_field_constraints.py` | 第3节 |
| URL验证 | `02_field_constraints.py` | 第3节 |
| 集合约束 | `02_field_constraints.py` | 第4节 |

### 验证器

| 功能 | 文件 | 位置 |
|------|------|------|
| 字段验证器基础 | `03_validators.py` | 第1节 |
| 验证多个字段 | `03_validators.py` | 第2节 |
| 跨字段验证 | `03_validators.py` | 第3节 |
| before vs after | `03_validators.py` | 第4节 |
| 完整验证示例 | `03_validators.py` | 第5节 |

### 复杂类型

| 功能 | 文件 | 位置 |
|------|------|------|
| 嵌套模型 | `04_nested_models.py` | 第1节 |
| List 类型 | `04_nested_models.py` | 第2节 |
| Dict 类型 | `04_nested_models.py` | 第3节 |
| Set/Tuple | `04_nested_models.py` | 第4节 |
| Optional/Union | `04_nested_models.py` | 第5节 |
| 深度嵌套 | `04_nested_models.py` | 第6节 |
| 可变默认值 | `04_nested_models.py` | 第7节 |

### 配置

| 功能 | 文件 | 位置 |
|------|------|------|
| ConfigDict 语法 | `05_model_config.py` | 第1节 |
| 字符串处理 | `05_model_config.py` | 第2节 |
| 赋值验证 | `05_model_config.py` | 第3节 |
| 不可变模型 | `05_model_config.py` | 第4节 |
| 别名配置 | `05_model_config.py` | 第5节 |
| 额外字段 | `05_model_config.py` | 第6节 |
| ORM支持 | `05_model_config.py` | 第7节 |

### 序列化

| 功能 | 文件 | 位置 |
|------|------|------|
| 基础别名 | `06_aliases_serialization.py` | 第1节 |
| 双向别名 | `06_aliases_serialization.py` | 第2节 |
| 序列化别名 | `06_aliases_serialization.py` | 第3节 |
| include/exclude | `06_aliases_serialization.py` | 第4节 |
| 序列化过滤 | `06_aliases_serialization.py` | 第5节 |
| 自定义序列化 | `06_aliases_serialization.py` | 第6节 |
| 嵌套序列化 | `06_aliases_serialization.py` | 第7节 |

### 实战案例

| 案例 | 文件 | 位置 |
|------|------|------|
| 用户认证系统 | `07_practical.py` | 实战1 |
| 电商商品管理 | `07_practical.py` | 实战2 |
| API分页响应 | `07_practical.py` | 实战3 |
| 配置管理 | `07_practical.py` | 实战4 |

### 常见错误

| 错误类型 | 文件 | 位置 |
|---------|------|------|
| V1方法名 | `08_common_mistakes.py` | 错误1 |
| Field参数 | `08_common_mistakes.py` | 错误2 |
| 验证器装饰器 | `08_common_mistakes.py` | 错误3-5 |
| 可变默认值 | `08_common_mistakes.py` | 错误6 |
| Config语法 | `08_common_mistakes.py` | 错误7 |
| 约束混淆 | `08_common_mistakes.py` | 错误8 |
| 别名配置 | `08_common_mistakes.py` | 错误9-10 |
| 类型误用 | `08_common_mistakes.py` | 错误11-12 |

---

## 🔎 按问题查找

### "如何..."

| 问题 | 答案位置 |
|------|---------|
| 如何验证邮箱格式？ | `02_field_constraints.py` 第3节 |
| 如何验证两次密码一致？ | `03_validators.py` 第3节 |
| 如何处理嵌套的JSON？ | `04_nested_models.py` 第1、6节 |
| 如何让模型不可修改？ | `05_model_config.py` 第4节 |
| 如何排除敏感字段？ | `06_aliases_serialization.py` 第4节 |
| 如何支持驼峰命名？ | `06_aliases_serialization.py` 第3节 |

### "为什么..."

| 问题 | 答案位置 |
|------|---------|
| 为什么提示方法不存在？ | `08_common_mistakes.py` 错误1 |
| 为什么验证器不生效？ | `08_common_mistakes.py` 错误3-5 |
| 为什么列表被多个实例共享？ | `08_common_mistakes.py` 错误6 |
| 为什么别名不能用？ | `08_common_mistakes.py` 错误9 |
| 为什么 age 变成 None？ | `08_common_mistakes.py` 错误5 |

### "什么是..."

| 概念 | 解释位置 |
|------|---------|
| Field(...) 的三个点 | `02_field_constraints.py` 第5节 |
| gt 和 ge 的区别 | `02_field_constraints.py` 第1节 |
| mode='before' vs 'after' | `03_validators.py` 第4节 |
| alias vs serialization_alias | `06_aliases_serialization.py` 第2-3节 |
| Optional[T] 的含义 | `04_nested_models.py` 第5节 |

---

## 📱 按使用场景查找

### Web API 开发
1. `07_practical.py` - 实战1（用户认证）
2. `07_practical.py` - 实战3（分页响应）
3. `06_aliases_serialization.py` - 第10节（API格式化）

### 数据验证
1. `02_field_constraints.py` - 全部章节
2. `03_validators.py` - 第1-5节
3. `07_practical.py` - 实战1（用户注册验证）

### 配置管理
1. `05_model_config.py` - 全部章节
2. `07_practical.py` - 实战4（配置管理）

### ORM 集成
1. `05_model_config.py` - 第7节
2. `06_aliases_serialization.py` - 第9节

---

## 🎯 按学习阶段查找

### 第1天（入门）
- [ ] `00_START_HERE.md`
- [ ] `01_basics.py`
- [ ] `02_field_constraints.py`
- [ ] `QUICK_REFERENCE.md`

### 第2天（进阶）
- [ ] `03_validators.py`
- [ ] `04_nested_models.py`
- [ ] `05_model_config.py`

### 第3天（高级）
- [ ] `06_aliases_serialization.py`
- [ ] `07_practical.py`
- [ ] `08_common_mistakes.py`

---

## 🚀 快速命令

```bash
# 查看所有文件列表
ls -lh learning/

# 运行所有示例（按顺序）
for i in {1..8}; do python learning/0${i}_*.py; done

# 搜索特定内容
grep -r "model_dump" learning/*.py

# 统计代码行数
wc -l learning/*.py

# 查看文件大小
du -sh learning/*
```

---

## 📞 需要帮助？

1. **查看速查表**: `learning/QUICK_REFERENCE.md`
2. **查看常见错误**: `learning/08_common_mistakes.py`
3. **查看完整指南**: `learning/README_LEARNING.md`
4. **查阅官方文档**: https://docs.pydantic.dev

---

**提示**: 使用 `Ctrl+F` 在本页面快速搜索你需要的内容！

