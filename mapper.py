# -*- coding: utf-8 -*-
from typing import List
from .mybatis import Mapper
from .model import Question

@Mapper()
class QuestionMapper:

    def insert(self, question: Question):
        return '''
            INSERT INTO tb_question(
                id, question, solution, 
                type, category, source, 
                code_sample, search_count, 
                link, create_time, update_time
            ) 
            VALUES(
                {id}, {question}, {solution}, 
                {type}, {category}, {source}, 
                {code_sample}, {search_count}, {link}, 
                {create_time}, {update_time}
            )
        '''

    def select(self, question: str)->List[Question]:
        return "SELECT * FROM tb_question WHERE question LIKE '%'||{question}||'%'"
