from abc import ABC, abstractmethod
from typing import Literal, Callable, Union

import rich.repr
from rich import print
from rich.align import Align
from rich.box import Box, ROUNDED
from rich.console import Console, RenderableType
from rich.layout import Layout
from rich.padding import PaddingDimensions
from rich.panel import Panel
from rich.segment import Segment
from rich.segment import SegmentLines
from rich.style import StyleType
from rich_pixels import Pixels

from .templates import Progress, StandartHeader


def autoscroll(layout: Layout, sub_layout: Layout, text: RenderableType) -> SegmentLines:
	"""Автоматически прокручивает текст вниз, если он не помещается.

	Args:
		layout (Layout): Корневой layout вашего макета.
		sub_layout (Layout): layout, в котором вы хотите сделать автопрокрутку.
		text (RenderableType): Текст, который надо сдвинуть вниз.
	"""
	console = Console()

	# Получение размеров sub_layout.
	region, _ = layout.render(console, console.options)[sub_layout]
	width, height = region.width, region.height

	# Делим sub_layout на строчки.
	segments = Console(width=width, height=height).render(text)
	lines = [_ for _ in Segment(width).split_lines(segments)]

	# Обрезаем текст до необходимого размера.
	if len(lines) > height:
		lines = lines[len(lines) - height:]

	return SegmentLines(iter(lines), new_lines=True)


@rich.repr.auto
class Slide(ABC):
	"""Базовый класс для слайдов."""

	@abstractmethod
	def create_slide(self, slide_number: int, total_slides: int, progress: tuple[int, int] = None) -> Layout:
		"""Отвечает за создание слайда.

		Args:
			slide_number (int): Порядковый номер слайда.
			total_slides (int): Общее количество слайдов.
			progress (tuple[int, int], optional): Прогресс поэтапного отображения слайда (текущий слайд, всего слайдов).
				По умолчанию None.

		Returns:
			Layout: Сгенерированный слайд.
		"""

	def next(self) -> bool:
		"""Переключает слайд на следующий этап.

		Returns:
			bool: Если слайд переключился на следующий этап, возвращаем True, иначе False.
		"""
		return False

	def previous(self) -> bool:
		"""Переключает слайд на предыдущий этап.

		Returns:
			bool: Если слайд переключился на предыдущий этап, возвращаем True, иначе False.
		"""
		return False

	def show(self):
		"""Печатает слайд отдельно от презентации."""
		print(self.create_slide(1, 1))


class SlideWithSteps(Slide):
	"""Поэтапно отображает слайды.

	Args:
		steps (Union[list[Slide], Callable[[], Slide]]): Слайды для отображения.
	"""

	def __init__(self, steps: Union[list[Slide], Callable[[], Slide]]):
		self._steps = steps if isinstance(steps, list) else [_ for _ in steps()]
		self._index = 0

	def next(self) -> bool:
		if self._index < len(self._steps) - 1:
			self._index += 1
			return True
		return False

	def previous(self) -> bool:
		if self._index > 0:
			self._index -= 1
			return True
		return False

	def create_slide(self, slide_number: int, total_slides: int, progress: tuple[int, int] = None) -> Layout:
		return self._steps[self._index].create_slide(slide_number, total_slides, (self._index + 1, len(self._steps)))


class ImageSlide(Slide):
	"""Слайд, выводящий картинку на весь экран.

	Args:
		path (str): Путь к файлу изображения.
		resize (tuple[int, int], optional): Набор значений (ширина, высота) для изменения размера изображения.
			По умолчанию размер экрана.
	"""

	def __init__(self, path: str, resize: tuple[int, int] | None = None):
		self.path = path
		self.resize = resize or (Console().width, Console().height * 2)

		self._image: Pixels = Pixels.from_image_path(self.path, resize=self.resize)

	def create_slide(self, slide_number: int, total_slides: int, progress: tuple[int, int] = None) -> Layout:
		return Layout(Align.center(self._image, vertical='middle'))


class TitleSlide(Slide):
	"""Слайд с заголовком и подзаголовком.

	Args:
		title (str): Заголовок слайда.
		subtitle (RenderableType, optional): Подзаголовок слайда. По умолчанию пустая строка.
		box (Box, optional): Экземпляр Box, который определяет внешний вид границы заголовка. По умолчанию box.ROUNDED.
		style (str, optional): Стиль заголовка (границы и содержимое). По умолчанию "none".
		border_style (str, optional): Стиль границы заголовка. По умолчанию "none".
		padding (PaddingDimensions, optional): Необязательное отступление вокруг заголовка. По умолчанию (0, 1).
	"""

	def __init__(
			self,
			title: str,
			subtitle: RenderableType = '',
			*,
			box: Box = ROUNDED,
			style: StyleType = 'none',
			border_style: StyleType = 'none',
			padding: PaddingDimensions = (0, 1)
	):
		self.title = title
		self.subtitle = subtitle

		self.box = box
		self.style = style
		self.border_style = border_style
		self.padding = padding

	def create_slide(self, slide_number: int, total_slides: int, progress: tuple[int, int] = None) -> Layout:
		layout = Layout()
		layout.split(Layout(name='title'), Layout(name='subtitle'))

		layout['title'].update(
			Align.center(
				Panel(self.title, box=self.box, style=self.style, border_style=self.border_style, padding=self.padding),
				vertical='bottom'
			)
		)
		layout['subtitle'].update(Align.center(self.subtitle, vertical='middle'))

		return layout


class TitleImageSlide(Slide):
	"""Слайд с заголовком, подзаголовком и изображением.

	Args:
		title (str): Заголовок слайда.
		path (str): Путь к файлу изображения.
		subtitle (RenderableType, optional): Подзаголовок слайда. По умолчанию пустая строка.
		side (Literal["right", "left"], optional): Расположение изображения на слайде. По умолчанию "left".
		resize (tuple[int, int], optional): Набор значений (ширина, высота) для изменения размера изображения.
			По умолчанию половина размера окна.
		box (Box, optional): Экземпляр Box, который определяет внешний вид границы заголовка. По умолчанию box.ROUNDED.
		style (str, optional): Стиль заголовка (границы и содержимое). По умолчанию "none".
		border_style (str, optional): Стиль границы заголовка. По умолчанию "none".
		padding (PaddingDimensions, optional): Необязательное отступление вокруг заголовка. По умолчанию (0, 1).
	"""

	def __init__(
			self,
			title: str,
			path: str,
			subtitle: RenderableType = '',
			*,
			side: Literal['right', 'left'] = 'left',
			resize: tuple[int, int] = None,
			box: Box = ROUNDED,
			style: StyleType = 'none',
			border_style: StyleType = 'none',
			padding: PaddingDimensions = (0, 1)
	):
		self.title = title
		self.path = path
		self.subtitle = subtitle

		self.side = side
		self.resize = resize or (Console().width // 2, Console().height * 2)
		self.box = box
		self.style = style
		self.border_style = border_style
		self.padding = padding

		self._image: Pixels = Pixels.from_image_path(self.path, resize=self.resize)

	def create_slide(self, slide_number: int, total_slides: int, progress: tuple[int, int] = None) -> Layout:
		column = (Layout(name='text'), Layout(name='image'))

		if self.side == 'left':
			column = column[::-1]

		layout = Layout()
		layout.split_row(*column)
		layout['text'].split(Layout(name='title'), Layout(name='subtitle'))

		layout['text']['title'].update(
			Align.center(
				Panel(self.title, box=self.box, style=self.style, border_style=self.border_style, padding=self.padding),
				vertical='bottom'
			)
		)
		layout['text']['subtitle'].update(Align.center(self.subtitle, vertical='middle'))
		layout['image'].update(Align.center(self._image, vertical='middle'))

		return layout


class StandardSlide(Slide):
	"""Простой слайд с заголовком.

	Args:
		title (str): Заголовок слайда.
		text (RenderableType): Контент слайда.
		info_visible (bool, optional): Надо ли показывать информацию о слайдах. По умолчанию True.
		progress_visible (bool, optional): Надо ли показывать прогресс поэтапного отображения слайда. По умолчанию True.
		info_style (str, optional): Стиль текста с информацией о слайдах. По умолчанию "dim".
		border_style (str, optional): Стиль границы заголовка. По умолчанию "dim".
		complete_style (str, optional): Стиль незавершенного прогресс бара. По умолчанию "yellow".
		finished_style (str, optional): Стиль завершенного прогресс бара. По умолчанию "green".
	"""

	def __init__(
			self,
			title: str,
			text: RenderableType,
			*,
			info_visible: bool = True,
			progress_visible: bool = True,
			info_style: StyleType = 'dim',
			border_style: StyleType = 'dim',
			complete_style: StyleType = 'yellow',
			finished_style: StyleType = 'green'
	):
		self.title = title
		self.text = text

		self.progress_visible = progress_visible
		self.info_visible = info_visible
		self.info_style = info_style
		self.border_style = border_style
		self.complete_style = complete_style
		self.finished_style = finished_style

	def create_slide(self, slide_number: int, total_slides: int, progress: tuple[int, int] = None) -> Layout:
		layout = Layout()
		layout.split(Layout(name='header', size=3), Layout(name='body'), Layout(name='footer', size=2))

		layout['header'].update(
			StandartHeader(
				self.title,
				slide_number,
				total_slides,
				self.info_style,
				self.border_style,
				self.info_visible
			)
		)
		layout['body'].update(autoscroll(layout, layout['body'], self.text))
		layout['footer'].update(Progress(progress, self.complete_style, self.finished_style))

		layout['footer'].visible = progress and self.progress_visible

		return layout


class StandardImageSlide(Slide):
	"""Простой слайд с заголовком и изображением.

	Args:
		title (str): Заголовок слайда.
		text (RenderableType): Контент слайда.
		path (str): Путь к файлу изображения.
		side (Literal["right", "left"], optional): Расположение изображения на слайде. По умолчанию "left".
		resize (tuple[int, int], optional): Набор значений (ширина, высота) для изменения размера изображения.
			По умолчанию половина размера окна.
		info_visible (bool, optional): Надо ли показывать информацию о слайдах. По умолчанию True.
		progress_visible (bool, optional): Надо ли показывать прогресс поэтапного отображения слайда. По умолчанию True.
		info_style (str, optional): Стиль текста с информацией о слайдах. По умолчанию "dim".
		border_style (str, optional): Стиль границы заголовка. По умолчанию "dim".
		complete_style (str, optional): Стиль незавершенного прогресс бара. По умолчанию "yellow".
		finished_style (str, optional): Стиль завершенного прогресс бара. По умолчанию "green".
	"""

	def __init__(
			self,
			title: str,
			text: RenderableType,
			path: str,
			*,
			side: Literal['right', 'left'] = 'right',
			resize: tuple[int, int] = None,
			info_visible: bool = True,
			progress_visible: bool = True,
			info_style: StyleType = 'dim',
			border_style: StyleType = 'dim',
			complete_style: StyleType = 'yellow',
			finished_style: StyleType = 'green'
	):
		self.title = title
		self.text = text
		self.path = path

		self.side = side
		self.resize = resize or (Console().width // 2, Console().height * 2)
		self.progress_visible = progress_visible
		self.info_visible = info_visible
		self.info_style = info_style
		self.border_style = border_style
		self.complete_style = complete_style
		self.finished_style = finished_style

		self._image: Pixels = Pixels.from_image_path(self.path, resize=self.resize)

	def create_slide(self, slide_number: int, total_slides: int, progress: tuple[int, int] = None) -> Layout:
		column = (Layout(name='text'), Layout(name='image'))

		if self.side == 'left':
			column = column[::-1]

		layout = Layout()
		layout.split(Layout(name='header', size=3), Layout(name='body'), Layout(name='footer', size=2))
		layout['body'].split_row(*column)

		layout['header'].update(
			StandartHeader(
				self.title,
				slide_number,
				total_slides,
				self.info_style,
				self.border_style,
				self.info_visible
			)
		)
		layout['body']['image'].update(Align.center(self._image, vertical='middle'))
		layout['body']['text'].update(autoscroll(layout, layout['body']['text'], self.text))
		layout['footer'].update(Progress(progress, self.complete_style, self.finished_style))

		layout['footer'].visible = progress and self.progress_visible

		return layout
