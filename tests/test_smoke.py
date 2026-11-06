from pytest import CaptureFixture

from rag.__main__ import main


def test_main(capsys: CaptureFixture[str]) -> None:
    main()
    assert capsys.readouterr().out == "Application is running.\n"
