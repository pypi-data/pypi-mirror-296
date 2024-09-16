#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Method class test cases."""

import asyncio
import pytest

from cmdcraft.method import Method

class Testing:

    a: int = 0
    b: str = ''

    def test_one(self, a: int = 0, b: str = ''):
        self.a = a
        self.b = b

    def test_two(self, a: int = 0, /, b: str = ''):
        self.a = a
        self.b = b

    def test_three(self, a: int = 0, *, b: str = ''):
        self.a = a
        self.b = b


def test_method_one_call():
    t = Testing()
    m = Method(t.test_one)
    m.process()

    m.eval('1', '2')
    assert t.a == 1
    assert t.b == '2'

    m.eval('a=2', 'b=3')
    assert t.a == 2
    assert t.b == '3'

def test_method_two_call():
    t = Testing()
    m = Method(t.test_two)
    m.process()

    m.eval('1', '2')
    assert t.a == 1
    assert t.b == '2'

    m.eval('2', 'b=3')
    assert t.a == 2
    assert t.b == '3'

def test_method_three_call():
    t = Testing()
    m = Method(t.test_three)
    m.process()

    m.eval('1', '2')
    assert t.a == 1
    assert t.b == '2'

    m.eval('a=2', 'b=3')
    assert t.a == 2
    assert t.b == '3'