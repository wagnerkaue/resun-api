import dataclasses


@dataclasses.dataclass(frozen=True)
class MapeamentoBandejao:
    """Descreve em qual célula (linha e coluna) está cada informação do cardápio"""
    saladas: list[tuple[int, int]]
    molhos: list[tuple[int, int]]
    sementes: list[tuple[int, int]]
    pratos_origem_animal: list[tuple[int, int]]
    pratos_origem_vegetal: list[tuple[int, int]]
    guarnicoes: list[tuple[int, int]]
    pratos_base: list[tuple[int, int]]
    sobremesas: list[tuple[int, int]]
    bebidas: list[tuple[int, int]]


@dataclasses.dataclass(frozen=True)
class MapeamentoCardapio:
    """Descreve em qual célula (linha e coluna) está cada informação do bandejão"""
    campus: tuple[int, int]
    fornecedor: tuple[int, int]
    tipo_refeicao: tuple[int, int]
    dia_da_semana: tuple[int, int]
    bandejao: MapeamentoBandejao
