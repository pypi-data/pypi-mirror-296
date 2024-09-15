from abc import ABC, abstractmethod

import rich.repr
from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import ProgressBar
from rich.style import StyleType
from rich.table import Table


@rich.repr.auto
class Template(ABC):
	"""Базовый класс для шаблонов элементов слайда."""

	@abstractmethod
	def __rich__(self) -> Layout:
		"""
		Отвечает за генерацию шаблона элемента слайда.

		Returns:
			Layout: Сгенерированный элемент слайда.
		"""


class StandartHeader(Template):
	"""
	Стандартный заголовок слайда.

	Args:
		title (str): Текст заголовка.
		slide_number (int): Порядковый номер слайда.
		total_slides (int): Общее количество слайдов.
		info_style (str, optional): Стиль текста с информацией о слайдах. По умолчанию "dim".
		border_style (str, optional): Стиль границы заголовка. По умолчанию "dim".
		info_visible (bool, optional): Надо ли показывать информацию о слайдах. По умолчанию True.
	"""

	def __init__(
			self,
			title: str,
			slide_number: int,
			total_slides: int,
			info_style: StyleType = 'dim',
			border_style: StyleType = 'dim',
			info_visible: bool = True
	):
		self.title = title
		self.slide_number = slide_number
		self.total_slides = total_slides

		self.info_style = info_style
		self.border_style = border_style
		self.info_visible = info_visible

	def __rich__(self) -> Layout:
		header = Layout()
		header.split_row(Layout(name='title'), Layout(name='info', size=15))

		header['title'].update(Panel(self.title, border_style=self.border_style))
		header['info'].update(
			Panel(
				Align.center(
					f'[{self.info_style}]Слайд[/] {self.slide_number}[{self.info_style}]/[/]{self.total_slides}'),
				border_style=self.border_style
			)
		)
		header['info'].visible = self.info_visible

		return header


class Progress(Template):
	"""
	Прогресс продвижения по шагам слайда.

	Args:
		progress (Union[tuple[int, int], None]): Прогресс по шагам слайда.
		complete_style (str, optional): Стиль незавершенного прогресс бара. По умолчанию "yellow".
		finished_style (str, optional): Стиль завершенного прогресс бара. По умолчанию "green".
	"""

	def __init__(self, progress: tuple[int, int] | None, complete_style: str = 'yellow', finished_style: str = 'green'):
		self.progress = progress

		self.complete_style = complete_style
		self.finished_style = finished_style

	def __rich__(self) -> Table:
		grid = Table.grid('', '', padding=(0, 2, 0, 1), pad_edge=True)

		if self.progress:
			completed, total = self.progress

			progress = ProgressBar(completed=completed, total=total, complete_style=self.complete_style,
								   finished_style=self.finished_style)
			grid.add_row(progress, f'{completed}/{total}')

		return Align.center(grid, vertical='bottom')
