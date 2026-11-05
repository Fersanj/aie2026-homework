import json

from pydantic_ai.models.test import TestModel

from app import tools
from app.agent import agent, run


def test_make_quiz():
    quiz = json.loads(tools.make_quiz(2))
    assert quiz["question"] and quiz["answer"]
    assert "no glossary terms" in tools.make_quiz(0)


def test_save_learning_log(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "LOG_DIR", tmp_path)
    tools.save_learning_log("LoRA notes", "Only small matrices are trained.")
    assert len(list(tmp_path.glob("*.md"))) == 1


def test_save_only_after_yes(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "LOG_DIR", tmp_path)
    model = TestModel(call_tools=["save_learning_log"])

    monkeypatch.setattr("builtins.input", lambda _: "n")
    run(agent, "save my notes", model)
    assert not list(tmp_path.glob("*.md"))

    monkeypatch.setattr("builtins.input", lambda _: "y")
    run(agent, "save my notes", model)
    assert len(list(tmp_path.glob("*.md"))) == 1
