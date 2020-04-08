# -*- coding: utf-8 -*-
from .mybatis import Model, Field

class Question(Model):
    
    id = Field('id')
    question = Field('question')
    solution = Field('solution')
    type = Field('type')
    category = Field('category')
    source = Field('source')
    code_sample = Field('code_sample')
    search_count = Field('search_count')
    link = Field('link')
    create_time = Field('create_time')
    update_time = Field('update_time')