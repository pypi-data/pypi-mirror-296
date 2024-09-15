import rich.repr
from keyboard import read_event
from rich.layout import Layout
from rich.live import Live

from .slide import Slide

# Кнопки управления.
FORWARD_BUTTONS = ('right', 'down', 'space', 'enter', 'n')
REWIND_BUTTONS = ('up', 'left', 'p')
EXIT_BUTTON = 'q'


@rich.repr.auto
class Presentation:
	"""Класс для создания и управления презентацией."""

	def __init__(self):
		self._slides: list[Slide] = []

	def add(self, slide: Slide) -> None:
		"""Добавляет слайд в презентацию."""
		self._slides.append(slide)

	def start(self) -> None:
		"""Запуск презентации.

		Raises:
			IndexError: Если в презентации отсутствуют слайды.
		"""

		if not self._slides:
			raise IndexError('There are no slides in the presentation!')

		slide_number = 0
		slide = self._get_slide(slide_number)

		with Live(self._render(slide, slide_number), screen=True, transient=True, auto_refresh=False) as live:
			while True:
				try:
					key_event = read_event()

					if key_event.event_type == 'down':
						if key_event.name == EXIT_BUTTON:
							break

						elif key_event.name in FORWARD_BUTTONS:
							if not slide.next() and slide_number < len(self._slides) - 1:
								slide_number += 1

						elif key_event.name in REWIND_BUTTONS:
							if not slide.previous() and slide_number > 0:
								slide_number -= 1

						slide = self._get_slide(slide_number)
						live.update(self._render(slide, slide_number), refresh=True)
				except KeyboardInterrupt:
					break

	def _render(self, slide: Slide, slide_number: int) -> Layout:
		"""Создаёт слайд.

		Args:
			slide (Slide): Класс, из которого надо создать слайд.
			slide_number (int): Номер слайда.
		"""
		return slide.create_slide(slide_number + 1, len(self._slides))

	def _get_slide(self, slide_number: int) -> Slide:
		"""Получение слайда по номеру.

		Args:
			slide_number (int): Номер слайда.
		"""
		return self._slides[slide_number]
