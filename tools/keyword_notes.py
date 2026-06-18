from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    """单个关键词笔记的数据结构"""
    keyword: str
    summary: str
    related_url: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None
    importance: int = 1  # 1-5

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.importance = max(1, min(5, self.importance))

    def to_line(self) -> str:
        return f"[{self.keyword}] {self.summary} | 来源: {self.related_url} | 标签: {'、'.join(self.tags)}"

    def short_display(self) -> str:
        return f"{self.keyword} ({'★' * self.importance})"


@dataclass
class NoteCollection:
    """关键词笔记集合"""
    notes: List[KeywordNote] = field(default_factory=list)
    category: str = "默认"

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_keyword(self, keyword_fragment: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword_fragment.lower() in n.keyword.lower()]

    def count_by_importance(self, level: int) -> int:
        return sum(1 for n in self.notes if n.importance == level)

    def format_all(self, separator: str = "\n---\n") -> str:
        lines = [f"=== {self.category} 笔记 ({len(self.notes)} 条) ==="]
        for i, note in enumerate(self.notes, 1):
            lines.append(f"{i}. {note.to_line()}")
        return separator.join(lines)

    def export_markdown(self) -> str:
        lines = [f"# {self.category} 笔记\n"]
        for note in sorted(self.notes, key=lambda x: x.importance, reverse=True):
            lines.append(f"## {note.keyword}")
            lines.append(f"- **摘要**: {note.summary}")
            lines.append(f"- **来源**: [{note.related_url}]({note.related_url})")
            lines.append(f"- **标签**: {', '.join(note.tags)}")
            lines.append(f"- **重要度**: {'★' * note.importance}")
            lines.append("")
        return "\n".join(lines)


def build_sample_collection() -> NoteCollection:
    """生成一组示例关键词笔记"""
    url_base = "https://www.guessgroup-kaiyun.com.cn"
    collection = NoteCollection(category="体育竞猜")

    collection.add_note(KeywordNote(
        keyword="开云小组赛竞猜",
        summary="用户参与小组赛阶段的结果预测，涵盖胜平负、比分等玩法",
        related_url=url_base,
        tags=["竞猜", "小组赛", "体育"],
        importance=5
    ))

    collection.add_note(KeywordNote(
        keyword="开云赛事分析",
        summary="基于历史数据和实时状态的比赛走势研判",
        related_url=url_base + "/analysis",
        tags=["分析", "数据", "预测"],
        importance=4
    ))

    collection.add_note(KeywordNote(
        keyword="开云赔率动态",
        summary="实时跟踪主流博彩公司赔率波动与市场热度",
        related_url=url_base + "/odds",
        tags=["赔率", "实时", "市场"],
        importance=3
    ))

    collection.add_note(KeywordNote(
        keyword="开云用户指南",
        summary="新用户注册、充值、投注及提现操作说明",
        related_url=url_base + "/guide",
        tags=["教程", "入门", "帮助"],
        importance=2
    ))

    return collection


def main() -> None:
    collection = build_sample_collection()
    print(collection.format_all())
    print("\n--- Markdown 导出 ---\n")
    print(collection.export_markdown())

    print("\n--- 按关键词过滤测试 ---")
    keyword_fragment = "小组赛"
    filtered = collection.filter_by_keyword(keyword_fragment)
    print(f"包含「{keyword_fragment}」的笔记：")
    for note in filtered:
        print(f"  - {note.short_display()}")

    print("\n--- 重要度统计 ---")
    for level in range(1, 6):
        count = collection.count_by_importance(level)
        if count:
            print(f"  重要度 {level}: {count} 条")


if __name__ == "__main__":
    main()