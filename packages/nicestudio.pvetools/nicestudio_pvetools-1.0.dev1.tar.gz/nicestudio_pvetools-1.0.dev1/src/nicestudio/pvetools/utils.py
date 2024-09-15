# -*- coding: utf-8 -*-

def get_percentage(c, t):
    p = (c * 100.0 / t) if c > 0 and t > 0 else 0.0
    return "%.2f%%" % p
