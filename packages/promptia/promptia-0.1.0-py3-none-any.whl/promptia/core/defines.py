"""各種定義クラス."""
from pydantic import BaseModel


class Property(BaseModel):
    """プロパティクラス."""

    name: str


class ObjectProperty(Property):
    """オブジェクトプロパティクラス."""

    properties: list[Property]


class ArrayProperty(Property):
    """配列プロパティクラス."""

    items: Property


class StringProperty(Property):
    """文字列プロパティクラス."""

    description: str


class Function(BaseModel):
    """関数クラス."""

    name: str
    description: str
    parameters: list[Property]


class FunctionCallingConfig(BaseModel):
    """関数呼び出し設定クラス."""

    functions: list[Function]
    function_call: str | None = None


class PromptTemplate(BaseModel):
    """プロンプトテンプレートクラス."""

    name: str
    description: str
    content: str
    parameters: dict[str, str]
    function_calling_config: FunctionCallingConfig | None = None
    version: str = '1.0'


class BuiltPrompt:
    """適用済みプロンプトクラス."""

    def __init__(self, content: str, function_calling_config: FunctionCallingConfig | None = None) -> None:
        """コンストラクタ."""
        self.content = content
        self.function_calling_config = function_calling_config
