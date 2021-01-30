import getDataDeps


def test_always_passes():
    assert True


def test_getListOfFiles_structure():
    listOfFiles = getDataDeps.getListOfFiles(
        './examples/normalProjectStructure')
    assert listOfFiles is not None
    assert len(listOfFiles) == 5


def test_getListOfFiles_content():
    expected = ['./examples/normalProjectStructure/code/03_modeling/03A_train.py', './examples/normalProjectStructure/code/04_modelResults/04A_stataCode.do',
                './examples/normalProjectStructure/code/01_dataConstruct/01A_analyticFile.R', './examples/normalProjectStructure/code/02_analyses/02B_featureEngineering.R', './examples/normalProjectStructure/code/02_analyses/02A_descriptives.R']
    actual = getDataDeps.getListOfFiles(
        './examples/normalProjectStructure')

    assert len(actual) == len(expected)
    # assert all([a == b for a, b in zip(actual, expected)])


def test_extractDataDeps_structure():
    example_file_structure = ['./examples/normalProjectStructure/code/03_modeling/03A_train.py', './examples/normalProjectStructure/code/04_modelResults/04A_stataCode.do',
                              './examples/normalProjectStructure/code/01_dataConstruct/01A_analyticFile.R', './examples/normalProjectStructure/code/02_analyses/02B_featureEngineering.R', './examples/normalProjectStructure/code/02_analyses/02A_descriptives.R']
    data, save, read = getDataDeps.extractDataDeps(example_file_structure)

    assert save is not None
    assert len(save) == 5

    assert read is not None
    assert len(read) == 7

    assert data is not None
    assert len(data) == 8
    assert [len(data[x]) for x in data] == [2, 2, 2, 2, 2, 2, 2, 2]
