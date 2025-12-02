from abc import ABC, abstractmethod
import asyncio
from dataclasses import dataclass
from enum import Enum
import sys
from types import CoroutineType
from typing import Any, Callable
from PyQt6.QtWidgets import QLabel, QApplication, QScrollArea, QSizePolicy, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QComboBox, QMessageBox, QInputDialog
from PyQt6.QtCore import Qt
from ..input.iinput import IInput

from .ioutput import IOutput

from ..models.task import Task, TaskStatus

class EventType(Enum):
    delete = 1
    update = 2
    status = 3

@dataclass
class TaskWidgetEvent:
    id: int
    event: EventType
    task: Task | None = None

class IPubSubSubscriber(ABC):
    @abstractmethod
    async def notify(self, event: TaskWidgetEvent): ...

class PubSub:
    subscribers: list[IPubSubSubscriber] = []

    @classmethod
    async def notify(cls, event: TaskWidgetEvent):
        await asyncio.gather(*[subscriber.notify(event) for subscriber in cls.subscribers])

class TaskWidget(QWidget):
    def __init__(self, task: Task, parent: QWidget | None = None, flags: Qt.WindowType = Qt.WindowType.Widget):
        super().__init__(parent, flags)

        self.task = task
        self.draw()

    async def _delete_task_clicked(self):
        response = QMessageBox.question(None, "The task will be deleted.", "Do you want to proceed?", QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)

        if response == QMessageBox.StandardButton.Yes:
            notify_task = asyncio.create_task(PubSub.notify(TaskWidgetEvent(
                id=self.task.id,
                event=EventType.delete
            )))
            await notify_task

    async def _update_task_clicked(self):
        new_description, ok = QInputDialog.getText(None, 'Editing task', 'Task description:', text=self.task.description)
        if ok and new_description:
            notify_task = asyncio.create_task(PubSub.notify(TaskWidgetEvent(
                id=self.task.id,
                event=EventType.update,
                task=Task(**{**self.task.__dict__, "description": new_description})
            )))
            await notify_task

    async def _mark_done_clicked(self):
        notify_task = asyncio.create_task(PubSub.notify(TaskWidgetEvent(
            id=self.task.id,
            event=EventType.status,
            task=Task(**{**self.task.__dict__, "status": TaskStatus.done.value})
        )))
        await notify_task

    async def _mark_in_progress_clicked(self):
        notify_task = asyncio.create_task(PubSub.notify(TaskWidgetEvent(
            id=self.task.id,
            event=EventType.status,
            task=Task(**{**self.task.__dict__, "status": TaskStatus.in_progress.value})
        )))
        await notify_task

    def _format_content(self) -> str:
        return f"{self.task.status}: {self.task.description}"

    def _draw_content(self):
        task_content_widget = QWidget()
        task_content_layout = QVBoxLayout(task_content_widget)

        self.label = QLabel(self._format_content())
        self.label.setWordWrap(True)
        task_content_layout.addWidget(self.label)
        task_content_layout.addStretch()
        return task_content_widget

    def _draw_buttons(self):
        task_buttons_widget = QWidget()
        task_buttons_widget.setFixedWidth(140)
        task_buttons_layout = QVBoxLayout(task_buttons_widget)
        task_buttons_layout.setSpacing(0)
        update_button = QPushButton("Edit")
        task_buttons_layout.addWidget(update_button)
        update_button.clicked.connect(lambda: asyncio.create_task(self._update_task_clicked()))
        in_progress_button = QPushButton("In progress")
        task_buttons_layout.addWidget(in_progress_button)
        in_progress_button.clicked.connect(lambda: asyncio.create_task(self._mark_in_progress_clicked()))
        done_button = QPushButton("Done")
        task_buttons_layout.addWidget(done_button)
        done_button.clicked.connect(lambda: asyncio.create_task(self._mark_done_clicked()))
        delete_button = QPushButton("Delete")
        task_buttons_layout.addWidget(delete_button)
        delete_button.clicked.connect(lambda: asyncio.create_task(self._delete_task_clicked()))
        task_buttons_layout.addStretch()
        return task_buttons_widget
       
    def draw(self):
        self.task_outer_layout = QHBoxLayout(self)
        self.task_outer_layout.addWidget(self._draw_content())
        self.task_outer_layout.addWidget(self._draw_buttons())
    
    def remove(self):
        self.task_outer_layout.removeWidget(self)
        self.deleteLater()
    
    def apply_changes(self, task: Task):
        self.task = task
        self.label.setText(self._format_content())

 

class PyQtInputOutput(IOutput, IInput, IPubSubSubscriber):
    def __init__(self):
        self.task_mapping: dict[int, TaskWidget] = {}
        self.application = QApplication(sys.argv)
        self.window = self._draw_window()

    def _create_task_clicked(self):
        title, ok = QInputDialog.getText(None, 'Creating new task', 'New task:')
        if ok and title:
            handler_task = asyncio.create_task(self.__add_handler(title))

    def _add_task(self, task: Task, idx: int):
        widget = TaskWidget(task=task)
        self.task_mapping[task.id] = widget
        self.inner_task_list_layout.addWidget(widget)

    def _draw_top_controls(self):
        top_buttons_widget = QWidget()
        top_buttons_layout = QHBoxLayout(top_buttons_widget)

        create_button = QPushButton("Add task")
        create_button.setFixedHeight(30)
        create_button.setMaximumWidth(140)
        create_button.clicked.connect(self._create_task_clicked)

        filter_combobox = QComboBox()
        filter_combobox.addItems(["All", "Planned", "In Progress", "Done"])

        top_buttons_layout.setContentsMargins(10, 0, 0, 0)
        top_buttons_layout.setSpacing(0)
        top_buttons_layout.addWidget(create_button)
        top_buttons_layout.addStretch()
        top_buttons_layout.addWidget(filter_combobox)

        return top_buttons_widget
    
    def _draw_window(self):
        window = QWidget()
        window_layout = QVBoxLayout(window)

        task_list_area = QWidget(window)
        task_list_area.setWindowTitle("Task Manager")
        task_list_area.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.task_list_layout = QVBoxLayout(task_list_area)
        self.task_list_layout.setContentsMargins(0, 0, 0, 0)
        self.task_list_layout.setSpacing(0)

        inner_task_list_area = QWidget(window)
        inner_task_list_area.setWindowTitle("Task Manager")
        inner_task_list_area.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.inner_task_list_layout = QVBoxLayout(inner_task_list_area)
        self.inner_task_list_layout.setContentsMargins(0, 0, 0, 0)
        self.inner_task_list_layout.setSpacing(0)

        self.task_list_layout.addWidget(inner_task_list_area)
        self.task_list_layout.addStretch()

        task_list_scroll_area = QScrollArea()
        task_list_scroll_area.setWidgetResizable(True)
        task_list_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        task_list_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        task_list_scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        task_list_scroll_area.setWidget(task_list_area)

        top_buttons_widget = self._draw_top_controls()

        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.setSpacing(0)
        window_layout.addWidget(top_buttons_widget)
        window_layout.addWidget(task_list_scroll_area)

        return window

    # output
    async def tasks_list(self, tasks_list: list[tuple[int, Task]]):
        [self._add_task(idx=task[1].id, task=task[1]) for task in tasks_list]

    async def task_added_success(self, id: int, task: Task):
        self._add_task(idx=task.id, task=task)

    async def task_status_updated_success(self, id: int, task: Task):
        self.task_mapping[task.id].apply_changes(task)

    async def task_updated_success(self, id: int, task: Task):
        self.task_mapping[task.id].apply_changes(task)

    async def task_deleted_success(self, id: int):
        self.task_mapping[id].remove()

    async def error_task_not_found(self, index: int):
        pass

    async def error_task_status_not_found(self, key: str): 
        pass

    async def error_index_type(self, index: str):
        pass

    async def error_storage_type(self, storage_type: str):
        pass

    async def error(self, text: str):
        pass

    # input
    async def start(self):
        PubSub.subscribers.append(self)
        await asyncio.create_task(self.__list_handler(None))
        self.window.show()
        # sys.exit(self.application.exec())
        pass


    def set_add_handler(
        self, callback: Callable[[str], CoroutineType[Any, Any, None]]
    ) -> None:
        self.__add_handler = callback

    def set_list_handler(
        self, callback: Callable[[TaskStatus | None], CoroutineType[Any, Any, None]]
    ) -> None:
        self.__list_handler = callback

    def set_update_handler(
        self, callback: Callable[[int, str], CoroutineType[Any, Any, None]]
    ) -> None:
        self.__update_handler = callback

    def set_status_handler(
        self, callback: Callable[[int, str], CoroutineType[Any, Any, None]]
    ) -> None:
        self.__status_handler = callback

    def set_delete_handler(
        self, callback: Callable[[int], CoroutineType[Any, Any, None]]
    ) -> None:
        self.__delete_handler = callback

    def set_error_handler(
        self, callback: Callable[[str], CoroutineType[Any, Any, None]]
    ) -> None:
        self.__error_handler = callback

    # pubsubsubscriber
    async def notify(self, event: TaskWidgetEvent):
        match event.event:
            case EventType.delete:
                handler_task = asyncio.create_task(self.__delete_handler(event.id))
                await handler_task
            case EventType.update:
                if event.task:
                    handler_task = asyncio.create_task(self.__update_handler(event.id, event.task.description))
                    await handler_task
                else:
                    handler_task = asyncio.create_task(self.__error_handler("Update message is missing task information."))
                    await handler_task
            case EventType.status:
                if event.task:
                    handler_task = asyncio.create_task(self.__status_handler(event.id, event.task.status))
                    await handler_task
                else:
                    handler_task = asyncio.create_task(self.__error_handler("Status message is missing task information."))
                    await handler_task
