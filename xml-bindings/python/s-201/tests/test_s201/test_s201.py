import pytest
import os
import pyxb

from iso639 import Lang
from datetime import date
from s201 import s201


@pytest.fixture
def s201_msg_xml():
    # Get absolute path of this test file
    test_dir = os.path.dirname(__file__)

    # Open the file
    s201_msg_file = open(test_dir + '/s201-msg.xml', mode="rb")

    # And return the contents
    yield s201_msg_file.read()


@pytest.fixture
def s201_dataset():
    # Create a new dataset
    s201Dataset = s201.Dataset()

    # Initialise the dataset
    s201Dataset.id = "CorkHoleTestDataset"

    # Bounded by section
    boundingShape = s201._ImportedBinding__gml.BoundingShapeType()
    boundingShape.Envelope = s201._ImportedBinding__gml.EnvelopeType()
    boundingShape.Envelope.srsName = 'EPSG:4326'
    boundingShape.Envelope.srsDimension = '1'
    boundingShape.Envelope.lowerCorner = [51.8916667, 1.4233333]
    boundingShape.Envelope.upperCorner = [51.8916667, 1.4233333]
    s201Dataset.boundingShape = boundingShape

    # Add the dataset identification information
    dataSetIdentificationType = s201._ImportedBinding__S100.DataSetIdentificationType()
    dataSetIdentificationType.encodingSpecification = 'S-100 Part 10b'
    dataSetIdentificationType.encodingSpecificationEdition = '1.0'
    dataSetIdentificationType.productIdentifier = 'S-201'
    dataSetIdentificationType.productEdition = '0.0.1'
    dataSetIdentificationType.applicationProfile = 'test'
    dataSetIdentificationType.datasetFileIdentifier = 'junit'
    dataSetIdentificationType.datasetTitle = 'S-201 Cork Hole Test Dataset'
    dataSetIdentificationType.datasetReferenceDate = date(2001, 1, 1)
    dataSetIdentificationType.datasetLanguage = Lang("English").pt3
    dataSetIdentificationType.datasetAbstract = 'Test dataset for unit testing'
    dataSetIdentificationType.datasetTopicCategory = [s201._ImportedBinding__S100.MD_TopicCategoryCode.oceans]
    dataSetIdentificationType.datasetPurpose = s201._ImportedBinding__S100.datasetPurposeType.base
    dataSetIdentificationType.updateNumber = 2
    s201Dataset.DatasetIdentificationInformation = dataSetIdentificationType

    # Add the dataset members - A single Virtual AIS Aid to Navigation
    s201Dataset.members = s201.CTD_ANON_52()
    s201Dataset.members.VirtualAISAidToNavigation = []
    virtualAISAidToNavigation = s201.VirtualAISAidToNavigation()
    virtualAISAidToNavigation.id = 'ID001'
    virtualAISAidToNavigation.boundingShape = boundingShape
    virtualAISAidToNavigation.idCode = 'urn:mrn:grad:aton:test:corkhole'
    virtualAISAidToNavigation.mMSICode = '992359598'
    #virtualAISAidToNavigation.source = 'CGHT'
    virtualAISAidToNavigation.sourceDate = date(2000, 1, 1)
    virtualAISAidToNavigation.pictorialRepresentation = 'N/A'
    virtualAISAidToNavigation.installationDate = date(2000, 1, 1)
    virtualAISAidToNavigation.inspectionFrequency = 'yearly'
    virtualAISAidToNavigation.inspectionRequirements = 'IALA'
    virtualAISAidToNavigation.aToNMaintenanceRecord = 'urn:mrn:grad:aton:test:corkhole:maintenance:x001'
    virtualAISAidToNavigation.virtualAISAidToNavigationType = 'Special Purpose'
    virtualAISAidToNavigation.virtualAISbroadcasts = []
    virtualAISAidToNavigation.geometry = [s201.CTD_ANON_16()]
    virtualAISAidToNavigation.geometry[0].pointProperty = s201._ImportedBinding__S100.PointPropertyType()
    virtualAISAidToNavigation.geometry[0].pointProperty.Point =  s201._ImportedBinding__S100.PointType()
    virtualAISAidToNavigation.geometry[0].pointProperty.Point.id = 'AtoNPoint'
    virtualAISAidToNavigation.geometry[0].pointProperty.Point.srsName = 'EPSG:4326'
    virtualAISAidToNavigation.geometry[0].pointProperty.Point.srsDimension = '1'
    virtualAISAidToNavigation.geometry[0].pointProperty.Point.pos = [51.8916667, 1.4233333]
    s201Dataset.members.VirtualAISAidToNavigation.append(virtualAISAidToNavigation)

    # And return the dataset
    yield s201Dataset


def test_marshall(s201_dataset):
    """
    Test that we can successfully marshall an S-201 dataset from the generated
    python objects using the PYXB library.
    """    
    # And Marshall to XMl
    s201_msg_xml = s201_dataset.toxml("utf-8", element_name='Dataset').decode('utf-8')
    
    # Make sure the XMl seems correct
    assert s201_msg_xml != None


def test_unmarshall(s201_msg_xml):
    """
    Test that we can successfully unmarshall a packaged S-201 dataset using the 
    generated python objects of the PYXB library.
    """
    # Parse the S201 test message XML
    s201_msg = s201.CreateFromDocument(s201_msg_xml)

    # And make sure the contents seem correct
    assert s201_msg.members.VirtualAISAidToNavigation[0].featureName[0].name == 'Test AtoN for Cork Hole'

