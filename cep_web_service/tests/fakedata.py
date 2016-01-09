from faker import Factory

fake = Factory.create('pt_BR')


class PostmonModelFake(object):
    """
    Represents a fake model in postmon
    """
    def __init__(self, faker):
        self.faker = faker


class Cidade(PostmonModelFake):

    def __init__(self, faker):
        super(self.__class__, self).__init__(faker)
        self.nome = self.faker.city()


class Estado(PostmonModelFake):

    def __init__(self, faker):
        super(self.__class__, self).__init__(faker)
        self.nome = self.faker.estado_nome()


class Endereco(PostmonModelFake):

    def __init__(self, faker, cidade_fake, estado_fake):
        super(self.__class__, self).__init__(faker)
        self.logradouro = self.faker.address()
        self.cep = self.faker.postcode()
        self.estado = estado_fake
        self.cidade = cidade_fake
        self.bairro = self.faker.bairro()


def fake_endereco():
    cidade = Cidade(fake)
    estado = Estado(fake)

    endereco = Endereco(fake, cidade, estado)
    return endereco


class ZipcodeFake():
    """
    represents a fake zipcode document.
    """
    def __init__(self, fake_generator_function):
        self.endereco = fake_generator_function()

    def to_dict(self):
        return {
            'zip_code': self.endereco.cep,
            'address': self.endereco.logradouro,
            'neighborhood': self.endereco.bairro,
            'state': self.endereco.estado.nome,
            'city': self.endereco.cidade.nome
        }


def get_many_zip_codes(how_many=1):
    return [ZipcodeFake(fake_endereco) for _ in range(0, how_many)]
