# Pydantic V2 学习指南

欢迎来到 Pydantic V2 一天速成学习计划！🎉

## 📚 学习路径

本指南包含 8 个循序渐进的学习模块，每个模块都有详细的代码示例和说明。

### 学习顺序

| 序号 | 文件 | 主题 | 时间 | 重点内容 |
|------|------|------|------|----------|
| 1 | `01_basics.py` | V2 基础 | 1小时 | 核心方法、V1/V2对比 |
| 2 | `02_field_constraints.py` | Field 约束 | 1.5小时 | 数值、字符串约束 |
| 3 | `03_validators.py` | 自定义验证器 | 1小时 | field_validator、model_validator |
| 4 | `04_nested_models.py` | 嵌套模型 | 1.5小时 | 复杂类型、嵌套关系 |
| 5 | `05_model_config.py` | Model Config | 1小时 | ConfigDict 配置 |
| 6 | `06_aliases_serialization.py` | 别名和序列化 | 1小时 | alias、序列化控制 |
| 7 | `07_practical.py` | 实战练习 | 1小时 | 真实场景应用 |
| 8 | `08_common_mistakes.py` | 常见错误 | 0.5小时 | 易错点对比 |

**总计：约 8.5 小时**

## 🚀 快速开始

### 1. 环境准备

```bash
# Python 3.8+
python --version

# 安装 Pydantic V2
pip install pydantic
# 或使用 uv
uv pip install pydantic
```

### 2. 运行示例

每个文件都可以独立运行：

```bash
# 从基础开始
python learning/01_basics.py

# 或按顺序学习
python learning/02_field_constraints.py
python learning/03_validators.py
# ... 依此类推
```

### 3. 学习建议

1. **按顺序学习** - 后面的章节依赖前面的知识
2. **动手实践** - 修改代码，尝试不同的参数
3. **查看输出** - 每个示例都有详细的打印输出
4. **做笔记** - 记录易错点和重点内容
5. **完成练习** - 第 7 章有完整的实战案例

## 📖 学习大纲

### 上午部分（4.5小时）

#### ✅ 第一阶段：V2 基础（1小时）
- Pydantic V2 核心概念
- 基础模型定义
- V2 核心方法：
  - `model_validate()` - 从字典创建
  - `model_validate_json()` - 从 JSON 创建
  - `model_dump()` - 转换为字典
  - `model_dump_json()` - 转换为 JSON
  - `model_copy()` - 复制模型
- V1 vs V2 对比

#### ✅ 第二阶段：Field 约束（1.5小时）
- 数值约束：`gt`, `ge`, `lt`, `le`
- 字符串约束：`min_length`, `max_length`, `pattern`
- 特殊类型：`EmailStr`, `HttpUrl`
- 集合约束
- Field 参数完整说明

#### ✅ 第三阶段：自定义验证器（1小时）
- `@field_validator` - 单字段验证
- `@model_validator` - 跨字段验证
- `mode='before'` vs `mode='after'`
- 复杂验证逻辑实现

### 下午部分（4小时）

#### ✅ 第四阶段：嵌套模型（1.5小时）
- 基础嵌套模型
- `List[T]`, `Dict[K, V]`, `Set[T]`, `Tuple[...]`
- `Optional[T]`, `Union[T1, T2]`
- 深度嵌套示例
- 可变默认值处理

#### ✅ 第五阶段：Model Config（1小时）
- V2 配置语法：`model_config = ConfigDict(...)`
- 常用配置：
  - `str_strip_whitespace` - 去除空格
  - `validate_assignment` - 赋值验证
  - `frozen` - 不可变模型
  - `extra` - 额外字段处理
  - `from_attributes` - ORM 支持
  - `populate_by_name` - 别名配置

#### ✅ 第六阶段：别名和序列化（1小时）
- `alias` - 输入别名
- `serialization_alias` - 输出别名
- 序列化控制：`include`, `exclude`
- 序列化过滤：`exclude_none`, `exclude_unset`
- `@field_serializer` - 自定义序列化
- `by_alias` 参数

#### ✅ 第七阶段：实战练习（1小时）
- 用户认证系统
- 电商商品管理
- API 分页响应
- 应用配置管理

### 复习部分（0.5小时）

#### ✅ 第八阶段：常见错误（0.5小时）
- V1 vs V2 方法名错误
- Field 参数错误
- 验证器常见错误
- 配置语法错误
- 类型使用错误
- 错误汇总表

## 🎯 核心知识点

### V2 核心变化

```python
# V1 → V2 方法对照表
dict()              → model_dump()
json()              → model_dump_json()
parse_obj()         → model_validate()
parse_raw()         → model_validate_json()
copy()              → model_copy()
schema()            → model_json_schema()

# V1 → V2 配置对照
class Config:       → model_config = ConfigDict()
orm_mode            → from_attributes

# V1 → V2 验证器对照
@validator          → @field_validator
@root_validator     → @model_validator
```

### 必须掌握的概念

1. **Field 约束**
   - 数值：`gt`, `ge`, `lt`, `le`
   - 字符串：`min_length`, `max_length`, `pattern`
   - 默认值：`default`, `default_factory`

2. **验证器**
   - `@field_validator` + `@classmethod`
   - `@model_validator(mode='after')`
   - 必须返回值

3. **配置**
   - `model_config = ConfigDict(...)`
   - 常用配置记住 5 个
   - V1 vs V2 对照

4. **序列化**
   - `model_dump()` - Python 字典
   - `model_dump_json()` - JSON 字符串
   - `include`/`exclude` - 字段控制
   - `by_alias` - 使用别名

## 💡 学习技巧

### 记忆口诀

1. **V2 方法有前缀**
   ```
   model_ 前缀不能忘
   validate、dump、copy 常用上
   ```

2. **验证器三要素**
   ```
   field_validator 装饰上
   classmethod 不能忘
   return 返回值必须有
   ```

3. **边界值记忆**
   ```
   gt/lt 不包含
   ge/le 要包含
   ```

4. **可变默认值**
   ```
   列表字典不直接赋
   default_factory 来帮助
   ```

### 易错点清单

- [ ] 使用 V1 方法名（`dict()`, `parse_obj()`）
- [ ] Field 参数不用关键字（`Field("value")`）
- [ ] 验证器忘记 `@classmethod`
- [ ] 验证器忘记 `return`
- [ ] 可变默认值直接赋值（`tags: List[str] = []`）
- [ ] 使用 `class Config:` 而不是 `model_config`
- [ ] 混淆 `gt`/`ge`、`lt`/`le`
- [ ] `Optional[T]` 不设置默认值
- [ ] 混淆 `alias` 和 `serialization_alias`

## 📝 实战检查清单

完成学习后，你应该能够：

- [ ] 熟练使用 V2 的核心方法
- [ ] 正确使用 Field 约束
- [ ] 编写自定义验证器
- [ ] 处理嵌套模型和复杂类型
- [ ] 配置模型行为
- [ ] 控制序列化输出
- [ ] 构建真实项目的数据模型
- [ ] 避免常见错误

## 🔗 延伸学习

完成本教程后，建议学习：

1. **与 FastAPI 集成**
   - 请求验证
   - 响应模型
   - 依赖注入

2. **与 ORM 集成**
   - SQLAlchemy
   - Tortoise ORM
   - Beanie (MongoDB)

3. **高级特性**
   - 泛型模型
   - 插件系统
   - 自定义类型
   - JSON Schema 生成

4. **性能优化**
   - 延迟验证
   - 缓存策略
   - 序列化性能

## 📚 参考资源

- [Pydantic V2 官方文档](https://docs.pydantic.dev/latest/)
- [迁移指南](https://docs.pydantic.dev/latest/migration/)
- [GitHub 仓库](https://github.com/pydantic/pydantic)

## 🤝 学习建议

1. **不要跳章节** - 知识点是递进的
2. **多动手实践** - 修改示例代码，尝试不同参数
3. **理解而非死记** - 理解原理比记忆 API 更重要
4. **做好笔记** - 记录自己的理解和易错点
5. **实践应用** - 在自己的项目中使用 Pydantic

## ❓ 常见问题

### Q: 需要先学习 V1 吗？
**A:** 不需要！直接学习 V2 即可。本教程会标注 V1/V2 的区别。

### Q: Python 版本要求？
**A:** Pydantic V2 需要 Python 3.8+，推荐 Python 3.10+。

### Q: 学完需要多久？
**A:** 建议用一整天（8-10小时）完整学习，包括实践和练习。

### Q: 如何检验学习效果？
**A:** 完成第 7 章的实战练习，并尝试在自己的项目中应用。

### Q: 遇到错误怎么办？
**A:** 
1. 查看第 8 章的常见错误对比
2. 检查是否使用了 V1 的语法
3. 仔细阅读错误信息
4. 查阅官方文档

---

**祝学习愉快！🎓**

如有问题或建议，欢迎提出 Issue 或 PR。

