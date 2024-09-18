import asyncio
import re
from os import PathLike
from typing import Callable

import awaitlet
from bs4 import BeautifulSoup, Tag
from httpx import Response

# from pages.course.assignments import AssignmentsPage
# from pages.course.course import CoursePage
# from pages.course.files import FilesPage
from ntucool.requestor import Requestor

from .base import NTUCoolBase


class Course(NTUCoolBase):
    id: int
    semester: str | None

    @property
    def url(self) -> str:
        return f"/courses/{self.id}"

    @property
    def assignments(self):
        return AssignmentsPage(parent=self, course_id=self.id)

    @property
    def files(self):
        # print(self.id, "files", "start")
        files = FilesPage(parent=self, course_id=self.id)
        # print(self.id, "files,", "end")
        return files

    def get_folder_by_path(self, path: PathLike | str, course_id: int | None = None):
        return self.files.root_folder / path


def _parse_row(row: Tag, parent: NTUCoolBase):
    span = row.select(".course-list-star-column > span")[0]
    if "disabled" in span.attrs["class"]:
        return None
    id = span.attrs["data-course-id"]
    id = int(id)
    try:
        assert span.parent and span.parent.parent
        semester = span.parent.parent.select(".course-list-term-column")[0].text
        semester = semester[: semester.index("(")].strip()
        assert re.match(r"\d+-\d", semester)
    except:
        semester = None

    course = Course(
        id=id,
        semester=semester,
        parent=parent,
    )
    course.requestor = requestor
    return course


courses_url = "https://cool.ntu.edu.tw/courses"


def _get_courses_old(parent: NTUCoolBase, resp: Response):
    soup = BeautifulSoup(resp.text, "html.parser")

    courses = [
        _parse_row(row, parent)
        for table in soup.select("#content > table")[:2]
        for row in table.select("tbody > tr")
    ]

    return [c for c in courses if c]


def _get_courses(parent: NTUCoolBase, resp: Response):

def get_courses(parent: NTUCoolBase):
    resp = parent.requestor.get(courses_url)
    return asyncio.run(awaitlet.async_def(_get_courses, parent, resp))


async def get_courses_async(parent: NTUCoolBase):
    resp = await parent.requestor.async_get(courses_url)
    return await awaitlet.async_def(_get_courses, parent, resp)
