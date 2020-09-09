import mock
from core.models import MultiAliasResource


def test_multi_alias_resource_capitalize_snames():
    mock_resource = mock.MagicMock(spec=MultiAliasResource)
    snames = ['test_name1', 'test_name2']
    mock_resource.snames = snames

    ret_val = MultiAliasResource._capitalize_snames(mock_resource)

    assert ret_val == list(map(lambda x: x.capitalize(), snames))


def test_multi_alias_resource_str():
    mock_resource = mock.MagicMock(spec=MultiAliasResource)
    name = 'test_name'
    mock_resource.name = name

    ret_val = MultiAliasResource.__str__(mock_resource)

    assert ret_val == name.capitalize()


def test_multi_alias_resource_repr():
    mock_resource = mock.MagicMock(spec=MultiAliasResource)
    name = 'test_name'
    snames = ['test_name1', 'test_name2']
    mock_resource.name = name
    mock_resource.snames = snames
    mock_resource.__str__.return_value = name.capitalize()
    mock_resource._capitalize_snames.return_value = list(map(lambda x: x.capitalize(), snames))

    ret_val = MultiAliasResource.__repr__(mock_resource)

    assert ret_val == f'Name: {name.capitalize()}\n\t{snames[0].capitalize()}\n\t{snames[1].capitalize()}'


def test_multi_alias_resource_aliases():
    name = 'test_name'
    snames = ['test_name1', 'test_name2']
    resource = MultiAliasResource(name=name, snames=snames)

    ret_val = resource.aliases

    assert ret_val == [name.capitalize()] + list(map(lambda x: x.capitalize(), snames))
