
from modelos import Campus
from scraping.mapeamentos_base import MapeamentoCardapio, MapeamentoBandejao

_SAO_CRISTOVAO_HEADER = {
    "campus": (2, 3),
    "fornecedor": (3, 2),

}

MAPEAMENTO_SAO_CRISTOVAO = [
    MapeamentoCardapio(
        **_SAO_CRISTOVAO_HEADER,
        tipo_refeicao=(4, 2),
        dia_da_semana=(4, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(6, 3), (7, 3)],
            molhos=[(8, 3)],
            sementes=[(9, 3)],
            pratos_origem_animal=[(10, 3)],
            pratos_origem_vegetal=[(11, 3)],
            guarnicoes=[(12, 3)],
            pratos_base=[(13, 3), (14, 3)],
            sobremesas=[(15, 3)],
            bebidas=[(16, 3)]
        )
    ),
    MapeamentoCardapio(
        **_SAO_CRISTOVAO_HEADER,
        tipo_refeicao=(17, 2),
        dia_da_semana=(17, 3),
        bandejao=MapeamentoBandejao(
            pratos_origem_animal=[(19, 3)],
            pratos_origem_vegetal=[(20, 3)],
            guarnicoes=[(21, 3)],
            pratos_base=[(22, 3)],
            bebidas=[(23, 3), (24, 3)],
            sobremesas=[(25, 3)],
            saladas=[],
            molhos=[],
            sementes=[]
        )
    ),
    MapeamentoCardapio(
        **_SAO_CRISTOVAO_HEADER,
        tipo_refeicao=(26, 2),
        dia_da_semana=(26, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(28, 3), (29, 3)],
            molhos=[(30, 3)],
            sementes=[(31, 3)],
            pratos_origem_animal=[(32, 3)],
            pratos_origem_vegetal=[(33, 3)],
            guarnicoes=[(34, 3)],
            pratos_base=[(35, 3), (36, 3)],
            sobremesas=[(37, 3)],
            bebidas=[(38, 3)]
        )
    ),
    MapeamentoCardapio(
        **_SAO_CRISTOVAO_HEADER,
        tipo_refeicao=(39, 2),
        dia_da_semana=(39, 3),
        bandejao=MapeamentoBandejao(
            pratos_origem_animal=[(41, 3)],
            pratos_origem_vegetal=[(42, 3)],
            guarnicoes=[(43, 3)],
            pratos_base=[(44, 3)],
            bebidas=[(45, 3), (46, 3)],
            sobremesas=[(47, 3)],
            saladas=[],
            molhos=[],
            sementes=[]
        )
    ),
    MapeamentoCardapio(
        **_SAO_CRISTOVAO_HEADER,
        tipo_refeicao=(48, 2),
        dia_da_semana=(48, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(50, 3), (51, 3)],
            molhos=[(52, 3)],
            sementes=[(53, 3)],
            pratos_origem_animal=[(54, 3)],
            pratos_origem_vegetal=[(55, 3)],
            guarnicoes=[(56, 3)],
            pratos_base=[(57, 3), (58, 3)],
            sobremesas=[(59, 3)],
            bebidas=[(60, 3)]
        )
    ),
    MapeamentoCardapio(
        **_SAO_CRISTOVAO_HEADER,
        tipo_refeicao=(61, 2),
        dia_da_semana=(61, 3),
        bandejao=MapeamentoBandejao(
            pratos_origem_animal=[(63, 3)],
            pratos_origem_vegetal=[(64, 3)],
            guarnicoes=[(65, 3)],
            pratos_base=[(66, 3)],
            bebidas=[(67, 3), (68, 3)],
            sobremesas=[(69, 3)],
            saladas=[],
            molhos=[],
            sementes=[]
        )
    ),
    MapeamentoCardapio(
        **_SAO_CRISTOVAO_HEADER,
        tipo_refeicao=(70, 2),
        dia_da_semana=(70, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(72, 3), (73, 3)],
            molhos=[(74, 3)],
            sementes=[(75, 3)],
            pratos_origem_animal=[(76, 3)],
            pratos_origem_vegetal=[(77, 3)],
            guarnicoes=[(78, 3)],
            pratos_base=[(79, 3), (80, 3)],
            sobremesas=[(81, 3)],
            bebidas=[(82, 3)]
        )
    ),
    MapeamentoCardapio(
        **_SAO_CRISTOVAO_HEADER,
        tipo_refeicao=(83, 2),
        dia_da_semana=(83, 3),
        bandejao=MapeamentoBandejao(
            pratos_origem_animal=[(85, 3)],
            pratos_origem_vegetal=[(86, 3)],
            guarnicoes=[(87, 3)],
            pratos_base=[(88, 3)],
            bebidas=[(89, 3), (90, 3)],
            sobremesas=[(91, 3)],
            saladas=[],
            molhos=[],
            sementes=[]
        )
    ),
    MapeamentoCardapio(
        **_SAO_CRISTOVAO_HEADER,
        tipo_refeicao=(92, 2),
        dia_da_semana=(92, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(94, 3), (95, 3)],
            molhos=[(96, 3)],
            sementes=[(97, 3)],
            pratos_origem_animal=[(98, 3)],
            pratos_origem_vegetal=[(99, 3)],
            guarnicoes=[(100, 3)],
            pratos_base=[(101, 3), (102, 3)],
            sobremesas=[(103, 3)],
            bebidas=[(104, 3)]
        )
    ),
    MapeamentoCardapio(
        **_SAO_CRISTOVAO_HEADER,
        tipo_refeicao=(105, 2),
        dia_da_semana=(105, 3),
        bandejao=MapeamentoBandejao(
            pratos_origem_animal=[(107, 3)],
            pratos_origem_vegetal=[(108, 3)],
            guarnicoes=[(109, 3)],
            pratos_base=[(110, 3)],
            bebidas=[(111, 3), (112, 3)],
            sobremesas=[(113, 3)],
            saladas=[],
            molhos=[],
            sementes=[]
        )
    ),
]


_ITABAIANA_HEADER = {
    "campus": (2, 3),
    "fornecedor": (3, 2),
}

MAPEAMENTO_ITABAIANA = [
    MapeamentoCardapio(
        **_ITABAIANA_HEADER,
        tipo_refeicao=(5, 2),
        dia_da_semana=(5, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(7, 3), (8, 3)],
            molhos=[(9, 3)],
            sementes=[(10, 3)],
            pratos_origem_animal=[(11, 3)],
            pratos_origem_vegetal=[(12, 3)],
            guarnicoes=[(13, 3)],
            pratos_base=[(14, 3), (15, 3)],
            sobremesas=[(16, 3)],
            bebidas=[(17, 3)]
        )
    ),
    MapeamentoCardapio(
        **_ITABAIANA_HEADER,
        tipo_refeicao=(18, 2),
        dia_da_semana=(18, 3),
        bandejao=MapeamentoBandejao(
            pratos_origem_animal=[(20, 3)],
            pratos_origem_vegetal=[(21, 3)],
            guarnicoes=[(22, 3)],
            pratos_base=[(23, 3)],
            sobremesas=[(24, 3)],
            bebidas=[(25, 3), (26, 3)],
            saladas=[],
            molhos=[],
            sementes=[]
        )
    ),
    MapeamentoCardapio(
        **_ITABAIANA_HEADER,
        tipo_refeicao=(27, 2),
        dia_da_semana=(27, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(29, 3), (30, 3)],
            molhos=[(31, 3)],
            sementes=[(32, 3)],
            pratos_origem_animal=[(33, 3)],
            pratos_origem_vegetal=[(34, 3)],
            guarnicoes=[(35, 3)],
            pratos_base=[(36, 3), (37, 3)],
            sobremesas=[(38, 3)],
            bebidas=[(39, 3)]
        )
    ),
    MapeamentoCardapio(
        **_ITABAIANA_HEADER,
        tipo_refeicao=(40, 2),
        dia_da_semana=(40, 3),
        bandejao=MapeamentoBandejao(
            pratos_origem_animal=[(42, 3)],
            pratos_origem_vegetal=[(43, 3)],
            guarnicoes=[(44, 3)],
            pratos_base=[(45, 3)],
            sobremesas=[(46, 3)],
            bebidas=[(47, 3), (48, 3)],
            saladas=[],
            molhos=[],
            sementes=[]
        )
    ),
    MapeamentoCardapio(
        **_ITABAIANA_HEADER,
        tipo_refeicao=(49, 2),
        dia_da_semana=(49, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(51, 3), (52, 3)],
            molhos=[(53, 3)],
            sementes=[(54, 3)],
            pratos_origem_animal=[(55, 3)],
            pratos_origem_vegetal=[(56, 3)],
            guarnicoes=[(57, 3)],
            pratos_base=[(58, 3), (59, 3)],
            sobremesas=[(60, 3)],
            bebidas=[(61, 3)]
        )
    ),
    MapeamentoCardapio(
        **_ITABAIANA_HEADER,
        tipo_refeicao=(62, 2),
        dia_da_semana=(62, 3),
        bandejao=MapeamentoBandejao(
            pratos_origem_animal=[(64, 3)],
            pratos_origem_vegetal=[(65, 3)],
            guarnicoes=[(66, 3)],
            pratos_base=[(67, 3)],
            sobremesas=[(68, 3)],
            bebidas=[(69, 3), (70, 3)],
            saladas=[],
            molhos=[],
            sementes=[]
        )
    ),
    MapeamentoCardapio(
        **_ITABAIANA_HEADER,
        tipo_refeicao=(71, 2),
        dia_da_semana=(71, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(73, 3), (74, 3)],
            molhos=[(75, 3)],
            sementes=[(76, 3)],
            pratos_origem_animal=[(77, 3)],
            pratos_origem_vegetal=[(78, 3)],
            guarnicoes=[(79, 3)],
            pratos_base=[(80, 3), (81, 3)],
            sobremesas=[(82, 3)],
            bebidas=[(83, 3)]
        )
    ),
    MapeamentoCardapio(
        **_ITABAIANA_HEADER,
        tipo_refeicao=(84, 2),
        dia_da_semana=(84, 3),
        bandejao=MapeamentoBandejao(
            pratos_origem_animal=[(86, 3)],
            pratos_origem_vegetal=[(87, 3)],
            guarnicoes=[(88, 3)],
            pratos_base=[(89, 3)],
            sobremesas=[(90, 3)],
            bebidas=[(91, 3), (92, 3)],
            saladas=[],
            molhos=[],
            sementes=[]
        )
    ),
    MapeamentoCardapio(
        **_ITABAIANA_HEADER,
        tipo_refeicao=(93, 2),
        dia_da_semana=(93, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(95, 3), (96, 3)],
            molhos=[(97, 3)],
            sementes=[(98, 3)],
            pratos_origem_animal=[(99, 3)],
            pratos_origem_vegetal=[(100, 3)],
            guarnicoes=[(101, 3)],
            pratos_base=[(102, 3), (103, 3)],
            sobremesas=[(104, 3)],
            bebidas=[(105, 3)]
        )
    ),
    MapeamentoCardapio(
        **_ITABAIANA_HEADER,
        tipo_refeicao=(106, 2),
        dia_da_semana=(106, 3),
        bandejao=MapeamentoBandejao(
            pratos_origem_animal=[(108, 3)],
            pratos_origem_vegetal=[(109, 3)],
            guarnicoes=[(110, 3)],
            pratos_base=[(111, 3)],
            sobremesas=[(112, 3)],
            bebidas=[(113, 3), (114, 3)],
            saladas=[],
            molhos=[],
            sementes=[]
        )
    ),
]


_CENTRAL_HEADER = {
    "campus": (2, 3),
    "fornecedor": (3, 2),
}

MAPEAMENTO_CENTRAL = [
    MapeamentoCardapio(
        **_CENTRAL_HEADER,
        tipo_refeicao=(4, 2),
        dia_da_semana=(4, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(6, 3), (7, 3)],
            molhos=[(8, 3)],
            sementes=[(9, 3)],
            pratos_origem_animal=[(10, 3)],
            pratos_origem_vegetal=[(11, 3)],
            guarnicoes=[(12, 3)],
            pratos_base=[(13, 3), (14, 3)],
            sobremesas=[(15, 3)],
            bebidas=[(16, 3)]
        )
    ),
    MapeamentoCardapio(
        **_CENTRAL_HEADER,
        tipo_refeicao=(17, 2),
        dia_da_semana=(17, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(19, 3), (20, 3)],
            molhos=[(21, 3)],
            sementes=[(22, 3)],
            pratos_origem_animal=[(23, 3)],
            pratos_origem_vegetal=[(24, 3)],
            guarnicoes=[(25, 3)],
            pratos_base=[(26, 3), (27, 3)],
            sobremesas=[(28, 3)],
            bebidas=[(29, 3)]
        )
    ),
    MapeamentoCardapio(
        **_CENTRAL_HEADER,
        tipo_refeicao=(30, 2),
        dia_da_semana=(30, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(32, 3), (33, 3)],
            molhos=[(34, 3)],
            sementes=[(35, 3)],
            pratos_origem_animal=[(36, 3)],
            pratos_origem_vegetal=[(37, 3)],
            guarnicoes=[(38, 3)],
            pratos_base=[(39, 3), (40, 3)],
            sobremesas=[(41, 3)],
            bebidas=[(42, 3)]
        )
    ),
    MapeamentoCardapio(
        **_CENTRAL_HEADER,
        tipo_refeicao=(43, 2),
        dia_da_semana=(43, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(45, 3), (46, 3)],
            molhos=[(47, 3)],
            sementes=[(48, 3)],
            pratos_origem_animal=[(49, 3)],
            pratos_origem_vegetal=[(50, 3)],
            guarnicoes=[(51, 3)],
            pratos_base=[(52, 3), (53, 3)],
            sobremesas=[(54, 3)],
            bebidas=[(55, 3)]
        )
    ),
    MapeamentoCardapio(
        **_CENTRAL_HEADER,
        tipo_refeicao=(56, 2),
        dia_da_semana=(56, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(58, 3), (59, 3)],
            molhos=[(60, 3)],
            sementes=[(61, 3)],
            pratos_origem_animal=[(62, 3)],
            pratos_origem_vegetal=[(63, 3)],
            guarnicoes=[(64, 3)],
            pratos_base=[(65, 3), (66, 3)],
            sobremesas=[(67, 3)],
            bebidas=[(68, 3)]
        )
    ),
]

_LAGARTO_HEADER = {
    "campus": (2, 3),
    "fornecedor": (3, 2),
}

MAPEAMENTO_LAGARTO = [
    MapeamentoCardapio(
        **_LAGARTO_HEADER,
        tipo_refeicao=(4, 2),
        dia_da_semana=(4, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(6, 3), (7, 3)],
            molhos=[(8, 3)],
            sementes=[(9, 3)],
            pratos_origem_animal=[(10, 3)],
            pratos_origem_vegetal=[(11, 3)],
            guarnicoes=[(12, 3)],
            pratos_base=[(13, 3), (14, 3)],
            sobremesas=[(15, 3)],
            bebidas=[(16, 3)]
        )
    ),
    MapeamentoCardapio(
        **_LAGARTO_HEADER,
        tipo_refeicao=(17, 2),
        dia_da_semana=(17, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(19, 3), (20, 3)],
            molhos=[(21, 3)],
            sementes=[(22, 3)],
            pratos_origem_animal=[(23, 3)],
            pratos_origem_vegetal=[(24, 3)],
            guarnicoes=[(25, 3)],
            pratos_base=[(26, 3), (27, 3)],
            sobremesas=[(28, 3)],
            bebidas=[(29, 3)]
        )
    ),
    MapeamentoCardapio(
        **_LAGARTO_HEADER,
        tipo_refeicao=(30, 2),
        dia_da_semana=(30, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(32, 3), (33, 3)],
            molhos=[(34, 3)],
            sementes=[(35, 3)],
            pratos_origem_animal=[(36, 3)],
            pratos_origem_vegetal=[(37, 3)],
            guarnicoes=[(38, 3)],
            pratos_base=[(39, 3), (40, 3)],
            sobremesas=[(41, 3)],
            bebidas=[(42, 3)]
        )
    ),
    MapeamentoCardapio(
        **_LAGARTO_HEADER,
        tipo_refeicao=(43, 2),
        dia_da_semana=(43, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(45, 3), (46, 3)],
            molhos=[(47, 3)],
            sementes=[(48, 3)],
            pratos_origem_animal=[(49, 3)],
            pratos_origem_vegetal=[(50, 3)],
            guarnicoes=[(51, 3)],
            pratos_base=[(52, 3), (53, 3)],
            sobremesas=[(54, 3)],
            bebidas=[(55, 3)]
        )
    ),
    MapeamentoCardapio(
        **_LAGARTO_HEADER,
        tipo_refeicao=(56, 2),
        dia_da_semana=(56, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(58, 3), (59, 3)],
            molhos=[(60, 3)],
            sementes=[(61, 3)],
            pratos_origem_animal=[(62, 3)],
            pratos_origem_vegetal=[(63, 3)],
            guarnicoes=[(64, 3)],
            pratos_base=[(65, 3), (66, 3)],
            sobremesas=[(67, 3)],
            bebidas=[(68, 3)]
        )
    ),
]


_SERTAO_HEADER = {
    "campus": (2, 3),
    "fornecedor": (3, 2),
}
MAPEAMENTO_SERTAO = [
    MapeamentoCardapio(
        **_SERTAO_HEADER,
        tipo_refeicao=(5, 2),
        dia_da_semana=(5, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(7, 3), (8, 3)],
            molhos=[(9, 3)],
            sementes=[(10, 3)],
            pratos_origem_animal=[(11, 3)],
            pratos_origem_vegetal=[(12, 3)],
            guarnicoes=[(13, 3)],
            pratos_base=[(14, 3), (15, 3)],
            sobremesas=[(16, 3)],
            bebidas=[(17, 3)]
        )
    ),
    MapeamentoCardapio(
        **_SERTAO_HEADER,
        tipo_refeicao=(18, 2),
        dia_da_semana=(18, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(20, 3), (21, 3)],
            molhos=[(22, 3)],
            sementes=[(23, 3)],
            pratos_origem_animal=[(24, 3)],
            pratos_origem_vegetal=[(25, 3)],
            guarnicoes=[(26, 3)],
            pratos_base=[(27, 3), (28, 3)],
            sobremesas=[(29, 3)],
            bebidas=[(30, 3)]
        )
    ),
    MapeamentoCardapio(
        **_SERTAO_HEADER,
        tipo_refeicao=(31, 2),
        dia_da_semana=(31, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(33, 3), (34, 3)],
            molhos=[(35, 3)],
            sementes=[(36, 3)],
            pratos_origem_animal=[(37, 3)],
            pratos_origem_vegetal=[(38, 3)],
            guarnicoes=[(39, 3)],
            pratos_base=[(40, 3), (41, 3)],
            sobremesas=[(42, 3)],
            bebidas=[(43, 3)]
        )
    ),
    MapeamentoCardapio(
        **_SERTAO_HEADER,
        tipo_refeicao=(44, 2),
        dia_da_semana=(44, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(46, 3), (47, 3)],
            molhos=[(48, 3)],
            sementes=[(49, 3)],
            pratos_origem_animal=[(50, 3)],
            pratos_origem_vegetal=[(51, 3)],
            guarnicoes=[(52, 3)],
            pratos_base=[(53, 3), (54, 3)],
            sobremesas=[(55, 3)],
            bebidas=[(56, 3)]
        )
    ),
    MapeamentoCardapio(
        **_SERTAO_HEADER,
        tipo_refeicao=(57, 2),
        dia_da_semana=(57, 3),
        bandejao=MapeamentoBandejao(
            saladas=[(59, 3), (60, 3)],
            molhos=[(61, 3)],
            sementes=[(62, 3)],
            pratos_origem_animal=[(63, 3)],
            pratos_origem_vegetal=[(64, 3)],
            guarnicoes=[(65, 3)],
            pratos_base=[(66, 3), (67, 3)],
            sobremesas=[(68, 3)],
            bebidas=[(69, 3)]
        )
    ),
]


MAPEAMENTO_BANDEJOES = {
    Campus.SAO_CRISTOVAO: MAPEAMENTO_SAO_CRISTOVAO,
    Campus.ITABAIANA: MAPEAMENTO_ITABAIANA,
    Campus.CENTRAL: MAPEAMENTO_CENTRAL,
    Campus.LAGARTO: MAPEAMENTO_LAGARTO,
    Campus.SERTAO: MAPEAMENTO_SERTAO
}