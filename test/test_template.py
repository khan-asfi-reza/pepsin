from pepsin.template import Template, TemplateDoesNotExistError


def test_template_does_not_exist():
    template = Template(template_name="TEST")

    try:
        template.read()

    except TemplateDoesNotExistError as error:
        assert isinstance(error, TemplateDoesNotExistError)
