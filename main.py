from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(..., description="The user's ID")
    name: str = Field(..., description="The user's name")
    email: str = Field(..., description="The user's email")

user = User(id=1, name="John Doe", email="john.doe@example.com")

# ===== 区别演示 =====
print("=" * 60)
print("model_dump() vs model_dump_json() 区别演示")
print("=" * 60)
print()

# 1. model_dump() 返回 Python 字典
dump_result = user.model_dump()
print("1. model_dump() 的结果:")
print(f"   返回类型: {type(dump_result)}")
print(f"   内容: {dump_result}")
print(f"   可以像字典一样访问: dump_result['name'] = {dump_result['name']}")
print()

# 2. model_dump_json() 返回 JSON 字符串
json_result = user.model_dump_json()
print("2. model_dump_json() 的结果:")
print(f"   返回类型: {type(json_result)}")
print(f"   内容: {json_result}")
print(f"   这是一个字符串，需要解析才能访问值")
print()

# 3. model_dump_json(indent=2) 格式化的 JSON 字符串
json_pretty = user.model_dump_json(indent=2)
print("3. model_dump_json(indent=2) 格式化输出:")
print(f"   返回类型: {type(json_pretty)}")
print(f"   内容:\n{json_pretty}")
print()

# 4. 使用场景对比
print("=" * 60)
print("使用场景:")
print("=" * 60)
print("model_dump() 适用于:")
print("  ✓ 在 Python 代码中操作数据")
print("  ✓ 直接访问字段值")
print("  ✓ 传递给其他 Python 函数")
print()
print("model_dump_json() 适用于:")
print("  ✓ 保存到文件")
print("  ✓ 发送 HTTP 请求")
print("  ✓ API 响应")
print("  ✓ 跨语言数据传输")
print("=" * 60)
