"""Promptiaのメインロジックを実装するモジュール."""
from jinja2 import Template

from .defines import BuiltPrompt
from .defines import PromptTemplate
from ..retrievers.base import Retriever
from ..storages.base import TemplateStorage


class Promptia:
    """Promptiaのメインロジックを実装するクラス."""

    def __init__(self, storage: TemplateStorage) -> None:
        """コンストラクタ."""
        self.storage = storage

    def add_template(self, template: PromptTemplate) -> None:
        """テンプレートを追加する."""
        self.storage.save_template(template)

    def get_template(self, name: str, version: str) -> PromptTemplate:
        """指定された名前とバージョンのテンプレートを取得する."""
        return self.storage.load_template(name, version)

    def build(self, template_name: str, version: str, values: dict[str, str | Retriever]) -> BuiltPrompt:
        """プロンプトを構築する."""
        template = self.get_template(template_name, version)
        processed_values = {}

        for key, value in values.items():
            if isinstance(value, Retriever):
                processed_values[key] = value.query()
            else:
                processed_values[key] = value

        tmpl = Template(source=template.system)
        rendered_content = tmpl.render(processed_values)
        return BuiltPrompt(
            system=rendered_content,
            messages=template.messages,
            function_calling_config=template.function_calling_config
        )

    # def list_versions(self, name: str) -> list[str]:
    #     """指定されたテンプレート名の全バージョンをリストアップする."""
    #     return self.storage.list_versions(name)

    # def compare_versions(self, name: str, version1: str, version2: str) -> str:
    #     """2つのバージョン間の差分を比較する."""
    #     pass
        # template1 = self.get_template(name, version1)
        # template2 = self.get_template(name, version2)
        # return self._calculate_diff(template1, template2)

    # def _calculate_diff(self, template1: PromptTemplate, template2: PromptTemplate) -> str:
    #     """テンプレート間の差分を計算する."""
    #     diff = difflib.unified_diff(
    #         template1.content.splitlines(keepends=True),
    #         template2.content.splitlines(keepends=True),
    #         fromfile=f'Version: {template1.version}',
    #         tofile=f'Version: {template2.version}',
    #         n=3
    #     )
    #     return ''.join(diff)
