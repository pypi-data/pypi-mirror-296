from django.core import validators as _django_validators
from django.db import models as _models
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions as _exceptions

from b2_utils import validators as _validators

__all__ = [
    "CpfField",
    "CnpjField",
    "DocumentField",
    "CIText",
    "CICharField",
    "CIEmailField",
]


class CpfField(_models.CharField):
    description = "(Brazil) Cadastro de Pessoa Física"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 11
        kwargs["validators"] = [
            _django_validators.MinLengthValidator(11),
            _validators.validate_cpf,
        ]

        super().__init__(*args, **kwargs)


class CnpjField(_models.CharField):
    description = "(Brazil) Cadastro Nacional da Pessoa Jurídica"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 14
        kwargs["validators"] = [
            _django_validators.MinLengthValidator(14),
            _validators.validate_cnpj,
        ]

        super().__init__(*args, **kwargs)


class DocumentField(_models.CharField):
    CNPJ_LEN = 14
    CPF_LEN = 11

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 14
        kwargs["validators"] = [
            _django_validators.MinLengthValidator(11),
            _django_validators.MaxLengthValidator(14),
            self.validate_cnpj_cpf,
        ]

        super().__init__(*args, **kwargs)

    @classmethod
    def validate_cnpj_cpf(cls, value):
        if len(value) == cls.CPF_LEN:
            _validators.validate_cpf(value)

        elif len(value) == cls.CNPJ_LEN:
            _validators.validate_cnpj(value)

        else:
            raise _exceptions.ValidationError(
                _("Invalid CPF or CNPJ"),
                "invalid_cpf_or_cnpj",
            )


class PISField(_models.CharField):
    description = "(Brazil) PIS (Programa de Integração Social) number."

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 11
        kwargs["validators"] = [
            _django_validators.MinLengthValidator(11),
            _validators.validate_pis,
        ]

        super().__init__(*args, **kwargs)


class CIText:
    def get_internal_type(self):
        return "CI" + super().get_internal_type()

    def db_type(self, connection):
        return "citext"


class CICharField(CIText, _models.CharField):
    pass


class CIEmailField(CIText, _models.EmailField):
    pass


class HexColorField(_models.CharField):
    description = "Hexadecimal color code field"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 7
        kwargs["validators"] = [
            _django_validators.MinLengthValidator(7),
            _validators.validate_hex_color_code,
        ]

        super().__init__(*args, **kwargs)
