# jaZYK

Simple LM api wrappers for production

## Installation
```
uv add zyk
```
or
```
pip install zyk
```

## Usage
```
from zyk import LM
lm = LM(model_name="gpt-4o-mini", temperature=0.0)
print(lm.respond_sync(system_message="You are a helpful assistant", user_message="Hello, how are you?"))
```
