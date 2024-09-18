from PyQt5.QtCore import Qt
import pytest

from fake_py_qt import FakePyQTApp


@pytest.fixture
def app(qtbot):
    """Fixture to initialize the FakePyQTApp."""
    test_app = FakePyQTApp()
    qtbot.addWidget(test_app)
    test_app.show()
    return test_app


def test_window_title(app):
    """Test if the window title is correct."""
    assert app.windowTitle() == "fake.py GUI"


def test_provider_tree_initial_state(app):
    """Test the initial state of the provider tree."""
    # Test if provider tree is populated with categories
    assert app.provider_tree.topLevelItemCount() > 0


def test_provider_selection(qtbot, app):
    """Test selecting a provider from the tree."""
    provider_item = app.provider_tree.topLevelItem(0).child(
        0
    )  # Get first provider
    app.provider_tree.setCurrentItem(provider_item)

    # Ensure the description label updates after selecting a provider
    assert (
        app.provider_description.text()
        != "Select a provider to see its description."
    )

    # Ensure form layout is populated with input fields
    assert app.form_layout.rowCount() > 1


def test_generate_button_with_empty_form(qtbot, app):
    """Test generating data with empty form inputs."""
    provider_item = app.provider_tree.topLevelItem(0).child(
        0
    )  # Select a provider
    app.provider_tree.setCurrentItem(provider_item)

    generate_button = app.form_layout.itemAt(
        app.form_layout.rowCount() - 1
    ).widget()

    with qtbot.waitSignal(
        app.results_display.itemChanged, timeout=1000, raising=False
    ):
        qtbot.mouseClick(generate_button, Qt.LeftButton)

    # Ensure no data is generated since the form is empty
    assert app.results_display.count() == 0


def test_clear_button(qtbot, app):
    """Test the clear button functionality."""
    # Populate the results display with a dummy item
    app.results_display.addItem("Test Item")
    assert app.results_display.count() == 1

    # Click the clear button and check if the list is cleared
    qtbot.mouseClick(app.clear_button, Qt.LeftButton)
    assert app.results_display.count() == 0
