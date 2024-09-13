# SPDX-License-Identifier: MIT

from __future__ import annotations

import re
import textwrap

import pytest

import pyproject_metadata


@pytest.mark.parametrize(
    ('items', 'data'),
    [
        # empty
        ([], ''),
        # simple
        (
            [
                ('Foo', 'Bar'),
            ],
            'Foo: Bar\n',
        ),
        (
            [
                ('Foo', 'Bar'),
                ('Foo2', 'Bar2'),
            ],
            """\
            Foo: Bar
            Foo2: Bar2
            """,
        ),
        # None
        (
            [
                ('Item', None),
            ],
            '',
        ),
        # order
        (
            [
                ('ItemA', 'ValueA'),
                ('ItemB', 'ValueB'),
                ('ItemC', 'ValueC'),
            ],
            """\
            ItemA: ValueA
            ItemB: ValueB
            ItemC: ValueC
            """,
        ),
        (
            [
                ('ItemB', 'ValueB'),
                ('ItemC', 'ValueC'),
                ('ItemA', 'ValueA'),
            ],
            """\
            ItemB: ValueB
            ItemC: ValueC
            ItemA: ValueA
            """,
        ),
        # multiple keys
        (
            [
                ('ItemA', 'ValueA1'),
                ('ItemB', 'ValueB'),
                ('ItemC', 'ValueC'),
                ('ItemA', 'ValueA2'),
            ],
            """\
            ItemA: ValueA1
            ItemB: ValueB
            ItemC: ValueC
            ItemA: ValueA2
            """,
        ),
        (
            [
                ('ItemA', 'ValueA'),
                ('ItemB', 'ValueB1\nValueB2\nValueB3'),
                ('ItemC', 'ValueC'),
            ],
            """\
            ItemA: ValueA
            ItemB: ValueB1
                    ValueB2
                    ValueB3
            ItemC: ValueC
            """,
        ),
    ],
)
def test_headers(items: list[tuple[str, str]], data: str) -> None:
    message = pyproject_metadata.RFC822Message()
    smart_message = pyproject_metadata._SmartMessageSetter(message)

    for name, value in items:
        if value and '\n' in value:
            msg = '"ItemB" should not be multiline; indenting to avoid breakage'
            with pytest.warns(
                pyproject_metadata.ConfigurationWarning, match=re.escape(msg)
            ):
                smart_message[name] = value
        else:
            smart_message[name] = value

    data = textwrap.dedent(data) + '\n'
    assert str(message) == data
    assert bytes(message) == data.encode()


def test_body() -> None:
    message = pyproject_metadata.RFC822Message()

    message['ItemA'] = 'ValueA'
    message['ItemB'] = 'ValueB'
    message['ItemC'] = 'ValueC'

    message.set_payload(
        textwrap.dedent("""
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris congue semper
        fermentum. Nunc vitae tempor ante. Aenean aliquet posuere lacus non faucibus.
        In porttitor congue luctus. Vivamus eu dignissim orci. Donec egestas mi ac
        ipsum volutpat, vel elementum sapien consectetur. Praesent dictum finibus
        fringilla. Sed vel feugiat leo. Nulla a pharetra augue, at tristique metus.

        Aliquam fermentum elit at risus sagittis, vel pretium augue congue. Donec leo
        risus, faucibus vel posuere efficitur, feugiat ut leo. Aliquam vestibulum vel
        dolor id elementum. Ut bibendum nunc interdum neque interdum, vel tincidunt
        lacus blandit. Ut volutpat sollicitudin dapibus. Integer vitae lacinia ex, eget
        finibus nulla. Donec sit amet ante in neque pulvinar faucibus sed nec justo.
        Fusce hendrerit massa libero, sit amet pulvinar magna tempor quis.
    """)
    )

    assert str(message) == textwrap.dedent("""\
        ItemA: ValueA
        ItemB: ValueB
        ItemC: ValueC


        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris congue semper
        fermentum. Nunc vitae tempor ante. Aenean aliquet posuere lacus non faucibus.
        In porttitor congue luctus. Vivamus eu dignissim orci. Donec egestas mi ac
        ipsum volutpat, vel elementum sapien consectetur. Praesent dictum finibus
        fringilla. Sed vel feugiat leo. Nulla a pharetra augue, at tristique metus.

        Aliquam fermentum elit at risus sagittis, vel pretium augue congue. Donec leo
        risus, faucibus vel posuere efficitur, feugiat ut leo. Aliquam vestibulum vel
        dolor id elementum. Ut bibendum nunc interdum neque interdum, vel tincidunt
        lacus blandit. Ut volutpat sollicitudin dapibus. Integer vitae lacinia ex, eget
        finibus nulla. Donec sit amet ante in neque pulvinar faucibus sed nec justo.
        Fusce hendrerit massa libero, sit amet pulvinar magna tempor quis.
    """)


def test_convert_optional_dependencies() -> None:
    metadata = pyproject_metadata.StandardMetadata.from_pyproject(
        {
            'project': {
                'name': 'example',
                'version': '0.1.0',
                'optional-dependencies': {
                    'test': [
                        'foo; os_name == "nt" or sys_platform == "win32"',
                        'bar; os_name == "posix" and sys_platform == "linux"',
                    ],
                },
            },
        }
    )
    message = metadata.as_rfc822()
    requires = message.get_all('Requires-Dist')
    assert requires == [
        'foo; (os_name == "nt" or sys_platform == "win32") and extra == "test"',
        'bar; os_name == "posix" and sys_platform == "linux" and extra == "test"',
    ]


def test_convert_author_email() -> None:
    metadata = pyproject_metadata.StandardMetadata.from_pyproject(
        {
            'project': {
                'name': 'example',
                'version': '0.1.0',
                'authors': [
                    {
                        'name': 'John Doe, Inc.',
                        'email': 'johndoe@example.com',
                    },
                    {
                        'name': 'Kate Doe, LLC.',
                        'email': 'katedoe@example.com',
                    },
                ],
            },
        }
    )
    message = metadata.as_rfc822()
    assert message.get_all('Author-Email') == [
        '"John Doe, Inc." <johndoe@example.com>, "Kate Doe, LLC." <katedoe@example.com>'
    ]
