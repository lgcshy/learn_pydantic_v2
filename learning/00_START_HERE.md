# 🚀 从这里开始！

欢迎来到 Pydantic V2 学习之旅！

## ⚡ 5分钟快速体验

```bash
# 1. 安装 Pydantic
pip install pydantic

# 2. 运行第一个示例
python learning/01_basics.py
```

## 📅 一天学习计划

### 上午（4.5小时）

**9:00 - 10:00** → `01_basics.py`  
学习 V2 核心方法，理解与 V1 的区别

**10:00 - 11:30** → `02_field_constraints.py`  
掌握 Field 约束，学会数据验证

**11:30 - 12:30** → `03_validators.py`  
编写自定义验证器

### 下午（4小时）

**14:00 - 15:30** → `04_nested_models.py`  
处理复杂数据结构

**15:30 - 16:30** → `05_model_config.py`  
配置模型行为

**16:30 - 17:30** → `06_aliases_serialization.py`  
控制输入输出格式

**17:30 - 18:30** → `07_practical.py`  
实战练习

### 复习（0.5小时）

**18:30 - 19:00** → `08_common_mistakes.py`  
避免常见错误

## 🎯 学习目标

完成后你将能够：

- ✅ 熟练使用 Pydantic V2 API
- ✅ 编写数据验证规则
- ✅ 处理复杂的数据结构
- ✅ 在实际项目中应用

## 📚 推荐学习顺序

```
01_basics.py (必学)
    ↓
02_field_constraints.py (必学)
    ↓
03_validators.py (必学)
    ↓
04_nested_models.py (推荐)
    ↓
05_model_config.py (推荐)
    ↓
06_aliases_serialization.py (进阶)
    ↓
07_practical.py (实战)
    ↓
08_common_mistakes.py (总结)
```

## 🔥 最重要的 3 个概念

### 1. V2 方法都有 `model_` 前缀

```python
# V1 (错误)          # V2 (正确)
user.dict()      →   user.model_dump()
user.json()      →   user.model_dump_json()
User.parse_obj() →   User.model_validate()
```

### 2. 验证器需要装饰器和返回值

```python
@field_validator('username')
@classmethod  # 不要忘记！
def validate_username(cls, v: str) -> str:
    return v.lower()  # 必须返回！
```

### 3. 可变默认值要用 `default_factory`

```python
# 错误 ❌
tags: List[str] = []

# 正确 ✅
tags: List[str] = Field(default_factory=list)
```

## 💡 学习技巧

1. **运行代码** - 每个文件都可以直接运行
2. **修改参数** - 尝试改变参数看效果
3. **制造错误** - 故意写错代码，理解错误信息
4. **做笔记** - 记录易错点
5. **查阅文档** - 遇到问题查看 [官方文档](https://docs.pydantic.dev)

## 🆘 遇到问题？

1. 查看 `08_common_mistakes.py` - 常见错误对比
2. 查看 `QUICK_REFERENCE.md` - 快速查询
3. 查看 `README_LEARNING.md` - 完整指南

## ✅ 学习检查清单

学完每章后，检查是否能做到：

- [ ] 第1章：能说出 5 个 V2 核心方法
- [ ] 第2章：能写出 3 种 Field 约束
- [ ] 第3章：能编写 field_validator
- [ ] 第4章：能处理嵌套的 List/Dict
- [ ] 第5章：能配置 ConfigDict
- [ ] 第6章：能控制序列化输出
- [ ] 第7章：能构建完整的数据模型
- [ ] 第8章：能避免 10 个常见错误

## 🎓 下一步

学完教程后：

1. **实践项目** - 在自己的项目中使用
2. **FastAPI** - 学习与 FastAPI 集成
3. **ORM** - 学习与数据库 ORM 集成

---

**准备好了吗？开始学习吧！** 🚀

```bash
python learning/01_basics.py
```

有任何问题欢迎查阅文档或提问！

